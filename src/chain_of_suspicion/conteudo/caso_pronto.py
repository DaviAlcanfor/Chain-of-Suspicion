from enum import StrEnum

from pydantic import model_validator

from ..dominio.base import ModeloBase
from ..dominio.caso import Caso
from ..dominio.ids import LocalId, PersonagemId
from .elenco.personas import ChavePersona
from .mapas import MAPAS, ChaveMapa


class ChaveCaso(StrEnum):
    VENENO_NA_BIBLIOTECA = "veneno_na_biblioteca"
    O_TESTAMENTO = "o_testamento"
    A_ULTIMA_DANCA = "a_ultima_danca"
    SANGUE_NO_CONVES = "sangue_no_conves"
    NEVASCA_NA_POUSADA = "nevasca_na_pousada"


class Escalado(ModeloBase, frozen=True):
    persona: ChavePersona
    funcao: str


class CasoPronto(ModeloBase, frozen=True):
    chave: ChaveCaso
    titulo: str
    mapa: ChaveMapa
    apresentacao: str
    solucao: str
    entrada: LocalId
    escalacao: dict[PersonagemId, Escalado]
    caso: Caso

    @model_validator(mode="after")
    def _consistencia(self) -> CasoPronto:
        if set(self.escalacao) != {p.id for p in self.caso.personagens}:
            raise ValueError("a escalação precisa cobrir exatamente os personagens do caso")
        if not self.caso.mapa.existe(self.entrada):
            raise ValueError("a entrada do detetive precisa ser um local do mapa")
        if self.caso.mapa != MAPAS[self.mapa].construir():
            raise ValueError("o caso precisa usar o mapa escolhido")
        return self
