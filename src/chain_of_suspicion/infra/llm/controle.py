import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from ...config.modelos_llm import Modelo
from ...config.precos import PRECO_DO_MODELO, SEM_PRECO
from ...erros.excecoes import OrcamentoEstourado

UM_MILHAO = 1_000_000


class ControleDeUso:
    def __init__(self, simultaneas: int, teto_usd: float) -> None:
        self._semaforo = asyncio.Semaphore(simultaneas)
        self._teto = teto_usd
        self.custo_usd = 0.0
        self.tokens_entrada = 0
        self.tokens_saida = 0

    @asynccontextmanager
    async def vaga(self) -> AsyncIterator[None]:
        if self.custo_usd >= self._teto:
            raise OrcamentoEstourado("o teto de custo da partida foi atingido")
        async with self._semaforo:
            yield

    def registrar_custo(self, usd: float, entrada: int, saida: int) -> None:
        self.tokens_entrada += entrada
        self.tokens_saida += saida
        self.custo_usd += usd

    def registrar(self, modelo: Modelo, entrada: int, saida: int) -> None:
        preco = PRECO_DO_MODELO.get(modelo, SEM_PRECO)
        self.tokens_entrada += entrada
        self.tokens_saida += saida
        self.custo_usd += (
            entrada * preco.entrada_por_milhao + saida * preco.saida_por_milhao
        ) / UM_MILHAO
