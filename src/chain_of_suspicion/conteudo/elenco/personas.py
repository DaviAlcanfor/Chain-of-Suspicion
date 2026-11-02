from enum import StrEnum

from pydantic import Field

from ...dominio.base import ModeloBase
from .aparencia import Aparencia


class ChavePersona(StrEnum):
    MARTA = "marta"
    PAULO = "paulo"
    LIA = "lia"
    CAIO = "caio"
    ALENCAR = "alencar"
    OTAVIO = "otavio"
    HELENA = "helena"
    RENATO = "renato"
    BEATRIZ = "beatriz"
    JOAQUIM = "joaquim"
    VERA = "vera"
    DAVI = "davi"


class Traco(StrEnum):
    CALMO = "calmo"
    NERVOSO = "nervoso"
    CONTROLADOR = "controlador"
    CALOROSO = "caloroso"
    DESCONFIADO = "desconfiado"
    CHARMOSO = "charmoso"
    IRRESPONSAVEL = "irresponsavel"
    METODICO = "metodico"
    CURIOSO = "curioso"
    DISCRETO = "discreto"
    DRAMATICO = "dramatico"
    IRONICO = "ironico"
    ORGULHOSO = "orgulhoso"
    GENEROSO = "generoso"
    AMBICIOSO = "ambicioso"
    LEAL = "leal"
    OBSERVADOR = "observador"
    TAGARELA = "tagarela"
    RESERVADO = "reservado"
    IMPULSIVO = "impulsivo"
    AUTORITARIO = "autoritario"


class Persona(ModeloBase, frozen=True):
    chave: ChavePersona
    nome: str
    nome_completo: str
    profissao: str
    tracos: list[Traco] = Field(min_length=2)
    personalidade: str
    jeito_de_falar: str
    manias: list[str]
    aparencia: Aparencia

    @property
    def modelo_godot(self) -> str:
        return f"res://personagens/{self.chave.value}.tscn"

    def ficha(self) -> str:
        return (
            f"{self.nome_completo}, {self.profissao}. "
            f"Personalidade: {self.personalidade} "
            f"Jeito de falar: {self.jeito_de_falar} "
            f"Manias: {'; '.join(self.manias)}."
        )
