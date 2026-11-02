from typing import Any

from chain_of_suspicion.agentes.agente import Agente, AgenteFalso
from chain_of_suspicion.agentes.turno import PropostaDoAgente
from chain_of_suspicion.config.api_keys import APIKeySettings
from chain_of_suspicion.config.jogo import GameSettings
from chain_of_suspicion.config.llm import LLMSettings
from chain_of_suspicion.config.settings import Settings
from chain_of_suspicion.conteudo.caso_pronto import CasoPronto, ChaveCaso
from chain_of_suspicion.conteudo.casos import CATALOGO
from chain_of_suspicion.dominio.acoes import PERMISSOES
from chain_of_suspicion.dominio.enums import TipoAcao
from chain_of_suspicion.dominio.ids import PersonagemId

ESPERAR = PropostaDoAgente(tipo=TipoAcao.ESPERAR)
VENENO = CATALOGO[ChaveCaso.VENENO_NA_BIBLIOTECA]


def settings_de_teste(chave: str = "chave", **jogo: Any) -> Settings:
    return Settings(
        api_keys=APIKeySettings(_env_file=None, ai_gateway_api_key=chave),  # type: ignore[call-arg, arg-type]
        llm=LLMSettings(_env_file=None),  # type: ignore[call-arg]
        game=GameSettings(_env_file=None, **jogo),  # type: ignore[call-arg]
    )


def pessoa(pronto: CasoPronto, nome: str) -> PersonagemId:
    return next(p.id for p in pronto.caso.personagens if p.nome == nome)


class FabricaFalsa:
    def __init__(self, agente: Agente | None = None) -> None:
        self._agente = agente

    def para(self, pronto: CasoPronto) -> dict[PersonagemId, Agente]:
        return {
            p.id: self._agente or AgenteFalso(ESPERAR)
            for p in pronto.caso.personagens
            if PERMISSOES[p.papel]
        }
