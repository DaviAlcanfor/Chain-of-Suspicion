import pytest

from ajudas import VENENO, FabricaFalsa, pessoa, settings_de_teste
from chain_of_suspicion.agentes.agente import Agente, AgenteFalso
from chain_of_suspicion.agentes.grafo import construir_grafo, executar
from chain_of_suspicion.agentes.turno import PropostaDoAgente
from chain_of_suspicion.conteudo.caso_pronto import ChaveCaso
from chain_of_suspicion.dominio.enums import Papel, TipoAcao
from chain_of_suspicion.dominio.eventos import EventoDePartida, MotivoFim, TipoEvento
from chain_of_suspicion.dominio.mundo import Mundo
from chain_of_suspicion.erros.excecoes import OrcamentoEstourado, TempoEsgotadoNoLLM
from chain_of_suspicion.servicos.casos import CatalogoDeCasos
from chain_of_suspicion.servicos.montador import MontadorDePartida

MARTA = pessoa(VENENO, "Marta")
GRAFO = construir_grafo()


def _montador(**jogo: int) -> MontadorDePartida:
    padrao = {"passos_por_partida": 3, "tentativas_por_acao": 1, **jogo}
    return MontadorDePartida(CatalogoDeCasos(), FabricaFalsa(), settings_de_teste(**padrao).game)


async def _rodar(marta: Agente | None = None, **jogo: int) -> tuple[list[EventoDePartida], Mundo]:
    partida = _montador(**jogo).montar(seed=0)
    if marta is not None:
        partida.contexto.agentes[MARTA] = marta  # type: ignore[index]
    eventos = [e async for e in executar(GRAFO, partida.mundo, partida.contexto)]
    return eventos, partida.mundo


@pytest.mark.parametrize("chave", list(ChaveCaso), ids=lambda c: c.value)
async def test_partida_completa_em_cada_caso_com_o_detetive_agindo(chave: ChaveCaso) -> None:
    seed = list(ChaveCaso).index(chave)
    partida = _montador().montar(seed)
    eventos = [e async for e in executar(GRAFO, partida.mundo, partida.contexto)]
    detetive = next(p.id for p in partida.mundo.caso.personagens if p.papel == Papel.DETETIVE)
    assert eventos[-1].tipo == TipoEvento.PARTIDA_ENCERRADA
    assert eventos[-1].detalhe == MotivoFim.PASSOS_ESGOTADOS
    assert any(e.ator_id == detetive and e.tipo == TipoEvento.ACAO_APLICADA for e in eventos)
    assert [e.seq for e in eventos] == list(range(len(eventos)))


async def test_fala_vira_evento_separado() -> None:
    falante = AgenteFalso(PropostaDoAgente(tipo=TipoAcao.ESPERAR, fala="boa noite"))
    eventos, _ = await _rodar(falante)
    falas = [e for e in eventos if e.tipo == TipoEvento.FALA]
    assert falas
    assert falas[0].ator_id == MARTA
    assert falas[0].detalhe == "boa noite"


async def test_acao_invalida_nunca_altera_o_mundo_e_vira_espera() -> None:
    invalida = AgenteFalso(PropostaDoAgente(tipo=TipoAcao.MOVER, alvo_local="Lugar Nenhum"))
    antes = _montador().montar(seed=0).mundo.posicoes
    eventos, mundo = await _rodar(invalida)
    assert mundo.posicoes == antes
    recusas = [e for e in eventos if e.ator_id == MARTA and e.tipo == TipoEvento.ACAO_RECUSADA]
    assert len(recusas) == 2 * 3
    assert TipoEvento.ESPERA_FORCADA in [e.tipo for e in eventos]


async def test_timeout_do_llm_vira_esperar() -> None:
    eventos, _ = await _rodar(AgenteFalso(TempoEsgotadoNoLLM("lento")))
    forcadas = [e for e in eventos if e.tipo == TipoEvento.ESPERA_FORCADA]
    assert forcadas
    assert forcadas[0].detalhe == "tempo_esgotado_no_llm"
    assert eventos[-1].detalhe == MotivoFim.PASSOS_ESGOTADOS


async def test_orcamento_estourado_encerra_a_partida() -> None:
    eventos, _ = await _rodar(AgenteFalso(OrcamentoEstourado("teto")))
    assert eventos[-1].tipo == TipoEvento.PARTIDA_ENCERRADA
    assert eventos[-1].detalhe == MotivoFim.ORCAMENTO_ESTOURADO


async def test_partida_acaba_quando_o_caso_acaba() -> None:
    partida = _montador(passos_por_partida=1000, passo_em_minutos=600).montar(seed=0)
    eventos = [e async for e in executar(GRAFO, partida.mundo, partida.contexto)]
    assert eventos[-1].detalhe == MotivoFim.CASO_ENCERRADO
