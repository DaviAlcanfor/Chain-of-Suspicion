from collections.abc import AsyncIterator, Callable
from typing import Any

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ..dominio.eventos import EventoDePartida
from ..dominio.mundo import Mundo
from .estado import ContextoDaPartida, EstadoPartida, No, NomeNo
from .nos import acao, rodada

type GrafoDaPartida = CompiledStateGraph[
    EstadoPartida, ContextoDaPartida, EstadoPartida, EstadoPartida
]
type Montagem = StateGraph[EstadoPartida, ContextoDaPartida, EstadoPartida, EstadoPartida]

PASSOS_FIXOS_POR_RODADA = 3
CHAMADAS_POR_TENTATIVA = 2


def construir_grafo() -> GrafoDaPartida:
    grafo: Montagem = StateGraph(EstadoPartida, context_schema=ContextoDaPartida)
    
    _adicionar_no(grafo, No.INICIAR_RODADA, rodada.iniciar_rodada)
    _adicionar_no(grafo, No.ESCOLHER_VEZ, rodada.escolher_vez)
    _adicionar_no(grafo, No.DECIDIR, acao.decidir_acao)
    _adicionar_no(grafo, No.APLICAR_ACAO, acao.aplicar_proposta)
    _adicionar_no(grafo, No.AVANCAR_TEMPO, rodada.avancar_tempo)
    
    grafo.add_edge(START, No.INICIAR_RODADA)
    grafo.add_edge(No.INICIAR_RODADA, No.ESCOLHER_VEZ)
    grafo.add_conditional_edges(No.ESCOLHER_VEZ, _depois_de_escolher)
    grafo.add_conditional_edges(No.DECIDIR, _depois_de_decidir)
    grafo.add_conditional_edges(No.APLICAR_ACAO, _depois_de_aplicar)
    grafo.add_conditional_edges(No.AVANCAR_TEMPO, _depois_de_avancar)
    
    return grafo.compile()


def estado_inicial(mundo: Mundo, contexto: ContextoDaPartida) -> EstadoPartida:
    return EstadoPartida(
        mundo=mundo,
        eventos=[],
        fila=[],
        vez=None,
        tentativas=0,
        proposta=None,
        recusa=None,
        passos_restantes=contexto.limites.passos,
        fim=None,
    )


async def executar(
    grafo: GrafoDaPartida, mundo: Mundo, contexto: ContextoDaPartida
) -> AsyncIterator[EventoDePartida]:
    configuracao = RunnableConfig(recursion_limit=_limite_de_recursao(mundo, contexto))
    fluxo = grafo.astream(
        estado_inicial(mundo, contexto), configuracao, context=contexto, stream_mode="updates"
    )
    async for atualizacao in fluxo:
        for saida in atualizacao.values():
            for evento in (saida or {}).get("eventos", []):
                yield evento


def _adicionar_no(grafo: Montagem, nome: NomeNo, funcao: Callable[..., Any]) -> None:
    grafo.add_node(nome, funcao)


def _limite_de_recursao(mundo: Mundo, contexto: ContextoDaPartida) -> int:
    limites = contexto.limites
    por_personagem = CHAMADAS_POR_TENTATIVA * (limites.tentativas_por_acao + 2)
    por_rodada = PASSOS_FIXOS_POR_RODADA + len(mundo.caso.personagens) * por_personagem
    return limites.passos * por_rodada + PASSOS_FIXOS_POR_RODADA


def _depois_de_escolher(estado: EstadoPartida) -> NomeNo:
    return No.AVANCAR_TEMPO if estado["vez"] is None else No.DECIDIR


def _depois_de_decidir(estado: EstadoPartida) -> NomeNo | str:
    return END if estado["fim"] else No.APLICAR_ACAO


def _depois_de_aplicar(estado: EstadoPartida) -> NomeNo:
    return No.DECIDIR if estado["recusa"] else No.ESCOLHER_VEZ


def _depois_de_avancar(estado: EstadoPartida) -> NomeNo | str:
    return END if estado["fim"] else No.INICIAR_RODADA
