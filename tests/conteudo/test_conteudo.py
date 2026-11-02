import re
from pathlib import Path

import pytest

from chain_of_suspicion.conteudo.caso_pronto import CasoPronto, ChaveCaso
from chain_of_suspicion.conteudo.casos import CATALOGO
from chain_of_suspicion.conteudo.documentacao import gerar_tudo
from chain_of_suspicion.conteudo.elenco import ELENCO
from chain_of_suspicion.conteudo.elenco.aparencia import HEX_DA_COR, Paleta
from chain_of_suspicion.conteudo.elenco.personas import ChavePersona
from chain_of_suspicion.conteudo.mapas import MAPAS, ChaveMapa
from chain_of_suspicion.dominio.enums import Papel
from chain_of_suspicion.servicos.casos import CatalogoDeCasos

CASOS = list(CATALOGO.values())


def test_elenco_tem_as_12_personas_com_aparencia_e_modelo() -> None:
    assert set(ELENCO) == set(ChavePersona)
    assert len(ELENCO) == 12
    for persona in ELENCO.values():
        assert persona.modelo_godot == f"res://personagens/{persona.chave.value}.tscn"
        assert persona.aparencia.acessorios
        assert persona.aparencia.hex_da_roupa.startswith("#")
        assert persona.manias


def test_nomes_do_elenco_sao_unicos() -> None:
    nomes = [persona.nome for persona in ELENCO.values()]
    assert len(nomes) == len(set(nomes))


def test_tres_mapas_com_entrada_e_cenas_do_godot() -> None:
    assert set(MAPAS) == set(ChaveMapa)
    for chave, mapa in MAPAS.items():
        chaves = {local.chave for local in mapa.locais}
        assert mapa.entrada in chaves
        assert len(chaves) == len(mapa.locais) == 8
        assert all(p.de in chaves and p.para in chaves for p in mapa.passagens)
        assert all(
            local.cena_godot(chave).startswith(f"res://cenas/{chave.value}/")
            for local in mapa.locais
        )
        mapa.construir()


def test_ha_cinco_casos_distintos_em_tres_mapas() -> None:
    assert set(CATALOGO) == set(ChaveCaso)
    assert len({caso.titulo for caso in CASOS}) == 5
    assert {caso.mapa for caso in CASOS} == set(ChaveMapa)


@pytest.mark.parametrize("pronto", CASOS, ids=lambda c: c.chave.value)
def test_caso_tem_um_culpado_um_detetive_uma_vitima_e_inocentes(pronto: CasoPronto) -> None:
    caso = pronto.caso
    papeis = [p.papel for p in caso.personagens]
    assert papeis.count(Papel.ASSASSINO) == papeis.count(Papel.DETETIVE) == 1
    assert papeis.count(Papel.VITIMA) == 1
    assert papeis.count(Papel.INOCENTE) >= 3
    assert caso.personagem(caso.culpado_id).papel == Papel.ASSASSINO


@pytest.mark.parametrize("pronto", CASOS, ids=lambda c: c.chave.value)
def test_caso_e_resolvivel(pronto: CasoPronto) -> None:
    caso = pronto.caso
    provas = set(caso.condicao_acerto.provas_minimas)
    assert len(provas) >= caso.condicao_acerto.quantas_provas
    assert {p.id for p in caso.pistas if p.tipo == "falsa"}
    assert pronto.apresentacao and pronto.solucao


@pytest.mark.parametrize("pronto", CASOS, ids=lambda c: c.chave.value)
def test_escalacao_usa_personas_diferentes_com_funcao(pronto: CasoPronto) -> None:
    personas = [escalado.persona for escalado in pronto.escalacao.values()]
    assert len(personas) == len(set(personas)) == 6
    assert all(escalado.funcao for escalado in pronto.escalacao.values())
    for pessoa, escalado in pronto.escalacao.items():
        assert pronto.caso.personagem(pessoa).nome == ELENCO[escalado.persona].nome


def test_culpados_e_vitimas_variam_entre_casos() -> None:
    culpados = {c.escalacao[c.caso.culpado_id].persona for c in CASOS}
    assert len(culpados) >= 4


def test_catalogo_escolhe_o_caso_pela_seed_de_forma_deterministica() -> None:
    catalogo = CatalogoDeCasos()
    assert catalogo.caso_para(0) is catalogo.caso_para(5)
    assert {catalogo.caso_para(seed).chave for seed in range(5)} == set(ChaveCaso)


def test_docs_geradas_nao_divergem_dos_dados() -> None:
    pasta = Path(__file__).resolve().parents[2] / "docs"
    for nome, texto in gerar_tudo().items():
        assert (pasta / nome).read_text(encoding="utf-8").replace("\r\n", "\n") == texto, (
            f"docs/{nome} desatualizado: rode `python tools/gerar_docs.py`"
        )


def test_toda_cor_da_paleta_tem_hex_valido_e_cada_persona_usa_uma_cor_da_paleta() -> None:
    assert set(HEX_DA_COR) == set(Paleta)
    assert all(re.fullmatch(r"#[0-9A-Fa-f]{6}", hexa) for hexa in HEX_DA_COR.values())
    assert all(isinstance(p.aparencia.cor_da_roupa, Paleta) for p in ELENCO.values())


def test_personas_sao_visualmente_distintas() -> None:
    assinaturas = {
        (a.cabelo_cor, a.cabelo_estilo, a.roupa, a.cor_da_roupa)
        for a in (p.aparencia for p in ELENCO.values())
    }
    assert len(assinaturas) == len(ELENCO)
