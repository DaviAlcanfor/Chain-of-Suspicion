from datetime import time, timedelta

import pytest

from caso_exemplo import (
    BIBLIOTECA,
    CAIO,
    CASO,
    COZINHA,
    DIAS_DO_CASO,
    ESCRITORIO,
    JARDIM,
    LIA,
    PRIMEIRO_DIA,
    hora,
    variar,
)
from jogo.calendario import Calendario
from jogo.caso import Presenca
from jogo.enums import PeriodoDoDia
from jogo.mundo import Mundo
from jogo.relogio import Intervalo

CALENDARIO = CASO.calendario


def _presenca(personagem_id, local_id, dia_de, de, dia_ate, ate) -> Presenca:
    periodo = Intervalo(inicio=hora(de, dia_de), fim=hora(ate, dia_ate))
    return Presenca(personagem_id=personagem_id, local_id=local_id, periodo=periodo)


def _com_agenda_extra(*extras: Presenca):
    return variar(agenda=[*CASO.agenda, *extras])


def test_dia_do_caso_conta_a_partir_de_um():
    assert CALENDARIO.dia_do_caso(hora("10:00", dia=1)) == 1
    assert CALENDARIO.dia_do_caso(hora("00:00", dia=2)) == 2
    assert CALENDARIO.dia_do_caso(hora("23:59", dia=3)) == 3


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("00:00", PeriodoDoDia.MADRUGADA),
        ("05:59", PeriodoDoDia.MADRUGADA),
        ("06:00", PeriodoDoDia.MANHA),
        ("11:59", PeriodoDoDia.MANHA),
        ("12:00", PeriodoDoDia.TARDE),
        ("17:59", PeriodoDoDia.TARDE),
        ("18:00", PeriodoDoDia.NOITE),
        ("23:59", PeriodoDoDia.NOITE),
    ],
)
def test_periodo_do_dia_nas_fronteiras(texto, esperado):
    assert CALENDARIO.periodo(hora(texto)) == esperado


def test_noite_e_madrugada_sao_escuras():
    assert CALENDARIO.eh_noite(hora("02:00"))
    assert CALENDARIO.eh_noite(hora("22:10"))
    assert not CALENDARIO.eh_noite(hora("14:00"))


def test_sol_configuravel_muda_o_periodo():
    inverno = Calendario(
        inicio=PRIMEIRO_DIA, dias=2, nascer_do_sol=time(7, 0), por_do_sol=time(17, 0)
    )
    assert inverno.periodo(hora("06:30")) == PeriodoDoDia.MADRUGADA
    assert inverno.periodo(hora("17:30")) == PeriodoDoDia.NOITE


def test_sol_fora_de_ordem_e_recusado():
    with pytest.raises(ValueError, match="sol nasce"):
        Calendario(inicio=PRIMEIRO_DIA, dias=1, nascer_do_sol=time(13, 0))


def test_calendario_precisa_de_ao_menos_um_dia():
    with pytest.raises(ValueError):
        Calendario(inicio=PRIMEIRO_DIA, dias=0)


def test_janela_cobre_todos_os_dias_do_caso():
    janela = CALENDARIO.janela
    assert janela.inicio == PRIMEIRO_DIA
    assert janela.duracao == timedelta(days=DIAS_DO_CASO)
    assert janela.contem(hora("23:59", dia=DIAS_DO_CASO))
    assert not janela.contem(hora("00:00", dia=DIAS_DO_CASO + 1))


def test_inicio_do_dia_e_limites():
    assert CALENDARIO.inicio_do_dia(2) == hora("00:00", dia=2)
    with pytest.raises(ValueError, match="não existe o dia"):
        CALENDARIO.inicio_do_dia(DIAS_DO_CASO + 1)


def test_descrever_mostra_dia_hora_e_periodo():
    assert CALENDARIO.descrever(hora("22:10")) == "dia 1, 22:10 (noite)"
    assert CALENDARIO.descrever(hora("08:05", dia=2)) == "dia 2, 08:05 (manha)"


def test_caso_aceita_agenda_em_varios_dias():
    caso = _com_agenda_extra(
        _presenca(LIA, ESCRITORIO, 2, "08:00", 2, "09:00"),
        _presenca(CAIO, JARDIM, 2, "14:00", 3, "09:00"),
    )
    assert len(caso.agenda) == len(CASO.agenda) + 2


def test_deslocamento_vale_atraves_da_meia_noite():
    cedo_demais = _presenca(LIA, BIBLIOTECA, 1, "22:31", 1, "23:00")
    with pytest.raises(ValueError, match="não tem tempo"):
        _com_agenda_extra(cedo_demais)


def test_sobreposicao_vale_entre_dias():
    with pytest.raises(ValueError, match="dois lugares"):
        _com_agenda_extra(_presenca(LIA, COZINHA, 1, "22:00", 2, "08:00"))


def test_caso_recusa_agenda_depois_do_ultimo_dia():
    fora = _presenca(CAIO, JARDIM, DIAS_DO_CASO + 1, "08:00", DIAS_DO_CASO + 1, "09:00")
    with pytest.raises(ValueError, match="fora dos dias do caso"):
        _com_agenda_extra(fora)


def test_caso_recusa_agenda_que_termina_depois_da_janela():
    longa = _presenca(CAIO, JARDIM, 3, "20:00", 4, "01:00")
    with pytest.raises(ValueError, match="fora dos dias do caso"):
        _com_agenda_extra(longa)


def test_caso_recusa_crime_fora_do_calendario():
    crime = CASO.crime.model_copy(update={"instante": hora("22:10", dia=DIAS_DO_CASO + 1)})
    with pytest.raises(ValueError, match="fora dos dias do caso"):
        variar(crime=crime)


def test_mundo_no_segundo_dia_sabe_dia_periodo_e_morte():
    mundo = Mundo.no_instante(CASO, hora("09:00", dia=2))
    assert mundo.dia == 2
    assert mundo.periodo == PeriodoDoDia.MANHA
    assert CASO.crime.vitima_id in mundo.mortos


def test_mundo_recusa_instante_fora_do_caso():
    with pytest.raises(ValueError, match="fora dos dias do caso"):
        Mundo.no_instante(CASO, hora("00:00", dia=DIAS_DO_CASO + 1))


def test_relogio_do_mundo_vira_o_dia_a_meia_noite():
    mundo = Mundo.no_instante(CASO, hora("23:50"))
    assert (mundo.dia, mundo.periodo) == (1, PeriodoDoDia.NOITE)
    mundo.relogio.avancar(timedelta(minutes=20))
    assert (mundo.dia, mundo.periodo) == (2, PeriodoDoDia.MADRUGADA)
