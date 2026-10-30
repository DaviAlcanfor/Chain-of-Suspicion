from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from caso_exemplo import BIBLIOTECA, CASO, COZINHA, ESCRITORIO, JARDIM, hora, janela
from jogo.ids import GeradorIds
from jogo.mapa import Conexao, Local, Mapa
from jogo.relogio import FabricaRelogio, Intervalo, formatar_instante

MAPA = CASO.mapa


def test_tempo_minimo_soma_o_caminho():
    assert MAPA.tempo_minimo(ESCRITORIO, BIBLIOTECA) == timedelta(minutes=3)
    assert MAPA.tempo_minimo(JARDIM, BIBLIOTECA) == timedelta(minutes=4)
    assert MAPA.tempo_minimo(COZINHA, COZINHA) == timedelta(0)


def test_vizinhos_so_trazem_conexoes_diretas():
    assert JARDIM not in MAPA.vizinhos(BIBLIOTECA)
    assert len(MAPA.vizinhos(BIBLIOTECA)) == 1


def test_mapa_com_local_isolado_e_rejeitado():
    ids = GeradorIds(7)
    a, b, isolado = ids.local(), ids.local(), ids.local()
    with pytest.raises(ValidationError, match="isolados"):
        Mapa(
            locais=[
                Local(id=a, nome="A"),
                Local(id=b, nome="B"),
                Local(id=isolado, nome="C"),
            ],
            conexoes=[Conexao(origem=a, destino=b, tempo=timedelta(minutes=1))],
        )


def test_conexao_com_tempo_nao_positivo_e_rejeitada():
    ids = GeradorIds(8)
    a, b = ids.local(), ids.local()
    with pytest.raises(ValidationError, match="positivo"):
        Mapa(
            locais=[Local(id=a, nome="A"), Local(id=b, nome="B")],
            conexoes=[Conexao(origem=a, destino=b, tempo=timedelta(0))],
        )


def test_relogio_simulado_avanca_e_nunca_volta():
    relogio = FabricaRelogio.simulado(hora("22:00"))
    relogio.avancar(timedelta(minutes=10))
    assert relogio.agora() == hora("22:10")
    with pytest.raises(ValueError, match="só avança"):
        relogio.avancar(timedelta(minutes=-1))


def test_relogio_simulado_vira_o_dia():
    relogio = FabricaRelogio.simulado(hora("23:50"))
    relogio.avancar(timedelta(minutes=20))
    assert relogio.agora().day == 31
    assert formatar_instante(relogio.agora()) == "31/10 00:10"


def test_relogio_simulado_exige_fuso():
    with pytest.raises(ValueError, match="fuso"):
        FabricaRelogio.simulado(datetime(2026, 10, 30, 22, 0))


def test_relogio_real_tem_fuso():
    assert FabricaRelogio.real().agora().tzinfo == UTC


def test_intervalo_com_fim_antes_do_inicio():
    with pytest.raises(ValidationError, match="depois do início"):
        Intervalo(inicio=hora("22:00"), fim=hora("21:00"))


def test_intervalo_e_semiaberto():
    periodo = janela("22:00", "22:30")
    assert periodo.contem(hora("22:00"))
    assert not periodo.contem(hora("22:30"))
    assert periodo.duracao == timedelta(minutes=30)


def test_intervalos_vizinhos_nao_se_sobrepoem():
    assert not janela("22:00", "22:30").sobrepoe(janela("22:30", "23:00"))
    assert janela("22:00", "22:30").sobrepoe(janela("22:29", "23:00"))


def test_intervalo_cobre():
    assert janela("21:00", "23:00").cobre(janela("22:00", "22:30"))
    assert not janela("22:00", "22:30").cobre(janela("21:00", "23:00"))
