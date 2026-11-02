import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..erros.codigos import ErrorCode, ErrorResponse
from ..erros.excecoes import (
    AcaoRecusada,
    CasoIndisponivel,
    ErroJogo,
    FalhaNoLLM,
    OrcamentoEstourado,
    PartidaEmEstadoInvalido,
    PartidaNaoEncontrada,
    ProvedorIndisponivel,
    TempoEsgotadoNoLLM,
)

logger = logging.getLogger(__name__)

STATUS_POR_ERRO: dict[type[ErroJogo], int] = {
    PartidaNaoEncontrada: status.HTTP_404_NOT_FOUND,
    PartidaEmEstadoInvalido: status.HTTP_409_CONFLICT,
    AcaoRecusada: status.HTTP_422_UNPROCESSABLE_CONTENT,
    CasoIndisponivel: status.HTTP_501_NOT_IMPLEMENTED,
    ProvedorIndisponivel: status.HTTP_503_SERVICE_UNAVAILABLE,
    TempoEsgotadoNoLLM: status.HTTP_504_GATEWAY_TIMEOUT,
    FalhaNoLLM: status.HTTP_502_BAD_GATEWAY,
    OrcamentoEstourado: status.HTTP_429_TOO_MANY_REQUESTS,
}

type Handler = Callable[[Request, Exception], Awaitable[JSONResponse]]


def _resposta(status_http: int, detail: str, code: ErrorCode) -> JSONResponse:
    corpo = ErrorResponse(detail=detail, code=code)
    return JSONResponse(status_code=status_http, content=corpo.model_dump(mode="json"))


def _handler_de(status_http: int) -> Handler:
    async def tratar(request: Request, erro: Exception) -> JSONResponse:
        if not isinstance(erro, ErroJogo):
            raise erro
        return _resposta(status_http, str(erro), erro.codigo)

    return tratar


async def _requisicao_invalida(request: Request, erro: Exception) -> JSONResponse:
    return _resposta(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "Requisição inválida.",
        ErrorCode.REQUISICAO_INVALIDA,
    )


async def _inesperado(request: Request, erro: Exception) -> JSONResponse:
    logger.error("Erro não tratado em %s %s", request.method, request.url.path, exc_info=erro)
    return _resposta(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro interno inesperado.", ErrorCode.ERRO_INTERNO
    )


def registrar_handlers(app: FastAPI) -> None:
    for tipo, status_http in STATUS_POR_ERRO.items():
        app.add_exception_handler(tipo, _handler_de(status_http))
    app.add_exception_handler(ErroJogo, _handler_de(status.HTTP_500_INTERNAL_SERVER_ERROR))
    app.add_exception_handler(RequestValidationError, _requisicao_invalida)
    app.add_exception_handler(Exception, _inesperado)
