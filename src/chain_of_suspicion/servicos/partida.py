import asyncio
from enum import StrEnum

from ..agentes.estado import ContextoDaPartida
from ..dominio.base import ModeloBase
from ..dominio.eventos import EventoDePartida, MotivoFim, TipoEvento
from ..dominio.ids import PartidaId
from ..dominio.mundo import Mundo

ULTIMAS_FALAS = 10


class StatusPartida(StrEnum):
    CRIADA = "criada"
    EM_ANDAMENTO = "em_andamento"
    PAUSADA = "pausada"
    ENCERRADA = "encerrada"


class Partida:
    def __init__(self, id: PartidaId, mundo: Mundo, contexto: ContextoDaPartida) -> None:
        self.id = id
        self.mundo = mundo
        self.contexto = contexto
        self.status = StatusPartida.CRIADA
        self.motivo_fim: MotivoFim | None = None
        self.eventos: list[EventoDePartida] = []
        self.tarefa: asyncio.Task[None] | None = None
        self.liberada = asyncio.Event()
        self._mudou = asyncio.Condition()

    async def publicar(self, evento: EventoDePartida) -> EventoDePartida:
        numerado = evento.model_copy(update={"seq": len(self.eventos)})
        async with self._mudou:
            self.eventos.append(numerado)
            self._mudou.notify_all()
        return numerado

    async def encerrar(self, motivo: MotivoFim) -> None:
        async with self._mudou:
            self.status = StatusPartida.ENCERRADA
            self.motivo_fim = motivo
            self._mudou.notify_all()

    async def eventos_apos(self, ultimo: int) -> list[EventoDePartida]:
        async with self._mudou:
            await self._mudou.wait_for(
                lambda: len(self.eventos) > ultimo + 1 or self.status == StatusPartida.ENCERRADA
            )
            return self.eventos[ultimo + 1 :]


class FalaVisivel(ModeloBase):
    personagem: str
    texto: str


class EstadoVisivel(ModeloBase):
    dia: int
    periodo: str
    posicoes: dict[str, str]
    mortos: list[str]
    ultimas_falas: list[FalaVisivel]


def estado_visivel(partida: Partida) -> EstadoVisivel:
    mundo = partida.mundo
    caso = mundo.caso
    falas = [e for e in partida.eventos if e.tipo == TipoEvento.FALA and e.ator_id is not None]
    return EstadoVisivel(
        dia=mundo.dia,
        periodo=mundo.periodo.value,
        posicoes={
            caso.personagem(personagem_id).nome: caso.mapa.nome(local_id)
            for personagem_id, local_id in mundo.posicoes.items()
        },
        mortos=sorted(caso.personagem(morto).nome for morto in mundo.mortos),
        ultimas_falas=[
            FalaVisivel(personagem=caso.personagem(e.ator_id).nome, texto=e.detalhe)
            for e in falas[-ULTIMAS_FALAS:]
            if e.ator_id is not None
        ],
    )
