import pytest

from caso_exemplo import (
    ALVES,
    CASO,
    F_DIVIDA,
    LIA,
    MARTA,
    P_CAMERA,
    P_COPO,
    P_EXTRATO,
    PAULO,
)
from jogo.enums import TipoPressao
from jogo.regras import (
    Acusacao,
    EstadoJogador,
    JuizDeterministico,
    Pressao,
    aplicar_pressao,
    visao_do_personagem,
)

CONFRONTO = Pressao(tipo=TipoPressao.CONFRONTAR_PROVA, prova_id=P_COPO)
AMEACA_ALTA = 0.9


@pytest.fixture
def marta():
    return CASO.personagem(MARTA).model_copy(deep=True)


def test_visao_do_personagem_nao_vaza_fatos_alheios():
    visao = visao_do_personagem(CASO, PAULO).model_dump_json()
    assert "devia dinheiro" not in visao
    assert "entrou na biblioteca" not in visao
    assert "Paulo escondeu uma carta" in visao


def test_visao_traz_onde_o_personagem_esteve_e_o_alibi():
    visao = visao_do_personagem(CASO, MARTA)
    assert visao.onde_estive == [
        "Quarto, de dia 1, 21:30 (noite) até dia 1, 21:50 (noite)",
        "Biblioteca, de dia 1, 21:55 (noite) até dia 1, 22:30 (noite)",
    ]
    assert visao.alibi_declarado == "Quarto, de dia 1, 21:35 (noite) até dia 1, 22:20 (noite)"


def test_visao_de_quem_nao_declarou_alibi():
    assert visao_do_personagem(CASO, ALVES).alibi_declarado is None


def test_pressao_sobe_o_estresse_sem_soltar_segredo_antes_do_limite(marta):
    assert aplicar_pressao(marta, CONFRONTO, AMEACA_ALTA) is None
    assert marta.estresse == pytest.approx(0.45)


def test_segredo_se_solta_depois_do_limite_com_a_prova_certa(marta):
    liberados = [aplicar_pressao(marta, CONFRONTO, AMEACA_ALTA) for _ in range(4)]
    assert liberados[:3] == [None, None, None]
    assert liberados[3] is not None
    assert marta.estresse >= marta.limite_estresse


def test_prova_errada_nao_solta_o_segredo(marta):
    errada = Pressao(tipo=TipoPressao.CONFRONTAR_PROVA, prova_id=P_EXTRATO)
    assert all(aplicar_pressao(marta, errada, AMEACA_ALTA) is None for _ in range(6))


def test_decision_model_inseguro_nao_muda_nada(marta):
    aplicar_pressao(marta, CONFRONTO, 0.5)
    aplicar_pressao(marta, CONFRONTO, 0.6)
    assert marta.estresse == 0.0


def test_insistir_demais_trava_o_personagem(marta):
    insistir = Pressao(tipo=TipoPressao.INSISTIR)
    for _ in range(3):
        aplicar_pressao(marta, insistir, AMEACA_ALTA)
    assert not marta.hostil
    aplicar_pressao(marta, insistir, AMEACA_ALTA)
    assert marta.hostil


def test_outra_pressao_zera_a_contagem_de_insistencia(marta):
    insistir = Pressao(tipo=TipoPressao.INSISTIR)
    for _ in range(3):
        aplicar_pressao(marta, insistir, AMEACA_ALTA)
    aplicar_pressao(marta, CONFRONTO, AMEACA_ALTA)
    aplicar_pressao(marta, insistir, AMEACA_ALTA)
    assert not marta.hostil


def test_personagem_hostil_nao_solta_nada(marta):
    marta.hostil = True
    marta.estresse = 10.0
    assert aplicar_pressao(marta, CONFRONTO, AMEACA_ALTA) is None


def _acusacao(**mudancas) -> Acusacao:
    base = Acusacao(culpado_id=MARTA, motivo_fato_id=F_DIVIDA, provas=[P_EXTRATO, P_CAMERA])
    return base.model_copy(update=mudancas)


ESTADO_COMPLETO = EstadoJogador(pistas={P_EXTRATO, P_CAMERA, P_COPO})
JUIZ = JuizDeterministico()


def test_juiz_aceita_acusacao_correta():
    assert JUIZ.julgar(CASO, ESTADO_COMPLETO, _acusacao()).correta


def test_juiz_recusa_culpado_errado():
    assert not JUIZ.julgar(CASO, ESTADO_COMPLETO, _acusacao(culpado_id=LIA)).correta


def test_juiz_recusa_motivo_errado():
    errada = _acusacao(motivo_fato_id=CASO.fatos[1].id)
    assert not JUIZ.julgar(CASO, ESTADO_COMPLETO, errada).correta


def test_juiz_recusa_provas_insuficientes():
    assert not JUIZ.julgar(CASO, ESTADO_COMPLETO, _acusacao(provas=[P_EXTRATO])).correta


def test_juiz_recusa_prova_que_o_jogador_nao_achou():
    sem_camera = EstadoJogador(pistas={P_EXTRATO})
    assert not JUIZ.julgar(CASO, sem_camera, _acusacao()).correta


def test_juiz_nao_conta_prova_repetida_duas_vezes():
    repetida = _acusacao(provas=[P_EXTRATO, P_EXTRATO])
    assert not JUIZ.julgar(CASO, ESTADO_COMPLETO, repetida).correta
