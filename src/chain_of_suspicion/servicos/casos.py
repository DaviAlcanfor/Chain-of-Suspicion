from typing import Protocol

from ..conteudo.caso_pronto import CasoPronto, ChaveCaso
from ..conteudo.casos import CATALOGO

ORDEM_DOS_CASOS = tuple(ChaveCaso)


class ProvedorDeCaso(Protocol):
    def caso_para(self, seed: int) -> CasoPronto: ...


class CatalogoDeCasos:
    def caso_para(self, seed: int) -> CasoPronto:
        return CATALOGO[ORDEM_DOS_CASOS[seed % len(ORDEM_DOS_CASOS)]]
