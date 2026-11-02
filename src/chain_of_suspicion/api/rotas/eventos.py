from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from ...dominio.ids import PartidaId
from ...erros.excecoes import PartidaNaoEncontrada
from ...servicos.partidas import ServicoDePartidas

roteador = APIRouter(tags=["eventos"])

CODIGO_PARTIDA_NAO_ENCONTRADA = 4404


@roteador.websocket("/partidas/{partida_id}/eventos")
@inject
async def transmitir_eventos(
    websocket: WebSocket,
    partida_id: UUID,
    servico: FromDishka[ServicoDePartidas],
    ultimo_evento: int = Query(default=-1, ge=-1),
) -> None:
    id_ = PartidaId(partida_id)
    try:
        servico.obter(id_)
    except PartidaNaoEncontrada:
        await websocket.close(code=CODIGO_PARTIDA_NAO_ENCONTRADA)
        return
    await websocket.accept()
    try:
        while novos := await servico.eventos_apos(id_, ultimo_evento):
            for evento in novos:
                await websocket.send_json(evento.model_dump(mode="json"))
                ultimo_evento = evento.seq
        await websocket.close()
    except WebSocketDisconnect:
        return
