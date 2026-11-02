from typing import Any

from langgraph.runtime import Runtime

from ...dominio.acoes import PERMISSOES
from ...dominio.eventos import MotivoFim, TipoEvento
from ...dominio.relogio import RelogioSimulado
from ...erros.excecoes import PartidaEmEstadoInvalido
from ..emissor import Rascunho, emitir
from ..estado import ContextoDaPartida, EstadoPartida


def iniciar_rodada(estado: EstadoPartida) -> dict[str, Any]:
    mundo = estado["mundo"]
    fila = [
        personagem.id
        for personagem in mundo.caso.personagens
        if personagem.id in mundo.posicoes
        and personagem.id not in mundo.mortos
        and PERMISSOES[personagem.papel]
    ]
    return {"fila": fila, "vez": None}


def escolher_vez(estado: EstadoPartida) -> dict[str, Any]:
    fila = estado["fila"]
    if not fila:
        return {"vez": None}
    return {"vez": fila[0], "fila": fila[1:], "tentativas": 0, "recusa": None}


def avancar_tempo(estado: EstadoPartida, runtime: Runtime[ContextoDaPartida]) -> dict[str, Any]:
    mundo = estado["mundo"]
    relogio = mundo.relogio
    if not isinstance(relogio, RelogioSimulado):
        raise PartidaEmEstadoInvalido("só o relógio simulado pode avançar")
    agora = relogio.avancar(runtime.context.limites.passo)
    restantes = estado["passos_restantes"] - 1
    fim = _motivo_do_fim(mundo.caso.calendario.janela.contem(agora), restantes)
    atualizacao: dict[str, Any] = {"passos_restantes": restantes, "fim": fim}
    if fim is not None:
        atualizacao["eventos"] = emitir(
            estado, Rascunho(TipoEvento.PARTIDA_ENCERRADA, detalhe=fim.value)
        )
    return atualizacao


def _motivo_do_fim(dentro_do_caso: bool, passos_restantes: int) -> MotivoFim | None:
    if not dentro_do_caso:
        return MotivoFim.CASO_ENCERRADO
    if passos_restantes <= 0:
        return MotivoFim.PASSOS_ESGOTADOS
    return None
