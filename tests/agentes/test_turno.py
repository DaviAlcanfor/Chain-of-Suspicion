import pytest

from ajudas import VENENO, pessoa
from chain_of_suspicion.agentes.turno import ContextoDoTurno, PropostaDoAgente, montar_acao
from chain_of_suspicion.dominio.acoes import AcaoInvalida
from chain_of_suspicion.dominio.enums import TipoAcao

MARTA = pessoa(VENENO, "Marta")
LIA = pessoa(VENENO, "Lia")
HALL = VENENO.caso.mapa.locais[0].id


def _contexto() -> ContextoDoTurno:
    return ContextoDoTurno(
        instante="06/11 21:30",
        local_atual="Cozinha",
        presentes={"Lia": LIA},
        saidas={"Hall": HALL},
        aqui={"Cozinha": HALL},
        pistas={},
        acoes_permitidas=[TipoAcao.MOVER, TipoAcao.CONVERSAR],
    )


def test_proposta_vira_acao_com_ids_resolvidos() -> None:
    proposta = PropostaDoAgente(tipo=TipoAcao.MOVER, alvo_local="Hall")
    acao = montar_acao(MARTA, proposta, _contexto())
    assert acao.alvo_local_id == HALL
    assert acao.ator_id == MARTA


def test_nome_desconhecido_e_recusado() -> None:
    proposta = PropostaDoAgente(tipo=TipoAcao.MOVER, alvo_local="Lua")
    with pytest.raises(AcaoInvalida):
        montar_acao(MARTA, proposta, _contexto())


def test_proposta_sem_alvo_obrigatorio_e_recusada() -> None:
    with pytest.raises(AcaoInvalida):
        montar_acao(MARTA, PropostaDoAgente(tipo=TipoAcao.MOVER), _contexto())
