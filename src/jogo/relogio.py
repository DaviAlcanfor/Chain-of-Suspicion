from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Protocol

from pydantic import AwareDatetime, ConfigDict, model_validator

from .base import ModeloBase

FORMATO_INSTANTE = "%d/%m %H:%M"


def formatar_instante(instante: datetime) -> str:
    return instante.strftime(FORMATO_INSTANTE)


def _exigir_fuso(instante: datetime) -> None:
    if instante.tzinfo is None:
        raise ValueError("o instante precisa ter fuso horário")


class Relogio(Protocol):
    def agora(self) -> datetime: ...


class RelogioReal:
    def agora(self) -> datetime:
        return datetime.now(UTC)


class RelogioSimulado:
    def __init__(self, inicio: datetime) -> None:
        _exigir_fuso(inicio)
        self._agora = inicio

    def agora(self) -> datetime:
        return self._agora

    def avancar(self, delta: timedelta) -> datetime:
        if delta <= timedelta(0):
            raise ValueError("o relógio simulado só avança")
        self._agora += delta
        return self._agora


class FabricaRelogio:
    @staticmethod
    def real() -> RelogioReal:
        return RelogioReal()

    @staticmethod
    def simulado(inicio: datetime) -> RelogioSimulado:
        return RelogioSimulado(inicio)


class Intervalo(ModeloBase):
    model_config = ConfigDict(frozen=True)

    inicio: AwareDatetime
    fim: AwareDatetime

    @model_validator(mode="after")
    def _fim_depois_do_inicio(self) -> Intervalo:
        if self.fim <= self.inicio:
            raise ValueError("o fim precisa ser depois do início")
        return self

    @property
    def duracao(self) -> timedelta:
        return self.fim - self.inicio

    def contem(self, instante: datetime) -> bool:
        return self.inicio <= instante < self.fim

    def cobre(self, outro: Intervalo) -> bool:
        return self.inicio <= outro.inicio and outro.fim <= self.fim

    def sobrepoe(self, outro: Intervalo) -> bool:
        return self.inicio < outro.fim and outro.inicio < self.fim
