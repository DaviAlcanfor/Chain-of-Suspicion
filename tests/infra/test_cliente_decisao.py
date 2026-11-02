import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from chain_of_suspicion.config.modelos_llm import ModeloDecisao
from chain_of_suspicion.erros.excecoes import FalhaNoLLM, OrcamentoEstourado
from chain_of_suspicion.infra.decisao.cliente import ClienteHttp
from chain_of_suspicion.infra.decisao.perguntas import (
    Pergunta,
    PerguntaDeDecisao,
    ResultadoBooleano,
    ResultadoEscolha,
    ResultadoNota,
)
from chain_of_suspicion.infra.llm.controle import ControleDeUso
from chain_of_suspicion.infra.llm.langchain import PoliticaDeChamada

USO = {"inputTokens": 100, "outputTokens": 10}
CUSTO = {"gateway": {"cost": "0.00002"}}


def _corpo(resposta: dict[str, Any]) -> dict[str, Any]:
    return {"answers": {"r": resposta}, "usage": USO, "providerMetadata": CUSTO}


def _cliente(
    tratador: Callable[[httpx.Request], httpx.Response], tentativas: int = 2
) -> tuple[ClienteHttp, ControleDeUso]:
    http = httpx.AsyncClient(
        base_url="http://gateway.teste/v1", transport=httpx.MockTransport(tratador)
    )
    controle = ControleDeUso(2, 1.0)
    politica = PoliticaDeChamada(
        ModeloDecisao.D1_ULTRA, 1.0, tentativas, espera_inicial_segundos=0.0
    )
    return ClienteHttp(http, politica, controle), controle


async def test_booleana_envia_o_formato_certo_e_registra_o_custo() -> None:
    vistos: list[dict[str, Any]] = []

    def tratador(pedido: httpx.Request) -> httpx.Response:
        vistos.append({"url": str(pedido.url), "corpo": json.loads(pedido.content)})
        return httpx.Response(200, json=_corpo({"type": "boolean", "probability": 0.93}))

    cliente, controle = _cliente(tratador)
    resultado = await cliente.perguntar("estado", Pergunta(tipo=PerguntaDeDecisao.DEVE_MENTIR))
    assert resultado == ResultadoBooleano(probabilidade=0.93)
    assert vistos[0]["url"] == "http://gateway.teste/v1/evaluate"
    assert vistos[0]["corpo"]["model"] == "liquid/d1-ultra"
    assert vistos[0]["corpo"]["state"] == "estado"
    assert vistos[0]["corpo"]["questions"]["r"]["type"] == "boolean"
    assert controle.custo_usd == pytest.approx(0.00002)
    assert (controle.tokens_entrada, controle.tokens_saida) == (100, 10)


async def test_escolha_leva_as_opcoes_como_criterios() -> None:
    corpos: list[dict[str, Any]] = []

    def tratador(pedido: httpx.Request) -> httpx.Response:
        corpos.append(json.loads(pedido.content))
        resposta = {
            "type": "choice",
            "choice": "mover",
            "probabilities": {"mover": 0.8, "esperar": 0.2},
        }
        return httpx.Response(200, json=_corpo(resposta))

    cliente, _ = _cliente(tratador)
    pergunta = Pergunta(
        tipo=PerguntaDeDecisao.ESCOLHER_ACAO, opcoes={"mover": "ir", "esperar": "ficar"}
    )
    resultado = await cliente.perguntar("estado", pergunta)
    assert isinstance(resultado, ResultadoEscolha)
    assert resultado.escolha == "mover"
    assert corpos[0]["questions"]["r"]["criteria"] == {"mover": "ir", "esperar": "ficar"}


async def test_nota_e_normalizada_pelo_numero_de_niveis() -> None:
    def tratador(pedido: httpx.Request) -> httpx.Response:
        resposta = {
            "type": "score",
            "score": 3.0,
            "probabilities": {"0": 0, "1": 0, "2": 0, "3": 1, "4": 0},
        }
        return httpx.Response(200, json=_corpo(resposta))

    cliente, _ = _cliente(tratador)
    pergunta = Pergunta(tipo=PerguntaDeDecisao.AMEACA, niveis=["a", "b", "c", "d", "e"])
    resultado = await cliente.perguntar("estado", pergunta)
    assert isinstance(resultado, ResultadoNota)
    assert resultado.normalizada == pytest.approx(0.75)


async def test_erro_transitorio_e_repetido() -> None:
    chamadas = []

    def tratador(pedido: httpx.Request) -> httpx.Response:
        chamadas.append(1)
        if len(chamadas) == 1:
            return httpx.Response(503)
        return httpx.Response(200, json=_corpo({"type": "boolean", "probability": 0.1}))

    cliente, _ = _cliente(tratador)
    await cliente.perguntar("e", Pergunta(tipo=PerguntaDeDecisao.CONTRADICAO))
    assert len(chamadas) == 2


async def test_erro_do_cliente_nao_e_repetido() -> None:
    chamadas = []

    def tratador(pedido: httpx.Request) -> httpx.Response:
        chamadas.append(1)
        return httpx.Response(401, json={"error": "chave inválida"})

    cliente, _ = _cliente(tratador)
    with pytest.raises(FalhaNoLLM):
        await cliente.perguntar("e", Pergunta(tipo=PerguntaDeDecisao.CONTRADICAO))
    assert len(chamadas) == 1


async def test_resposta_fora_do_formato_falha() -> None:
    cliente, _ = _cliente(lambda pedido: httpx.Response(200, json={"answers": {}}))
    with pytest.raises(FalhaNoLLM):
        await cliente.perguntar("e", Pergunta(tipo=PerguntaDeDecisao.CONTRADICAO))


async def test_teto_de_custo_vale_para_decisoes() -> None:
    cliente, controle = _cliente(lambda pedido: httpx.Response(200))
    controle.custo_usd = 1.0
    with pytest.raises(OrcamentoEstourado):
        await cliente.perguntar("e", Pergunta(tipo=PerguntaDeDecisao.CONTRADICAO))
