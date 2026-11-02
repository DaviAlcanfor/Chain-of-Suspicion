import pytest

from chain_of_suspicion.agentes.turno import ContextoDoTurno, DecisaoDoTurno
from chain_of_suspicion.conteudo.caso_pronto import CasoPronto
from chain_of_suspicion.conteudo.casos import CATALOGO
from chain_of_suspicion.conteudo.elenco import ELENCO
from chain_of_suspicion.dominio.enums import Papel, TipoAcao, TipoPressao
from chain_of_suspicion.dominio.regras import Pressao, visao_do_personagem
from chain_of_suspicion.prompts.carregador import (
    descrever_turno,
    ficha_da_persona,
    montar_sistema,
    pedido_de_fala,
    prompt_ameaca,
    prompt_contradicao,
)

CASOS = list(CATALOGO.values())
SECOES = [
    "# CONTEXTO DO CASO",
    "# VOCÊ",
    "## PAPEL",
    "## OBJETIVO",
    "## COMO DECIDIR",
    "## REGRAS",
    "## FORMATO",
]


def _contexto(recusa: str | None = None) -> ContextoDoTurno:
    return ContextoDoTurno(
        instante="06/11 21:30",
        local_atual="Biblioteca",
        presentes={},
        saidas={},
        aqui={},
        pistas={},
        acoes_permitidas=[TipoAcao.ESPERAR],
        recusa_anterior=recusa,
    )


def _personagens(pronto: CasoPronto):  # type: ignore[no-untyped-def]
    return list(pronto.caso.personagens)


@pytest.mark.parametrize("pronto", CASOS, ids=lambda c: c.chave.value)
def test_sistema_tem_todas_as_secoes_na_ordem(pronto: CasoPronto) -> None:
    for personagem in _personagens(pronto):
        texto = montar_sistema(pronto, personagem.id)
        posicoes = [texto.index(secao) for secao in SECOES]
        assert posicoes == sorted(posicoes)


@pytest.mark.parametrize("pronto", CASOS, ids=lambda c: c.chave.value)
def test_sistema_traz_contexto_do_caso_e_persona_do_personagem(pronto: CasoPronto) -> None:
    for personagem in _personagens(pronto):
        texto = montar_sistema(pronto, personagem.id)
        persona = ELENCO[pronto.escalacao[personagem.id].persona]
        assert pronto.apresentacao in texto
        assert persona.personalidade in texto
        assert pronto.escalacao[personagem.id].funcao in texto


@pytest.mark.parametrize("pronto", CASOS, ids=lambda c: c.chave.value)
def test_sistema_nunca_vaza_a_solucao_nem_os_fatos_do_caso(pronto: CasoPronto) -> None:
    for personagem in _personagens(pronto):
        texto = montar_sistema(pronto, personagem.id)
        assert pronto.solucao not in texto
        assert all(fato.descricao not in texto for fato in pronto.caso.fatos)
        if personagem.papel != Papel.ASSASSINO:
            assert "Você é o assassino" not in texto


def test_papeis_geram_instrucoes_diferentes() -> None:
    pronto = CASOS[0]
    por_papel = {p.papel: montar_sistema(pronto, p.id) for p in _personagens(pronto)}
    assert len(set(por_papel.values())) == len(por_papel)
    assert "Você é o assassino" in por_papel[Papel.ASSASSINO]
    assert "Você é o detetive" in por_papel[Papel.DETETIVE]


def test_ficha_da_persona_inclui_jeito_de_falar_e_manias() -> None:
    pronto = CASOS[0]
    personagem = pronto.caso.personagens[0]
    ficha = ficha_da_persona(pronto, personagem.id)
    persona = ELENCO[pronto.escalacao[personagem.id].persona]
    assert persona.jeito_de_falar in ficha
    assert persona.manias[0] in ficha


def test_turno_traz_o_que_a_visao_do_personagem_sabe() -> None:
    pronto = CASOS[0]
    marta = next(p for p in pronto.caso.personagens if p.nome == "Marta")
    texto = descrever_turno(visao_do_personagem(pronto.caso, marta.id), _contexto())
    assert "Marta" in texto
    assert "devia uma fortuna" in texto
    assert "recusada" not in texto


def test_turno_mostra_recusa_anterior() -> None:
    pronto = CASOS[0]
    marta = pronto.caso.personagens[0]
    texto = descrever_turno(visao_do_personagem(pronto.caso, marta.id), _contexto("sem caminho"))
    assert "sem caminho" in texto


def test_pedido_de_fala_leva_a_decisao_tomada() -> None:
    mentira = pedido_de_fala(
        "TURNO", DecisaoDoTurno(acao=TipoAcao.CONVERSAR, alvo="Lia", mentir=True)
    )
    sinceridade = pedido_de_fala("TURNO", DecisaoDoTurno(acao=TipoAcao.CONVERSAR))
    assert "conversar com foco em Lia" in mentira
    assert "esconder a verdade" in mentira
    assert "sincero" in sinceridade


def test_prompts_de_decisao_preenchem_todos_os_campos() -> None:
    pronto = CASOS[0]
    visao = visao_do_personagem(pronto.caso, pronto.caso.personagens[0].id)
    assert "{" not in prompt_ameaca(visao, Pressao(tipo=TipoPressao.INSISTIR))
    assert "{" not in prompt_contradicao("estive na cozinha", "estava na biblioteca")
