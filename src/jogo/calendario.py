from __future__ import annotations

from datetime import datetime, time, timedelta

from pydantic import AwareDatetime, ConfigDict, Field, model_validator

from .base import ModeloBase
from .enums import PeriodoDoDia
from .relogio import Intervalo

MEIO_DIA = time(12, 0)
PERIODOS_ESCUROS = frozenset({PeriodoDoDia.MADRUGADA, PeriodoDoDia.NOITE})


class Calendario(ModeloBase):
    model_config = ConfigDict(frozen=True)

    inicio: AwareDatetime
    dias: int = Field(ge=1)
    nascer_do_sol: time = time(6, 0)
    por_do_sol: time = time(18, 0)

    @model_validator(mode="after")
    def _sol_em_ordem(self) -> Calendario:
        if not self.nascer_do_sol < MEIO_DIA < self.por_do_sol:
            raise ValueError("o sol nasce antes do meio-dia e se põe depois dele")
        return self

    @property
    def janela(self) -> Intervalo:
        primeira_meia_noite = self._meia_noite(self.inicio)
        return Intervalo(
            inicio=primeira_meia_noite,
            fim=primeira_meia_noite + timedelta(days=self.dias),
        )

    def dia_do_caso(self, instante: datetime) -> int:
        local = instante.astimezone(self.inicio.tzinfo)
        return (local.date() - self.inicio.date()).days + 1

    def inicio_do_dia(self, dia: int) -> datetime:
        if not 1 <= dia <= self.dias:
            raise ValueError(f"o caso tem {self.dias} dias, não existe o dia {dia}")
        return self._meia_noite(self.inicio) + timedelta(days=dia - 1)

    def periodo(self, instante: datetime) -> PeriodoDoDia:
        hora = instante.astimezone(self.inicio.tzinfo).time()
        if hora < self.nascer_do_sol:
            return PeriodoDoDia.MADRUGADA
        if hora < MEIO_DIA:
            return PeriodoDoDia.MANHA
        if hora < self.por_do_sol:
            return PeriodoDoDia.TARDE
        return PeriodoDoDia.NOITE

    def eh_noite(self, instante: datetime) -> bool:
        return self.periodo(instante) in PERIODOS_ESCUROS

    def descrever(self, instante: datetime) -> str:
        hora = instante.astimezone(self.inicio.tzinfo)
        return f"dia {self.dia_do_caso(instante)}, {hora:%H:%M} ({self.periodo(instante)})"

    @staticmethod
    def _meia_noite(instante: datetime) -> datetime:
        return instante.replace(hour=0, minute=0, second=0, microsecond=0)
