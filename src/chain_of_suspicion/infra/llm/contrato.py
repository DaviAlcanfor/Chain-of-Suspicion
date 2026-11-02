from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel

from ...dominio.base import ModeloBase


class PapelMensagem(StrEnum):
    SISTEMA = "sistema"
    USUARIO = "usuario"


class Mensagem(ModeloBase, frozen=True):
    papel: PapelMensagem
    conteudo: str


@dataclass(frozen=True)
class RespostaLLM[S: BaseModel]:
    saida: S
    tokens_entrada: int = 0
    tokens_saida: int = 0


class ProvedorLLM(Protocol):
    async def gerar[S: BaseModel](
        self, mensagens: Sequence[Mensagem], saida: type[S]
    ) -> RespostaLLM[S]: ...
