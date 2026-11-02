import pytest
from langchain_core.language_models import BaseChatModel

from ajudas import settings_de_teste
from chain_of_suspicion.config.modelos_llm import EsforcoRaciocinio, ModeloLLM
from chain_of_suspicion.dominio.enums import Papel
from chain_of_suspicion.erros.excecoes import ProvedorIndisponivel
from chain_of_suspicion.infra.llm.catalogo import CatalogoLLM
from chain_of_suspicion.infra.llm.controle import ControleDeUso
from chain_of_suspicion.infra.llm.fabrica import construir_chat


@pytest.mark.parametrize("modelo", list(ModeloLLM))
def test_com_a_chave_do_gateway_todo_modelo_vira_um_chat(modelo: ModeloLLM) -> None:
    chat = construir_chat(modelo, EsforcoRaciocinio.BAIXO, settings_de_teste("chave"))
    assert isinstance(chat, BaseChatModel)


@pytest.mark.parametrize("modelo", list(ModeloLLM))
def test_sem_a_chave_do_gateway_fica_indisponivel(modelo: ModeloLLM) -> None:
    with pytest.raises(ProvedorIndisponivel):
        construir_chat(modelo, EsforcoRaciocinio.BAIXO, settings_de_teste(""))


def test_catalogo_reaproveita_o_provedor_do_papel() -> None:
    catalogo = CatalogoLLM(settings_de_teste(), ControleDeUso(2, 1.0))
    assert catalogo.para(Papel.DETETIVE) is catalogo.para(Papel.DETETIVE)
