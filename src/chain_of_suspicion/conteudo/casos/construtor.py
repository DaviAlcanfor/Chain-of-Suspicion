from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from ...dominio.caso import Personagem, Presenca
from ...dominio.enums import Papel
from ...dominio.ids import CasoId, EventoId, FatoId, LocalId, PersonagemId, PistaId
from ...dominio.relogio import Intervalo
from ..caso_pronto import ChaveCaso, Escalado
from ..elenco import ELENCO
from ..elenco.personas import ChavePersona

FUSO = timezone(timedelta(hours=-3))
PRIMEIRO_DIA = datetime(2026, 11, 6, tzinfo=FUSO)
DIAS_DO_CASO = 3


class Ids:
    def __init__(self, caso: ChaveCaso) -> None:
        self._caso = caso

    def _uuid(self, tipo: str, nome: str) -> UUID:
        return uuid5(NAMESPACE_URL, f"chain-of-suspicion/casos/{self._caso.value}/{tipo}/{nome}")

    def caso(self) -> CasoId:
        return CasoId(self._uuid("caso", self._caso.value))

    def personagem(self, persona: ChavePersona) -> PersonagemId:
        return PersonagemId(self._uuid("personagem", persona.value))

    def fato(self, nome: str) -> FatoId:
        return FatoId(self._uuid("fato", nome))

    def pista(self, nome: str) -> PistaId:
        return PistaId(self._uuid("pista", nome))

    def evento(self, nome: str) -> EventoId:
        return EventoId(self._uuid("evento", nome))


def hora(texto: str, dia: int = 1) -> datetime:
    horas, minutos = map(int, texto.split(":"))
    return PRIMEIRO_DIA + timedelta(days=dia - 1, hours=horas, minutes=minutos)


def periodo(de: str, ate: str, dia: int = 1) -> Intervalo:
    return Intervalo(inicio=hora(de, dia), fim=hora(ate, dia))


def noite_adentro(de: str, ate: str) -> Intervalo:
    return Intervalo(inicio=hora(de, 1), fim=hora(ate, 2))


def ator(ids: Ids, persona: ChavePersona, papel: Papel, **extra: Any) -> Personagem:
    return Personagem(id=ids.personagem(persona), nome=ELENCO[persona].nome, papel=papel, **extra)


def estadia(pessoa: PersonagemId, local: LocalId, intervalo: Intervalo) -> Presenca:
    return Presenca(personagem_id=pessoa, local_id=local, periodo=intervalo)


def escalar(persona: ChavePersona, funcao: str) -> Escalado:
    return Escalado(persona=persona, funcao=funcao)
