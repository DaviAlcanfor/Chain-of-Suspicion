from collections.abc import Awaitable, Callable
from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel

from ...dominio.enums import TipoAcao
from ...dominio.regras import Pressao, VisaoPersonagem
from ...infra.decisao.decisor import Decisor
from ...infra.decisao.perguntas import INSTRUCAO_DA_PERGUNTA, PerguntaDeDecisao


class ArgsEscolherAcao(BaseModel):
    estado: str
    viaveis: list[TipoAcao]


class ArgsEscolherAlvo(BaseModel):
    estado: str
    opcoes: dict[str, str]


class ArgsDeveMentir(BaseModel):
    estado: str


class ArgsAmeaca(BaseModel):
    visao: VisaoPersonagem
    pressao: Pressao


class ArgsContradicao(BaseModel):
    declaracao: str
    fato: str


ESQUEMA_DOS_ARGUMENTOS: dict[PerguntaDeDecisao, type[BaseModel]] = {
    PerguntaDeDecisao.ESCOLHER_ACAO: ArgsEscolherAcao,
    PerguntaDeDecisao.ESCOLHER_ALVO: ArgsEscolherAlvo,
    PerguntaDeDecisao.DEVE_MENTIR: ArgsDeveMentir,
    PerguntaDeDecisao.AMEACA: ArgsAmeaca,
    PerguntaDeDecisao.CONTRADICAO: ArgsContradicao,
}

type Execucao = Callable[..., Awaitable[dict[str, Any]]]


def criar_ferramentas(decisor: Decisor) -> dict[PerguntaDeDecisao, StructuredTool]:
    execucoes: dict[PerguntaDeDecisao, Execucao] = {
        PerguntaDeDecisao.ESCOLHER_ACAO: lambda estado, viaveis: _acao(decisor, estado, viaveis),
        PerguntaDeDecisao.ESCOLHER_ALVO: lambda estado, opcoes: _alvo(decisor, estado, opcoes),
        PerguntaDeDecisao.DEVE_MENTIR: lambda estado: _mentir(decisor, estado),
        PerguntaDeDecisao.AMEACA: lambda visao, pressao: _ameaca(decisor, visao, pressao),
        PerguntaDeDecisao.CONTRADICAO: lambda declaracao, fato: _contradicao(
            decisor, declaracao, fato
        ),
    }
    return {
        pergunta: StructuredTool.from_function(
            coroutine=execucoes[pergunta],
            name=pergunta.value,
            description=INSTRUCAO_DA_PERGUNTA[pergunta],
            args_schema=ESQUEMA_DOS_ARGUMENTOS[pergunta],
        )
        for pergunta in PerguntaDeDecisao
    }


async def _acao(decisor: Decisor, estado: str, viaveis: list[TipoAcao]) -> dict[str, Any]:
    return {"acao": (await decisor.escolher_acao(estado, viaveis)).value}


async def _alvo(decisor: Decisor, estado: str, opcoes: dict[str, str]) -> dict[str, Any]:
    return {"alvo": await decisor.escolher_alvo(estado, opcoes)}


async def _mentir(decisor: Decisor, estado: str) -> dict[str, Any]:
    return {"mentir": await decisor.deve_mentir(estado)}


async def _ameaca(decisor: Decisor, visao: VisaoPersonagem, pressao: Pressao) -> dict[str, Any]:
    return {"ameaca": (await decisor.ameaca(visao, pressao)).ameaca}


async def _contradicao(decisor: Decisor, declaracao: str, fato: str) -> dict[str, Any]:
    decisao = await decisor.contradiz(declaracao, fato)
    return {"contradiz": decisao.contradiz, "confianca": decisao.confianca}
