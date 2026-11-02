import pytest

from ajudas import VENENO, pessoa
from chain_of_suspicion.dominio.enums import TipoAcao, TipoPressao
from chain_of_suspicion.dominio.regras import Pressao, visao_do_personagem
from chain_of_suspicion.erros.excecoes import FalhaNoLLM
from chain_of_suspicion.infra.decisao.cliente import ClienteFalso
from chain_of_suspicion.infra.decisao.decisor import DecisorGateway
from chain_of_suspicion.infra.decisao.perguntas import (
    PerguntaDeDecisao,
    ResultadoBooleano,
    ResultadoEscolha,
    ResultadoNota,
)

MARTA = pessoa(VENENO, "Marta")
LIA = pessoa(VENENO, "Lia")
HALL = VENENO.caso.mapa.locais[0].id


def _escolha(valor: str) -> ResultadoEscolha:
    return ResultadoEscolha(escolha=valor, probabilidades={valor: 1.0})


async def test_escolher_acao_devolve_o_tipo_de_acao_e_descreve_as_opcoes() -> None:
    cliente = ClienteFalso(_escolha("mover"))
    acao = await DecisorGateway(cliente).escolher_acao("estado", [TipoAcao.MOVER, TipoAcao.ESPERAR])
    assert acao == TipoAcao.MOVER
    pergunta = cliente.perguntas[0][1]
    assert pergunta.tipo == PerguntaDeDecisao.ESCOLHER_ACAO
    assert set(pergunta.opcoes or {}) == {"mover", "esperar"}


async def test_escolha_fora_das_opcoes_e_rejeitada() -> None:
    decisor = DecisorGateway(ClienteFalso(_escolha("matar")))
    with pytest.raises(FalhaNoLLM):
        await decisor.escolher_acao("estado", [TipoAcao.MOVER])


async def test_tipo_de_resposta_errado_e_rejeitado() -> None:
    decisor = DecisorGateway(ClienteFalso(ResultadoBooleano(probabilidade=0.9)))
    with pytest.raises(FalhaNoLLM):
        await decisor.escolher_alvo("estado", {"Lia": "pessoa"})


async def test_deve_mentir_usa_o_limiar() -> None:
    decisor = DecisorGateway(
        ClienteFalso(ResultadoBooleano(probabilidade=0.7), ResultadoBooleano(probabilidade=0.2))
    )
    assert await decisor.deve_mentir("estado") is True
    assert await decisor.deve_mentir("estado") is False


async def test_ameaca_vem_normalizada_entre_0_e_1() -> None:
    decisor = DecisorGateway(ClienteFalso(ResultadoNota(nota=2.0, niveis=5)))
    visao = visao_do_personagem(VENENO.caso, MARTA)
    decisao = await decisor.ameaca(visao, Pressao(tipo=TipoPressao.INSISTIR))
    assert decisao.ameaca == pytest.approx(0.5)


async def test_contradicao_traz_a_confianca() -> None:
    decisor = DecisorGateway(ClienteFalso(ResultadoBooleano(probabilidade=0.1)))
    decisao = await decisor.contradiz("estive no quarto", "estava na biblioteca")
    assert decisao.contradiz is False
    assert decisao.confianca == pytest.approx(0.9)
