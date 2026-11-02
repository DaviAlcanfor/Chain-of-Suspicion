from collections.abc import Iterator
from uuid import uuid4

import pytest
from dishka import Provider, Scope, provide
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from ajudas import VENENO, FabricaFalsa, pessoa, settings_de_teste
from chain_of_suspicion.agentes.agente import AgenteFalso
from chain_of_suspicion.agentes.fabrica import FabricaDeAgentes
from chain_of_suspicion.agentes.turno import PropostaDoAgente
from chain_of_suspicion.api.app import criar_app
from chain_of_suspicion.config.settings import Settings
from chain_of_suspicion.di.provedores import montar_container
from chain_of_suspicion.dominio.enums import TipoAcao
from chain_of_suspicion.dominio.eventos import EventoDePartida, TipoEvento
from chain_of_suspicion.erros.codigos import ErrorCode

MARTA = pessoa(VENENO, "Marta")
LIA = pessoa(VENENO, "Lia")


class _Falsos(Provider):
    scope = Scope.APP

    @provide(override=True)
    def configuracoes(self) -> Settings:
        return settings_de_teste(passos_por_partida=3)

    @provide(override=True)
    def agentes(self) -> FabricaDeAgentes:
        espera = PropostaDoAgente(tipo=TipoAcao.ESPERAR, fala="boa noite")
        return FabricaFalsa(AgenteFalso(espera))


class _SemChave(Provider):
    scope = Scope.APP

    @provide(override=True)
    def configuracoes(self) -> Settings:
        return settings_de_teste("")


def _app(*extras: Provider) -> FastAPI:
    return criar_app(montar_container(*extras))


@pytest.fixture
def cliente() -> Iterator[TestClient]:
    with TestClient(_app(_Falsos())) as cliente:
        yield cliente


def _criar(cliente: TestClient) -> str:
    resposta = cliente.post("/partidas", json={"seed": 0})
    assert resposta.status_code == 201
    return str(resposta.json()["id"])


def _eventos(cliente: TestClient, partida_id: str, depois_de: int = -1) -> list[EventoDePartida]:
    url = f"/partidas/{partida_id}/eventos?ultimo_evento={depois_de}"
    with cliente.websocket_connect(url) as ws:
        recebidos = []
        while True:
            try:
                recebidos.append(EventoDePartida.model_validate(ws.receive_json()))
            except WebSocketDisconnect:
                return recebidos


def test_saude(cliente: TestClient) -> None:
    assert cliente.get("/saude").json() == {"status": "ok"}


def test_websocket_entrega_todos_os_eventos_em_ordem_e_fecha(cliente: TestClient) -> None:
    eventos = _eventos(cliente, _criar(cliente))
    assert [e.seq for e in eventos] == list(range(len(eventos)))
    assert eventos[-1].tipo == TipoEvento.PARTIDA_ENCERRADA
    assert any(e.tipo == TipoEvento.FALA for e in eventos)


def test_reconexao_recebe_so_o_que_veio_depois(cliente: TestClient) -> None:
    partida_id = _criar(cliente)
    todos = _eventos(cliente, partida_id)
    resto = _eventos(cliente, partida_id, depois_de=3)
    assert [e.seq for e in resto] == [e.seq for e in todos[4:]]


def test_websocket_de_partida_inexistente_fecha_com_4404(cliente: TestClient) -> None:
    with pytest.raises(WebSocketDisconnect) as erro:  # noqa: SIM117
        with cliente.websocket_connect(f"/partidas/{uuid4()}/eventos"):
            pass
    assert erro.value.code == 4404


def test_consulta_e_estado_sem_segredos(cliente: TestClient) -> None:
    partida_id = _criar(cliente)
    _eventos(cliente, partida_id)
    partida = cliente.get(f"/partidas/{partida_id}").json()
    assert partida["status"] == "encerrada"
    assert partida["motivo_fim"] == "passos_esgotados"
    estado = cliente.get(f"/partidas/{partida_id}/estado")
    assert estado.status_code == 200
    texto = estado.text.lower()
    assert "marta" in texto
    assert "culpado" not in texto
    assert "veneno" not in texto
    assert "devia dinheiro" not in texto


def test_partida_inexistente_vira_404_com_codigo(cliente: TestClient) -> None:
    resposta = cliente.get(f"/partidas/{uuid4()}")
    assert resposta.status_code == 404
    assert resposta.json()["code"] == ErrorCode.PARTIDA_NAO_ENCONTRADA


def test_id_malformado_vira_422_padronizado(cliente: TestClient) -> None:
    resposta = cliente.get("/partidas/nao-e-uuid")
    assert resposta.status_code == 422
    assert resposta.json()["code"] == ErrorCode.REQUISICAO_INVALIDA


def test_pausar_partida_encerrada_vira_409(cliente: TestClient) -> None:
    partida_id = _criar(cliente)
    _eventos(cliente, partida_id)
    resposta = cliente.post(f"/partidas/{partida_id}/pausar")
    assert resposta.status_code == 409
    assert resposta.json()["code"] == ErrorCode.PARTIDA_EM_ESTADO_INVALIDO


def test_acao_invalida_vira_422_e_valida_gera_evento(cliente: TestClient) -> None:
    partida_id = _criar(cliente)
    proibida = {"tipo": "matar", "ator_id": str(LIA), "alvo_personagem_id": str(MARTA)}
    resposta = cliente.post(f"/partidas/{partida_id}/acoes", json=proibida)
    assert resposta.status_code == 422
    assert resposta.json()["code"] == ErrorCode.ACAO_RECUSADA
    valida = {"tipo": "esperar", "ator_id": str(MARTA)}
    aceita = cliente.post(f"/partidas/{partida_id}/acoes", json=valida)
    assert aceita.status_code == 200
    assert EventoDePartida.model_validate(aceita.json()).tipo == TipoEvento.ACAO_APLICADA


def test_sem_a_chave_do_gateway_a_api_responde_503() -> None:
    with TestClient(_app(_SemChave())) as cliente:
        resposta = cliente.post("/partidas", json={"seed": 1})
    assert resposta.status_code == 503
    assert resposta.json()["code"] == ErrorCode.PROVEDOR_INDISPONIVEL


def test_grafo_compilado_fica_no_app_state() -> None:
    app = _app(_Falsos())
    with TestClient(app):
        assert app.state.grafo is not None


def test_erro_inesperado_vira_500_sem_vazar_detalhe() -> None:
    app = _app(_Falsos())

    @app.get("/explode")
    async def explode() -> None:
        raise RuntimeError("senha-do-banco")

    with TestClient(app, raise_server_exceptions=False) as cliente:
        resposta = cliente.get("/explode")
    assert resposta.status_code == 500
    assert resposta.json()["code"] == ErrorCode.ERRO_INTERNO
    assert "senha-do-banco" not in resposta.text


def test_openapi_publica_o_contrato_do_evento(cliente: TestClient) -> None:
    esquemas = cliente.get("/openapi.json").json()["components"]["schemas"]
    assert "EventoDePartida" in esquemas
