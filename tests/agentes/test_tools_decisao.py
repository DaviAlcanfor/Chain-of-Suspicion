import pytest

from ajudas import VENENO, pessoa
from chain_of_suspicion.agentes.tools.decisao import ESQUEMA_DOS_ARGUMENTOS, criar_ferramentas
from chain_of_suspicion.dominio.enums import TipoAcao, TipoPressao
from chain_of_suspicion.dominio.regras import Pressao, visao_do_personagem
from chain_of_suspicion.infra.decisao.cliente import ClienteFalso
from chain_of_suspicion.infra.decisao.decisor import DecisorGateway
from chain_of_suspicion.infra.decisao.perguntas import (
    PerguntaDeDecisao,
    ResultadoBooleano,
    ResultadoEscolha,
    ResultadoNota,
)


def _ferramentas(*respostas: ResultadoBooleano | ResultadoEscolha | ResultadoNota):  # type: ignore[no-untyped-def]
    return criar_ferramentas(DecisorGateway(ClienteFalso(*respostas)))


def test_ha_uma_ferramenta_por_pergunta_com_nome_e_esquema() -> None:
    ferramentas = _ferramentas()
    assert set(ferramentas) == set(PerguntaDeDecisao) == set(ESQUEMA_DOS_ARGUMENTOS)
    for pergunta, ferramenta in ferramentas.items():
        assert ferramenta.name == pergunta.value
        assert ferramenta.description
        assert ferramenta.args_schema is ESQUEMA_DOS_ARGUMENTOS[pergunta]


async def test_escolher_acao_devolve_o_valor_da_acao() -> None:
    ferramentas = _ferramentas(ResultadoEscolha(escolha="mover", probabilidades={"mover": 1}))
    ferramenta = ferramentas[PerguntaDeDecisao.ESCOLHER_ACAO]
    resultado = await ferramenta.ainvoke({"estado": "x", "viaveis": ["mover", "esperar"]})
    assert resultado == {"acao": TipoAcao.MOVER.value}


async def test_escolher_alvo_e_deve_mentir() -> None:
    ferramentas = _ferramentas(
        ResultadoEscolha(escolha="Lia", probabilidades={"Lia": 1}),
        ResultadoBooleano(probabilidade=0.9),
    )
    alvo = await ferramentas[PerguntaDeDecisao.ESCOLHER_ALVO].ainvoke(
        {"estado": "x", "opcoes": {"Lia": "pessoa presente aqui"}}
    )
    mentir = await ferramentas[PerguntaDeDecisao.DEVE_MENTIR].ainvoke({"estado": "x"})
    assert alvo == {"alvo": "Lia"}
    assert mentir == {"mentir": True}


async def test_ameaca_e_contradicao() -> None:
    ferramentas = _ferramentas(
        ResultadoNota(nota=4.0, niveis=5), ResultadoBooleano(probabilidade=0.2)
    )
    visao = visao_do_personagem(VENENO.caso, pessoa(VENENO, "Marta"))
    ameaca = await ferramentas[PerguntaDeDecisao.AMEACA].ainvoke(
        {"visao": visao, "pressao": Pressao(tipo=TipoPressao.INSISTIR)}
    )
    contradicao = await ferramentas[PerguntaDeDecisao.CONTRADICAO].ainvoke(
        {"declaracao": "estive no quarto", "fato": "estava na biblioteca"}
    )
    assert ameaca == {"ameaca": pytest.approx(1.0)}
    assert contradicao["contradiz"] is False
    assert contradicao["confianca"] == pytest.approx(0.8)
