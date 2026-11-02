import pytest
from pydantic import ValidationError

from caso_exemplo import (
    ALVES,
    BIBLIOTECA,
    CAIO,
    CASO,
    CORREDOR,
    ESCRITORIO,
    INSPETOR,
    JARDIM,
    LIA,
    MARTA,
    P_COPO,
    PAULO,
    hora,
)
from chain_of_suspicion.dominio.acoes import Acao, AcaoInvalida, aplicar_acao, validar_acao
from chain_of_suspicion.dominio.enums import TipoAcao
from chain_of_suspicion.dominio.mundo import Mundo


@pytest.fixture
def mundo() -> Mundo:
    mundo = Mundo.no_instante(CASO, hora("22:10"))
    mundo.colocar(INSPETOR, BIBLIOTECA)
    return mundo


def test_mundo_no_instante_do_crime_posiciona_assassino_e_vitima(mundo: Mundo):
    assert mundo.posicoes[MARTA] == BIBLIOTECA
    assert mundo.posicoes[ALVES] == BIBLIOTECA
    assert mundo.mortos == set()


def test_mundo_depois_do_crime_ja_tem_vitima_morta():
    assert Mundo.no_instante(CASO, hora("22:20")).mortos == {ALVES}


def test_assassino_mata_a_vitima_no_mesmo_local(mundo: Mundo):
    aplicar_acao(mundo, Acao(tipo=TipoAcao.MATAR, ator_id=MARTA, alvo_personagem_id=ALVES))
    assert ALVES in mundo.mortos


def test_assassino_nao_mata_de_outro_local(mundo: Mundo):
    mundo.colocar(MARTA, CORREDOR)
    acao = Acao(tipo=TipoAcao.MATAR, ator_id=MARTA, alvo_personagem_id=ALVES)
    with pytest.raises(AcaoInvalida, match="mesmo local"):
        validar_acao(mundo, acao)


def test_so_o_assassino_mata(mundo: Mundo):
    for ator in (PAULO, INSPETOR):
        acao = Acao(tipo=TipoAcao.MATAR, ator_id=ator, alvo_personagem_id=ALVES)
        with pytest.raises(AcaoInvalida, match="não pode"):
            validar_acao(mundo, acao)


def test_assassino_so_mata_a_vitima_do_caso(mundo: Mundo):
    mundo.colocar(LIA, BIBLIOTECA)
    acao = Acao(tipo=TipoAcao.MATAR, ator_id=MARTA, alvo_personagem_id=LIA)
    with pytest.raises(AcaoInvalida, match="só a vítima"):
        validar_acao(mundo, acao)


def test_nao_se_mata_quem_ja_morreu(mundo: Mundo):
    mundo.mortos.add(ALVES)
    acao = Acao(tipo=TipoAcao.MATAR, ator_id=MARTA, alvo_personagem_id=ALVES)
    with pytest.raises(AcaoInvalida, match="já morreu"):
        validar_acao(mundo, acao)


def test_vitima_nao_age(mundo: Mundo):
    acao = Acao(tipo=TipoAcao.CONVERSAR, ator_id=ALVES, alvo_personagem_id=MARTA)
    with pytest.raises(AcaoInvalida, match="não pode"):
        validar_acao(mundo, acao)


def test_mover_so_para_local_vizinho(mundo: Mundo):
    aplicar_acao(mundo, Acao(tipo=TipoAcao.MOVER, ator_id=MARTA, alvo_local_id=CORREDOR))
    assert mundo.posicoes[MARTA] == CORREDOR
    com_salto = Acao(tipo=TipoAcao.MOVER, ator_id=MARTA, alvo_local_id=JARDIM)
    with pytest.raises(AcaoInvalida, match="caminho direto"):
        validar_acao(mundo, com_salto)


def test_detetive_interroga_so_no_mesmo_local(mundo: Mundo):
    acao = Acao(tipo=TipoAcao.INTERROGAR, ator_id=INSPETOR, alvo_personagem_id=MARTA)
    validar_acao(mundo, acao)
    mundo.colocar(MARTA, CORREDOR)
    with pytest.raises(AcaoInvalida, match="mesmo local"):
        validar_acao(mundo, acao)


def test_detetive_examina_so_o_local_onde_esta(mundo: Mundo):
    examinar = Acao(tipo=TipoAcao.EXAMINAR_LOCAL, ator_id=INSPETOR, alvo_local_id=BIBLIOTECA)
    validar_acao(mundo, examinar)
    with pytest.raises(AcaoInvalida, match="no local da ação"):
        validar_acao(
            mundo,
            Acao(tipo=TipoAcao.EXAMINAR_LOCAL, ator_id=INSPETOR, alvo_local_id=ESCRITORIO),
        )


def test_inocente_nao_examina_local_nem_interroga(mundo: Mundo):
    mundo.colocar(CAIO, BIBLIOTECA)
    acao = Acao(tipo=TipoAcao.EXAMINAR_LOCAL, ator_id=CAIO, alvo_local_id=BIBLIOTECA)
    with pytest.raises(AcaoInvalida, match="não pode"):
        validar_acao(mundo, acao)


def test_assassino_esconde_evidencia_so_onde_esta(mundo: Mundo):
    acao = Acao(
        tipo=TipoAcao.ESCONDER_EVIDENCIA,
        ator_id=MARTA,
        alvo_local_id=BIBLIOTECA,
        pista_id=P_COPO,
    )
    validar_acao(mundo, acao)
    mundo.colocar(MARTA, CORREDOR)
    with pytest.raises(AcaoInvalida, match="no local da ação"):
        validar_acao(mundo, acao)


def test_personagem_fora_de_qualquer_local_nao_age(mundo: Mundo):
    del mundo.posicoes[MARTA]
    acao = Acao(tipo=TipoAcao.MOVER, ator_id=MARTA, alvo_local_id=CORREDOR)
    with pytest.raises(AcaoInvalida, match="não está em nenhum local"):
        validar_acao(mundo, acao)


def test_acao_sem_o_campo_exigido_e_rejeitada():
    with pytest.raises(ValidationError, match="alvo_personagem_id"):
        Acao(tipo=TipoAcao.MATAR, ator_id=MARTA)
    with pytest.raises(ValidationError, match="pista_id"):
        Acao(tipo=TipoAcao.APRESENTAR_PROVA, ator_id=INSPETOR, alvo_personagem_id=MARTA)
