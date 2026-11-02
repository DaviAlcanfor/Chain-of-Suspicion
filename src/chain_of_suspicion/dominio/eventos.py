from enum import StrEnum

from pydantic import AwareDatetime

from .base import ModeloBase
from .enums import TipoAcao
from .ids import PersonagemId


class TipoEvento(StrEnum):
    ACAO_APLICADA = "acao_aplicada"
    ACAO_RECUSADA = "acao_recusada"
    FALA = "fala"
    ESPERA_FORCADA = "espera_forcada"
    PARTIDA_ENCERRADA = "partida_encerrada"


class MotivoFim(StrEnum):
    PASSOS_ESGOTADOS = "passos_esgotados"
    CASO_ENCERRADO = "caso_encerrado"
    ORCAMENTO_ESTOURADO = "orcamento_estourado"
    ERRO_INTERNO = "erro_interno"


class EventoDePartida(ModeloBase, frozen=True):
    seq: int
    tipo: TipoEvento
    instante: AwareDatetime
    ator_id: PersonagemId | None = None
    acao: TipoAcao | None = None
    detalhe: str = ""
