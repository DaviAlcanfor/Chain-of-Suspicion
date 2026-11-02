import asyncio
from uuid import uuid4

import pytest

from ajudas import VENENO, FabricaFalsa, pessoa, settings_de_teste
from chain_of_suspicion.agentes.agente import AgenteFalso
from chain_of_suspicion.agentes.grafo import construir_grafo
from chain_of_suspicion.dominio.acoes import Acao
from chain_of_suspicion.dominio.enums import TipoAcao
from chain_of_suspicion.dominio.eventos import MotivoFim
from chain_of_suspicion.dominio.ids import PartidaId
from chain_of_suspicion.erros.excecoes import (
    AcaoRecusada,
    PartidaEmEstadoInvalido,
    PartidaNaoEncontrada,
)
from chain_of_suspicion.servicos.casos import CatalogoDeCasos
from chain_of_suspicion.servicos.montador import MontadorDePartida
from chain_of_suspicion.servicos.partida import StatusPartida, estado_visivel
from chain_of_suspicion.servicos.partidas import ServicoDePartidas
from chain_of_suspicion.servicos.repositorio import RepositorioEmMemoria

MARTA = pessoa(VENENO, "Marta")
LIA = pessoa(VENENO, "Lia")
GRAFO = construir_grafo()


def _servico(fabrica: FabricaFalsa | None = None) -> ServicoDePartidas:
    jogo = settings_de_teste(passos_por_partida=3).game
    montador = MontadorDePartida(CatalogoDeCasos(), fabrica or FabricaFalsa(), jogo)
    return ServicoDePartidas(RepositorioEmMemoria(), montador, GRAFO)


async def test_partida_roda_em_segundo_plano_ate_encerrar() -> None:
    partida = _servico().criar(seed=0)
    assert partida.status == StatusPartida.EM_ANDAMENTO
    assert partida.tarefa is not None
    await partida.tarefa
    assert partida.status == StatusPartida.ENCERRADA
    assert partida.motivo_fim == MotivoFim.PASSOS_ESGOTADOS
    assert [e.seq for e in partida.eventos] == list(range(len(partida.eventos)))


async def test_pausa_segura_os_eventos_e_retomar_libera() -> None:
    servico = _servico()
    partida = servico.criar(seed=0)
    servico.pausar(partida.id)
    await asyncio.sleep(0.05)
    parados = len(partida.eventos)
    await asyncio.sleep(0.05)
    assert len(partida.eventos) == parados
    assert partida.status == StatusPartida.PAUSADA
    servico.retomar(partida.id)
    assert partida.tarefa is not None
    await partida.tarefa
    assert partida.status == StatusPartida.ENCERRADA


async def test_pausar_ou_retomar_partida_que_nao_permite_falha() -> None:
    servico = _servico()
    partida = servico.criar(seed=0)
    with pytest.raises(PartidaEmEstadoInvalido):
        servico.retomar(partida.id)
    assert partida.tarefa is not None
    await partida.tarefa
    with pytest.raises(PartidaEmEstadoInvalido):
        servico.pausar(partida.id)


def test_partida_inexistente() -> None:
    with pytest.raises(PartidaNaoEncontrada):
        _servico().obter(PartidaId(uuid4()))


async def test_acao_humana_proibida_e_recusada_sem_mudar_o_mundo() -> None:
    servico = _servico()
    partida = servico.criar(seed=0)
    antes = dict(partida.mundo.posicoes)
    proibida = Acao(tipo=TipoAcao.MATAR, ator_id=LIA, alvo_personagem_id=MARTA)
    with pytest.raises(AcaoRecusada):
        await servico.agir(partida.id, proibida)
    assert partida.mundo.posicoes == antes
    assert partida.tarefa is not None
    await partida.tarefa


async def test_acao_humana_valida_gera_evento_numerado() -> None:
    servico = _servico()
    partida = servico.criar(seed=0)
    destino = next(iter(partida.mundo.caso.mapa.vizinhos(partida.mundo.posicoes[MARTA])))
    evento = await servico.agir(
        partida.id, Acao(tipo=TipoAcao.MOVER, ator_id=MARTA, alvo_local_id=destino)
    )
    assert partida.mundo.posicoes[MARTA] == destino
    assert partida.eventos[evento.seq] == evento
    assert partida.tarefa is not None
    await partida.tarefa


async def test_erro_inesperado_encerra_com_erro_interno() -> None:
    servico = _servico(FabricaFalsa(AgenteFalso(RuntimeError("bug"))))
    partida = servico.criar(seed=0)
    assert partida.tarefa is not None
    await partida.tarefa
    assert partida.motivo_fim == MotivoFim.ERRO_INTERNO
    assert partida.eventos[-1].detalhe == MotivoFim.ERRO_INTERNO


async def test_eventos_apos_devolve_so_os_novos_e_termina_vazio() -> None:
    partida = _servico().criar(seed=0)
    assert partida.tarefa is not None
    await partida.tarefa
    resto = await partida.eventos_apos(2)
    assert [e.seq for e in resto] == list(range(3, len(partida.eventos)))
    assert await partida.eventos_apos(len(partida.eventos) - 1) == []


async def test_estado_visivel_nao_vaza_a_verdade_do_caso() -> None:
    partida = _servico().criar(seed=0)
    assert partida.tarefa is not None
    await partida.tarefa
    texto = estado_visivel(partida).model_dump_json().lower()
    for fato in VENENO.caso.fatos:
        assert fato.descricao.lower() not in texto
    assert "culpado" not in texto
    assert "veneno" not in texto
    assert "inspetor alencar" in texto
