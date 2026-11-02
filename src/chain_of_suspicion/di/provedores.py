from collections.abc import AsyncIterator

import httpx
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from ..agentes.fabrica import FabricaDeAgentes, FabricaDeAgentesLLM
from ..agentes.grafo import GrafoDaPartida, construir_grafo
from ..config.jogo import GameSettings
from ..config.settings import Settings, settings
from ..erros.excecoes import ProvedorIndisponivel
from ..infra.decisao.cliente import ClienteDeDecisao, ClienteHttp
from ..infra.decisao.decisor import Decisor, DecisorGateway
from ..infra.llm.catalogo import CatalogoLLM
from ..infra.llm.controle import ControleDeUso
from ..infra.llm.langchain import PoliticaDeChamada
from ..servicos.casos import CatalogoDeCasos, ProvedorDeCaso
from ..servicos.montador import MontadorDePartida
from ..servicos.partidas import ServicoDePartidas
from ..servicos.repositorio import RepositorioEmMemoria, RepositorioPartidas


class ProvedorDeConfiguracao(Provider):
    scope = Scope.APP

    @provide
    def configuracoes(self) -> Settings:
        return settings


class ProvedorDeLLM(Provider):
    scope = Scope.APP

    catalogo = provide(CatalogoLLM)
    decisor = provide(DecisorGateway, provides=Decisor)
    fabrica_de_agentes = provide(FabricaDeAgentesLLM, provides=FabricaDeAgentes)

    @provide
    def controle(self, cfg: Settings) -> ControleDeUso:
        return ControleDeUso(cfg.llm.chamadas_simultaneas, cfg.llm.teto_de_custo_usd)

    @provide
    async def http(self, cfg: Settings) -> AsyncIterator[httpx.AsyncClient]:
        if not cfg.api_keys.configurada:
            raise ProvedorIndisponivel("AI_GATEWAY_API_KEY não configurada")
        chave = cfg.api_keys.ai_gateway_api_key.get_secret_value()
        async with httpx.AsyncClient(
            base_url=cfg.llm.url_do_gateway, headers={"Authorization": f"Bearer {chave}"}
        ) as cliente:
            yield cliente

    @provide
    def cliente_de_decisao(
        self, http: httpx.AsyncClient, cfg: Settings, controle: ControleDeUso
    ) -> ClienteDeDecisao:
        politica = PoliticaDeChamada(
            cfg.llm.modelo_decisao,
            cfg.llm.timeout_decisao_segundos,
            cfg.llm.tentativas_por_chamada,
        )
        return ClienteHttp(http, politica, controle)


class ProvedorDePartidas(Provider):
    scope = Scope.APP

    repositorio = provide(RepositorioEmMemoria, provides=RepositorioPartidas)
    casos = provide(CatalogoDeCasos, provides=ProvedorDeCaso)
    montador = provide(MontadorDePartida)
    servico = provide(ServicoDePartidas)

    @provide
    def jogo(self, cfg: Settings) -> GameSettings:
        return cfg.game

    @provide
    def grafo(self) -> GrafoDaPartida:
        return construir_grafo()


def montar_container(*extras: Provider) -> AsyncContainer:
    return make_async_container(
        ProvedorDeConfiguracao(), ProvedorDeLLM(), ProvedorDePartidas(), *extras
    )
