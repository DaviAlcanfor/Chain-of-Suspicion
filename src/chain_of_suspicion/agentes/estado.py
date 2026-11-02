import operator
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import timedelta
from typing import Annotated, Literal, TypedDict

from ..dominio.eventos import EventoDePartida, MotivoFim
from ..dominio.ids import PersonagemId
from ..dominio.mundo import Mundo
from .agente import Agente
from .turno import PropostaDoAgente

NomeNo = Literal[
    "iniciar_rodada",
    "escolher_vez",
    "decidir",
    "aplicar_acao",
    "avancar_tempo",
]


class No:
    INICIAR_RODADA: NomeNo = "iniciar_rodada"
    ESCOLHER_VEZ: NomeNo = "escolher_vez"
    DECIDIR: NomeNo = "decidir"
    APLICAR_ACAO: NomeNo = "aplicar_acao"
    AVANCAR_TEMPO: NomeNo = "avancar_tempo"


@dataclass(frozen=True)
class LimitesDaPartida:
    passos: int
    passo: timedelta
    tentativas_por_acao: int


@dataclass(frozen=True)
class ContextoDaPartida:
    agentes: Mapping[PersonagemId, Agente]
    limites: LimitesDaPartida


class EstadoPartida(TypedDict):
    mundo: Mundo
    eventos: Annotated[list[EventoDePartida], operator.add]
    fila: list[PersonagemId]
    vez: PersonagemId | None
    tentativas: int
    proposta: PropostaDoAgente | None
    recusa: str | None
    passos_restantes: int
    fim: MotivoFim | None
