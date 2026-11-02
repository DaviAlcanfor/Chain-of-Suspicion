from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from ..agentes.grafo import GrafoDaPartida
from .handlers import registrar_handlers
from .rotas import eventos, partidas, saude


def criar_app(container: AsyncContainer) -> FastAPI:
    @asynccontextmanager
    async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
        app.state.grafo = await container.get(GrafoDaPartida)
        yield
        await container.close()

    app = FastAPI(title="Chain of Suspicion", lifespan=ciclo_de_vida)
    setup_dishka(container, app)
    registrar_handlers(app)
    for roteador in (saude.roteador, partidas.roteador, eventos.roteador):
        app.include_router(roteador)
    return app
