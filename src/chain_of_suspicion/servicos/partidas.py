import asyncio
import logging

from ..agentes.grafo import GrafoDaPartida, executar
from ..dominio.acoes import Acao, AcaoInvalida, aplicar_acao
from ..dominio.eventos import EventoDePartida, MotivoFim, TipoEvento
from ..dominio.ids import PartidaId
from ..erros.excecoes import AcaoRecusada, PartidaEmEstadoInvalido
from .montador import MontadorDePartida
from .partida import Partida, StatusPartida
from .repositorio import RepositorioPartidas

logger = logging.getLogger(__name__)


class ServicoDePartidas:
    def __init__(
        self,
        repositorio: RepositorioPartidas,
        montador: MontadorDePartida,
        grafo: GrafoDaPartida,
    ) -> None:
        self._repositorio = repositorio
        self._montador = montador
        self._grafo = grafo

    def criar(self, seed: int) -> Partida:
        partida = self._montador.montar(seed)
        self._repositorio.salvar(partida)
        partida.status = StatusPartida.EM_ANDAMENTO
        partida.liberada.set()
        partida.tarefa = asyncio.create_task(self._rodar(partida))
        return partida

    def obter(self, partida_id: PartidaId) -> Partida:
        return self._repositorio.obter(partida_id)

    def pausar(self, partida_id: PartidaId) -> Partida:
        partida = self.obter(partida_id)
        _exigir(partida, StatusPartida.EM_ANDAMENTO, "só uma partida em andamento pode pausar")
        partida.liberada.clear()
        partida.status = StatusPartida.PAUSADA
        return partida

    def retomar(self, partida_id: PartidaId) -> Partida:
        partida = self.obter(partida_id)
        _exigir(partida, StatusPartida.PAUSADA, "só uma partida pausada pode retomar")
        partida.status = StatusPartida.EM_ANDAMENTO
        partida.liberada.set()
        return partida

    async def eventos_apos(self, partida_id: PartidaId, ultimo: int) -> list[EventoDePartida]:
        return await self.obter(partida_id).eventos_apos(ultimo)

    async def agir(self, partida_id: PartidaId, acao: Acao) -> EventoDePartida:
        partida = self.obter(partida_id)
        if partida.status == StatusPartida.ENCERRADA:
            raise PartidaEmEstadoInvalido("a partida já terminou")
        try:
            aplicar_acao(partida.mundo, acao)
        except AcaoInvalida as erro:
            raise AcaoRecusada(str(erro)) from erro
        evento = EventoDePartida(
            seq=0,
            tipo=TipoEvento.ACAO_APLICADA,
            instante=partida.mundo.relogio.agora(),
            ator_id=acao.ator_id,
            acao=acao.tipo,
        )
        return await partida.publicar(evento)

    async def _rodar(self, partida: Partida) -> None:
        motivo = MotivoFim.PASSOS_ESGOTADOS
        try:
            async for evento in executar(self._grafo, partida.mundo, partida.contexto):
                await partida.liberada.wait()
                publicado = await partida.publicar(evento)
                if publicado.tipo == TipoEvento.PARTIDA_ENCERRADA:
                    motivo = MotivoFim(publicado.detalhe)
        except Exception:
            logger.exception("partida %s terminou com erro", partida.id)
            motivo = MotivoFim.ERRO_INTERNO
            await partida.publicar(_evento_de_fim(partida, motivo))
        await partida.encerrar(motivo)


def _evento_de_fim(partida: Partida, motivo: MotivoFim) -> EventoDePartida:
    return EventoDePartida(
        seq=0,
        tipo=TipoEvento.PARTIDA_ENCERRADA,
        instante=partida.mundo.relogio.agora(),
        detalhe=motivo.value,
    )


def _exigir(partida: Partida, esperado: StatusPartida, mensagem: str) -> None:
    if partida.status != esperado:
        raise PartidaEmEstadoInvalido(mensagem)
