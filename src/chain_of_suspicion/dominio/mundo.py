from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .caso import Caso
from .enums import PeriodoDoDia
from .ids import LocalId, PersonagemId
from .relogio import FabricaRelogio, Relogio


@dataclass
class Mundo:
    caso: Caso
    relogio: Relogio
    posicoes: dict[PersonagemId, LocalId] = field(default_factory=dict)
    mortos: set[PersonagemId] = field(default_factory=set)

    @property
    def dia(self) -> int:
        return self.caso.calendario.dia_do_caso(self.relogio.agora())

    @property
    def periodo(self) -> PeriodoDoDia:
        return self.caso.calendario.periodo(self.relogio.agora())

    @classmethod
    def no_instante(cls, caso: Caso, instante: datetime) -> Mundo:
        if not caso.calendario.janela.contem(instante):
            raise ValueError("instante fora dos dias do caso")
        posicoes = {
            presenca.personagem_id: presenca.local_id
            for presenca in caso.agenda
            if presenca.periodo.contem(instante)
        }
        mortos = {caso.crime.vitima_id} if instante > caso.crime.instante else set()
        return cls(caso, FabricaRelogio.simulado(instante), posicoes, mortos)

    def colocar(self, personagem_id: PersonagemId, local_id: LocalId) -> None:
        self.posicoes[personagem_id] = local_id
