from typing import Any

from langgraph.runtime import Runtime

from ...dominio.acoes import AcaoInvalida
from ...dominio.acoes import aplicar_acao as aplicar_no_mundo
from ...dominio.enums import TipoAcao
from ...dominio.eventos import MotivoFim, TipoEvento
from ...dominio.ids import PersonagemId
from ...dominio.regras import visao_do_personagem
from ...erros.excecoes import FalhaNoLLM, OrcamentoEstourado
from ..contexto import montar_contexto
from ..emissor import Rascunho, emitir
from ..estado import ContextoDaPartida, EstadoPartida
from ..turno import PropostaDoAgente, montar_acao

ESPERAR = PropostaDoAgente(tipo=TipoAcao.ESPERAR)


async def decidir_acao(
    estado: EstadoPartida, runtime: Runtime[ContextoDaPartida]
) -> dict[str, Any]:
    ator_id = _ator(estado)
    mundo = estado["mundo"]
    visao = visao_do_personagem(mundo.caso, ator_id)
    contexto = montar_contexto(mundo, ator_id, estado["recusa"])
    try:
        proposta = await runtime.context.agentes[ator_id].decidir(visao, contexto)
    except OrcamentoEstourado:
        return _encerrar_por_orcamento(estado)
    except FalhaNoLLM as erro:
        rascunho = Rascunho(TipoEvento.ESPERA_FORCADA, ator_id, TipoAcao.ESPERAR, str(erro.codigo))
        return {"proposta": ESPERAR, "eventos": emitir(estado, rascunho)}
    return {"proposta": proposta}


def aplicar_proposta(estado: EstadoPartida, runtime: Runtime[ContextoDaPartida]) -> dict[str, Any]:
    ator_id = _ator(estado)
    proposta = estado["proposta"] or ESPERAR
    mundo = estado["mundo"]
    try:
        acao = montar_acao(ator_id, proposta, montar_contexto(mundo, ator_id))
        aplicar_no_mundo(mundo, acao)
    except AcaoInvalida as erro:
        return _recusar(estado, str(erro), runtime.context.limites.tentativas_por_acao)
    rascunhos = [Rascunho(TipoEvento.ACAO_APLICADA, ator_id, acao.tipo)]
    if proposta.fala:
        rascunhos.append(Rascunho(TipoEvento.FALA, ator_id, detalhe=proposta.fala))
    return {"eventos": emitir(estado, *rascunhos), "recusa": None}


def _recusar(estado: EstadoPartida, motivo: str, tentativas_maximas: int) -> dict[str, Any]:
    ator_id = _ator(estado)
    tentativas = estado["tentativas"] + 1
    rascunhos = [Rascunho(TipoEvento.ACAO_RECUSADA, ator_id, detalhe=motivo)]
    if tentativas <= tentativas_maximas:
        eventos = emitir(estado, *rascunhos)
        return {"eventos": eventos, "recusa": motivo, "tentativas": tentativas}
    rascunhos.append(Rascunho(TipoEvento.ESPERA_FORCADA, ator_id, TipoAcao.ESPERAR, motivo))
    return {"eventos": emitir(estado, *rascunhos), "recusa": None}


def _ator(estado: EstadoPartida) -> PersonagemId:
    ator_id = estado["vez"]
    if ator_id is None:
        raise AssertionError("nó de ação chamado sem personagem da vez")
    return ator_id


def _encerrar_por_orcamento(estado: EstadoPartida) -> dict[str, Any]:
    motivo = MotivoFim.ORCAMENTO_ESTOURADO
    encerramento = Rascunho(TipoEvento.PARTIDA_ENCERRADA, detalhe=motivo.value)
    return {"fim": motivo, "eventos": emitir(estado, encerramento)}
