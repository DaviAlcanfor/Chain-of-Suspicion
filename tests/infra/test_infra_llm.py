import asyncio
from typing import Any, cast

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from chain_of_suspicion.config.modelos_llm import ModeloLLM
from chain_of_suspicion.dominio.regras import DecisaoAmeaca
from chain_of_suspicion.erros.excecoes import (
    FalhaNoLLM,
    OrcamentoEstourado,
    TempoEsgotadoNoLLM,
)
from chain_of_suspicion.infra.llm.contrato import Mensagem, PapelMensagem
from chain_of_suspicion.infra.llm.controle import ControleDeUso
from chain_of_suspicion.infra.llm.falso import ProvedorFalso
from chain_of_suspicion.infra.llm.langchain import PoliticaDeChamada, ProvedorLangChain

PEDIDO = [Mensagem(papel=PapelMensagem.USUARIO, conteudo="oi")]
USO = {"input_tokens": 1000, "output_tokens": 200, "total_tokens": 1200}


class _Executor:
    def __init__(self, *comportamentos: Any) -> None:
        self._comportamentos = list(comportamentos)
        self.chamadas = 0

    async def ainvoke(self, entrada: object) -> Any:
        self.chamadas += 1
        comportamento = self._comportamentos.pop(0)
        if isinstance(comportamento, Exception):
            raise comportamento
        if comportamento == "travar":
            await asyncio.sleep(10)
        return comportamento


class _ChatFalso:
    def __init__(self, executor: _Executor) -> None:
        self._executor = executor

    def with_structured_output(self, esquema: object, include_raw: bool) -> _Executor:
        return self._executor


def _bruto(ameaca: float = 0.3) -> dict[str, Any]:
    raw = AIMessage(content="", usage_metadata=USO)
    return {"raw": raw, "parsed": DecisaoAmeaca(ameaca=ameaca), "parsing_error": None}


def _provedor(
    executor: _Executor, tentativas: int = 2, timeout: float = 1.0
) -> tuple[ProvedorLangChain, ControleDeUso]:
    controle = ControleDeUso(simultaneas=2, teto_usd=1.0)
    politica = PoliticaDeChamada(
        ModeloLLM.GPT_6_LUNA, timeout, tentativas, espera_inicial_segundos=0.0
    )
    chat = cast(BaseChatModel, _ChatFalso(executor))
    return ProvedorLangChain(chat, politica, controle), controle


async def test_resposta_valida_registra_tokens_e_custo() -> None:
    provedor, controle = _provedor(_Executor(_bruto()))
    resposta = await provedor.gerar(PEDIDO, DecisaoAmeaca)
    assert resposta.saida.ameaca == 0.3
    assert (resposta.tokens_entrada, resposta.tokens_saida) == (1000, 200)
    assert controle.custo_usd == pytest.approx((1000 * 0.10 + 200 * 0.50) / 1_000_000)


async def test_erro_transitorio_e_repetido() -> None:
    executor = _Executor(RuntimeError("rede"), _bruto())
    provedor, _ = _provedor(executor)
    await provedor.gerar(PEDIDO, DecisaoAmeaca)
    assert executor.chamadas == 2


async def test_falha_persistente_vira_falha_no_llm() -> None:
    executor = _Executor(RuntimeError("a"), RuntimeError("b"))
    provedor, _ = _provedor(executor)
    with pytest.raises(FalhaNoLLM):
        await provedor.gerar(PEDIDO, DecisaoAmeaca)
    assert executor.chamadas == 2


async def test_estouro_de_tempo_vira_tempo_esgotado() -> None:
    provedor, _ = _provedor(_Executor("travar"), tentativas=1, timeout=0.01)
    with pytest.raises(TempoEsgotadoNoLLM):
        await provedor.gerar(PEDIDO, DecisaoAmeaca)


async def test_resposta_fora_do_formato_falha() -> None:
    fora = {"raw": None, "parsed": None, "parsing_error": ValueError("x")}
    provedor, _ = _provedor(_Executor(fora))
    with pytest.raises(FalhaNoLLM):
        await provedor.gerar(PEDIDO, DecisaoAmeaca)


async def test_teto_de_custo_bloqueia_novas_chamadas() -> None:
    provedor, controle = _provedor(_Executor(_bruto()))
    controle.custo_usd = 1.0
    with pytest.raises(OrcamentoEstourado):
        await provedor.gerar(PEDIDO, DecisaoAmeaca)


async def test_provedor_falso_segue_o_roteiro() -> None:
    falso = ProvedorFalso(DecisaoAmeaca(ameaca=0.7), TempoEsgotadoNoLLM("t"))
    assert (await falso.gerar(PEDIDO, DecisaoAmeaca)).saida.ameaca == 0.7
    with pytest.raises(TempoEsgotadoNoLLM):
        await falso.gerar(PEDIDO, DecisaoAmeaca)
    with pytest.raises(FalhaNoLLM):
        await falso.gerar(PEDIDO, DecisaoAmeaca)
    assert len(falso.pedidos) == 3
