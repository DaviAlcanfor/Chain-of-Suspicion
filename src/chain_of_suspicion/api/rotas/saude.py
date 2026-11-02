from fastapi import APIRouter

from ..esquemas import Saude

roteador = APIRouter(tags=["saude"])


@roteador.get("/saude")
async def saude() -> Saude:
    return Saude()
