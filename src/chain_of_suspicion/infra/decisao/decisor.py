from collections.abc import Mapping, Sequence
from typing import Protocol

from ...dominio.enums import TipoAcao
from ...dominio.regras import DecisaoAmeaca, DecisaoContradicao, Pressao, VisaoPersonagem
from ...erros.excecoes import FalhaNoLLM
from ...prompts.carregador import prompt_ameaca, prompt_contradicao
from ...prompts.descricoes import DESCRICAO_DA_ACAO
from .cliente import ClienteDeDecisao
from .perguntas import (
    NIVEIS_DE_AMEACA,
    Pergunta,
    PerguntaDeDecisao,
    Resultado,
    ResultadoBooleano,
    ResultadoEscolha,
    ResultadoNota,
)


class Decisor(Protocol):
    async def escolher_acao(self, estado: str, viaveis: Sequence[TipoAcao]) -> TipoAcao: ...

    async def escolher_alvo(self, estado: str, opcoes: Mapping[str, str]) -> str: ...

    async def deve_mentir(self, estado: str) -> bool: ...

    async def ameaca(self, visao: VisaoPersonagem, pressao: Pressao) -> DecisaoAmeaca: ...

    async def contradiz(self, declaracao: str, fato: str) -> DecisaoContradicao: ...


class DecisorGateway:
    def __init__(self, cliente: ClienteDeDecisao) -> None:
        self._cliente = cliente

    async def escolher_acao(self, estado: str, viaveis: Sequence[TipoAcao]) -> TipoAcao:
        opcoes = {acao.value: DESCRICAO_DA_ACAO[acao] for acao in viaveis}
        resultado = await self._escolha(estado, PerguntaDeDecisao.ESCOLHER_ACAO, opcoes)
        return TipoAcao(resultado.escolha)

    async def escolher_alvo(self, estado: str, opcoes: Mapping[str, str]) -> str:
        resultado = await self._escolha(estado, PerguntaDeDecisao.ESCOLHER_ALVO, dict(opcoes))
        return resultado.escolha

    async def deve_mentir(self, estado: str) -> bool:
        resultado = await self._cliente.perguntar(
            estado, Pergunta(tipo=PerguntaDeDecisao.DEVE_MENTIR)
        )
        return _como(ResultadoBooleano, resultado).verdadeiro

    async def ameaca(self, visao: VisaoPersonagem, pressao: Pressao) -> DecisaoAmeaca:
        pergunta = Pergunta(tipo=PerguntaDeDecisao.AMEACA, niveis=NIVEIS_DE_AMEACA)
        resultado = await self._cliente.perguntar(prompt_ameaca(visao, pressao), pergunta)
        return DecisaoAmeaca(ameaca=_como(ResultadoNota, resultado).normalizada)

    async def contradiz(self, declaracao: str, fato: str) -> DecisaoContradicao:
        pergunta = Pergunta(tipo=PerguntaDeDecisao.CONTRADICAO)
        resultado = await self._cliente.perguntar(prompt_contradicao(declaracao, fato), pergunta)
        probabilidade = _como(ResultadoBooleano, resultado).probabilidade
        return DecisaoContradicao(
            contradiz=probabilidade >= 0.5, confianca=max(probabilidade, 1 - probabilidade)
        )

    async def _escolha(
        self, estado: str, tipo: PerguntaDeDecisao, opcoes: dict[str, str]
    ) -> ResultadoEscolha:
        resultado = await self._cliente.perguntar(estado, Pergunta(tipo=tipo, opcoes=opcoes))
        escolha = _como(ResultadoEscolha, resultado)
        if escolha.escolha not in opcoes:
            raise FalhaNoLLM(f"o decisor escolheu '{escolha.escolha}', fora das opções")
        return escolha


def _como[R: ResultadoBooleano | ResultadoEscolha | ResultadoNota](
    tipo: type[R], resultado: Resultado
) -> R:
    if not isinstance(resultado, tipo):
        raise FalhaNoLLM(f"esperava {tipo.__name__}, veio {type(resultado).__name__}")
    return resultado


class DecisorFalso:
    def __init__(self, acao: TipoAcao | None = None, mentir: bool = False) -> None:
        self._acao = acao
        self._mentir = mentir

    async def escolher_acao(self, estado: str, viaveis: Sequence[TipoAcao]) -> TipoAcao:
        if self._acao is not None and self._acao in viaveis:
            return self._acao
        return viaveis[0]

    async def escolher_alvo(self, estado: str, opcoes: Mapping[str, str]) -> str:
        return next(iter(opcoes))

    async def deve_mentir(self, estado: str) -> bool:
        return self._mentir

    async def ameaca(self, visao: VisaoPersonagem, pressao: Pressao) -> DecisaoAmeaca:
        return DecisaoAmeaca(ameaca=0.0)

    async def contradiz(self, declaracao: str, fato: str) -> DecisaoContradicao:
        return DecisaoContradicao(contradiz=False, confianca=1.0)
