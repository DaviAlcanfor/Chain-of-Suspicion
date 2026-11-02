from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from ...dominio.acoes import Acao
from ...dominio.eventos import EventoDePartida
from ...dominio.ids import PartidaId
from ...servicos.partida import EstadoVisivel, estado_visivel
from ...servicos.partidas import ServicoDePartidas
from ..esquemas import CriarPartida, PartidaResposta

Servico = FromDishka[ServicoDePartidas]

roteador = APIRouter(prefix="/partidas", tags=["partidas"], route_class=DishkaRoute)


@roteador.post("", status_code=status.HTTP_201_CREATED)
async def criar_partida(pedido: CriarPartida, servico: Servico) -> PartidaResposta:
    return PartidaResposta.de(servico.criar(pedido.seed))


@roteador.get("/{partida_id}")
async def consultar_partida(partida_id: UUID, servico: Servico) -> PartidaResposta:
    return PartidaResposta.de(servico.obter(PartidaId(partida_id)))


@roteador.get("/{partida_id}/estado")
async def consultar_estado(partida_id: UUID, servico: Servico) -> EstadoVisivel:
    return estado_visivel(servico.obter(PartidaId(partida_id)))


@roteador.post("/{partida_id}/acoes")
async def enviar_acao(
    partida_id: UUID, acao: Acao, servico: Servico
) -> EventoDePartida:
    return await servico.agir(PartidaId(partida_id), acao)


@roteador.post("/{partida_id}/pausar")
async def pausar_partida(partida_id: UUID, servico: Servico) -> PartidaResposta:
    return PartidaResposta.de(servico.pausar(PartidaId(partida_id)))


@roteador.post("/{partida_id}/retomar")
async def retomar_partida(partida_id: UUID, servico: Servico) -> PartidaResposta:
    return PartidaResposta.de(servico.retomar(PartidaId(partida_id)))
