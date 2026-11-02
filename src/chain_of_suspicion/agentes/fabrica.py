from typing import Protocol

from ..conteudo.caso_pronto import CasoPronto
from ..dominio.acoes import PERMISSOES
from ..dominio.ids import PersonagemId
from ..infra.decisao.decisor import Decisor
from ..infra.llm.catalogo import CatalogoLLM
from ..prompts.carregador import ficha_da_persona, montar_sistema
from .agente import Agente, AgenteEmDuasEtapas, FichaDoAgente


class FabricaDeAgentes(Protocol):
    def para(self, pronto: CasoPronto) -> dict[PersonagemId, Agente]: ...


class FabricaDeAgentesLLM:
    def __init__(self, catalogo: CatalogoLLM, decisor: Decisor) -> None:
        self._catalogo = catalogo
        self._decisor = decisor

    def para(self, pronto: CasoPronto) -> dict[PersonagemId, Agente]:
        return {
            personagem.id: AgenteEmDuasEtapas(
                self._decisor,
                self._catalogo.para(personagem.papel),
                FichaDoAgente(
                    sistema=montar_sistema(pronto, personagem.id),
                    persona=ficha_da_persona(pronto, personagem.id),
                ),
            )
            for personagem in pronto.caso.personagens
            if PERMISSOES[personagem.papel]
        }
