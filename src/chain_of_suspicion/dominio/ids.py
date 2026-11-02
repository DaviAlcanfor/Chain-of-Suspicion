import random
from typing import NewType
from uuid import UUID

CasoId = NewType("CasoId", UUID)
FatoId = NewType("FatoId", UUID)
EventoId = NewType("EventoId", UUID)
LocalId = NewType("LocalId", UUID)
PersonagemId = NewType("PersonagemId", UUID)
PistaId = NewType("PistaId", UUID)
PartidaId = NewType("PartidaId", UUID)


class GeradorIds:
    def __init__(self, seed: int) -> None:
        self._aleatorio = random.Random(seed)

    def _uuid(self) -> UUID:
        return UUID(int=self._aleatorio.getrandbits(128), version=4)

    def caso(self) -> CasoId:
        return CasoId(self._uuid())

    def fato(self) -> FatoId:
        return FatoId(self._uuid())

    def evento(self) -> EventoId:
        return EventoId(self._uuid())

    def local(self) -> LocalId:
        return LocalId(self._uuid())

    def personagem(self) -> PersonagemId:
        return PersonagemId(self._uuid())

    def pista(self) -> PistaId:
        return PistaId(self._uuid())
