from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from caso_exemplo import (
    ALVES,
    BIBLIOTECA,
    CASO,
    COZINHA,
    ESCRITORIO,
    F_BIBLIO,
    F_CARTA,
    F_DIVIDA,
    JARDIM,
    LIA,
    MARTA,
    P_CAMERA,
    P_COPO,
    PAULO,
    hora,
    janela,
    variar,
)
from jogo.caso import Alibi, Crime, Objetivo, Personagem, Presenca
from jogo.enums import MetodoCrime, Papel, TipoObjetivo
from jogo.ids import GeradorIds


def _paulo_assassino():
    paulo = CASO.personagem(PAULO).model_copy(
        update={
            "papel": Papel.ASSASSINO,
            "objetivo": Objetivo(tipo=TipoObjetivo.EVITAR_ACUSACAO),
        }
    )
    return [paulo if p.id == PAULO else p for p in CASO.personagens]


def test_caso_valido_carrega():
    assert CASO.culpado_id == MARTA


def test_consultas_de_presenca():
    assert CASO.estava_em(MARTA, BIBLIOTECA, hora("22:10"))
    assert not CASO.estava_em(MARTA, BIBLIOTECA, hora("21:40"))
    assert CASO.presentes_em(BIBLIOTECA, hora("22:10")) == {MARTA, ALVES}


def test_pista_que_exige_pista_inexistente():
    pista = CASO.pistas[1].model_copy(update={"exige_pistas": [GeradorIds(1).pista()]})
    with pytest.raises(ValidationError, match="exige pista inexistente"):
        variar(pistas=[CASO.pistas[0], pista, *CASO.pistas[2:]])


def test_pistas_que_dependem_uma_da_outra_ficam_inalcancaveis():
    copo = CASO.pistas[0].model_copy(update={"exige_pistas": [P_CAMERA]})
    with pytest.raises(ValidationError, match="inalcançáveis"):
        variar(pistas=[copo, *CASO.pistas[1:]])


def test_dois_assassinos():
    with pytest.raises(ValidationError, match="exatamente um assassino"):
        variar(personagens=_paulo_assassino())


def test_sem_detetive():
    sem_detetive = [p for p in CASO.personagens if p.papel != Papel.DETETIVE]
    with pytest.raises(ValidationError, match="exatamente um detetive"):
        variar(personagens=sem_detetive)


def test_objetivo_incompativel_com_o_papel():
    with pytest.raises(ValidationError, match="incompatível"):
        Personagem(
            id=MARTA,
            nome="Marta",
            papel=Papel.ASSASSINO,
            objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
        )


def test_proteger_segredo_exige_fato():
    with pytest.raises(ValidationError, match="exige o fato"):
        Objetivo(tipo=TipoObjetivo.PROTEGER_SEGREDO)


def test_fato_da_cadeia_sem_pista_relevante():
    with pytest.raises(ValidationError, match="sem nenhuma pista relevante"):
        variar(cadeia_solucao=[*CASO.cadeia_solucao, F_CARTA])


def test_segredo_de_algo_que_nao_sabe():
    marta = CASO.personagem(MARTA).model_copy(update={"sabe": {F_DIVIDA}})
    personagens = [marta if p.id == MARTA else p for p in CASO.personagens]
    with pytest.raises(ValidationError, match="guarda segredo que não sabe"):
        variar(personagens=personagens)


def test_personagem_em_dois_lugares_ao_mesmo_tempo():
    duplicada = Presenca(personagem_id=MARTA, local_id=COZINHA, periodo=janela("22:00", "22:20"))
    with pytest.raises(ValidationError, match="dois lugares ao mesmo tempo"):
        variar(agenda=[*CASO.agenda, duplicada])


def test_personagem_sem_tempo_de_deslocamento():
    agenda = [p for p in CASO.agenda if p.personagem_id != LIA]
    agenda += [
        Presenca(personagem_id=LIA, local_id=COZINHA, periodo=janela("21:30", "22:00")),
        Presenca(personagem_id=LIA, local_id=ESCRITORIO, periodo=janela("22:00", "22:30")),
    ]
    with pytest.raises(ValidationError, match="não tem tempo de ir de Cozinha para Escritório"):
        variar(agenda=agenda)


def test_personagem_sem_agenda():
    agenda = [p for p in CASO.agenda if p.personagem_id != LIA]
    with pytest.raises(ValidationError, match="Lia está sem agenda"):
        variar(agenda=agenda)


def test_assassino_fora_do_local_do_crime():
    crime = CASO.crime.model_copy(update={"local_id": JARDIM})
    with pytest.raises(ValidationError, match="no local do crime"):
        variar(crime=crime)


def test_alibi_falso_sem_fato_que_o_desminta():
    marta = CASO.alibis[0].model_copy(update={"desmentido_por": []})
    with pytest.raises(ValidationError, match="sem fato que o desminta"):
        variar(alibis=[marta, *CASO.alibis[1:]])


def test_alibi_verdadeiro_nao_pode_ser_desmentido():
    lia = Alibi(
        personagem_id=LIA,
        local_id=COZINHA,
        periodo=janela("21:30", "22:30"),
        desmentido_por=[F_BIBLIO],
    )
    with pytest.raises(ValidationError, match="não pode ser desmentido"):
        variar(alibis=[*CASO.alibis[:2], lia])


def test_instante_sem_fuso_e_rejeitado():
    with pytest.raises(ValidationError):
        Crime(
            vitima_id=ALVES,
            instante=datetime(2026, 10, 30, 22, 10),
            local_id=BIBLIOTECA,
            metodo=MetodoCrime.ARMA_BRANCA,
            motivo_fato_id=F_DIVIDA,
        )


def test_instante_com_fuso_e_aceito():
    crime = Crime(
        vitima_id=ALVES,
        instante=datetime(2026, 10, 30, 22, 10, tzinfo=UTC),
        local_id=BIBLIOTECA,
        metodo=MetodoCrime.ARMA_BRANCA,
        motivo_fato_id=F_DIVIDA,
    )
    assert crime.instante.tzinfo is not None


def test_provas_minimas_insuficientes():
    condicao = CASO.condicao_acerto.model_copy(update={"provas_minimas": [P_COPO]})
    with pytest.raises(ValidationError, match="provas mínimas inválidas"):
        variar(condicao_acerto=condicao)
