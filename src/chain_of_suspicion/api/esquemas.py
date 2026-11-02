from uuid import UUID

from pydantic import Field

from ..dominio.base import ModeloBase
from ..dominio.eventos import MotivoFim
from ..servicos.partida import Partida, StatusPartida


class CriarPartida(ModeloBase):
    seed: int


class PartidaResposta(ModeloBase):
    id: UUID
    status: StatusPartida
    dia: int
    periodo: str
    motivo_fim: MotivoFim | None = None
    eventos: int = Field(ge=0)

    @classmethod
    def de(cls, partida: Partida) -> PartidaResposta:
        return cls(
            id=partida.id,
            status=partida.status,
            dia=partida.mundo.dia,
            periodo=partida.mundo.periodo.value,
            motivo_fim=partida.motivo_fim,
            eventos=len(partida.eventos),
        )


class Saude(ModeloBase):
    status: str = "ok"
