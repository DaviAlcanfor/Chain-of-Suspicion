import asyncio
from collections import deque
from typing import Annotated, Any, Literal, Protocol

import httpx
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ...erros.excecoes import FalhaNoLLM, TempoEsgotadoNoLLM
from ..llm.controle import ControleDeUso
from ..llm.langchain import PoliticaDeChamada
from .perguntas import (
    Pergunta,
    Resultado,
    ResultadoBooleano,
    ResultadoEscolha,
    ResultadoNota,
)

CHAVE_DA_PERGUNTA = "r"
STATUS_TRANSITORIOS = frozenset({429, 500, 502, 503, 504})


class ClienteDeDecisao(Protocol):
    async def perguntar(self, estado: str, pergunta: Pergunta) -> Resultado: ...


class _Externo(BaseModel):
    model_config = ConfigDict(extra="ignore")


class _Booleana(_Externo):
    type: Literal["boolean"]
    probability: float


class _Escolha(_Externo):
    type: Literal["choice"]
    choice: str
    probabilities: dict[str, float]


class _Nota(_Externo):
    type: Literal["score"]
    score: float
    probabilities: dict[str, float]


_Union = _Booleana | _Escolha | _Nota
_RESPOSTA: TypeAdapter[_Union] = TypeAdapter(Annotated[_Union, Field(discriminator="type")])


class _Uso(_Externo):
    inputTokens: int = 0
    outputTokens: int = 0


class _Transitorio(Exception):
    pass


class ClienteHttp:
    def __init__(
        self, http: httpx.AsyncClient, politica: PoliticaDeChamada, controle: ControleDeUso
    ) -> None:
        self._http = http
        self._politica = politica
        self._controle = controle

    async def perguntar(self, estado: str, pergunta: Pergunta) -> Resultado:
        corpo = {
            "model": self._politica.modelo.value,
            "state": estado,
            "questions": {CHAVE_DA_PERGUNTA: pergunta.payload()},
        }
        async with self._controle.vaga():
            try:
                dados = await self._com_retry(corpo)
            except TimeoutError as erro:
                raise TempoEsgotadoNoLLM(f"{self._politica.modelo} estourou o tempo") from erro
            except (httpx.HTTPError, _Transitorio) as erro:
                raise FalhaNoLLM(f"{self._politica.modelo} indisponível") from erro
        return self._interpretar(dados, pergunta)

    async def _com_retry(self, corpo: dict[str, Any]) -> dict[str, Any]:
        tentativas = AsyncRetrying(
            stop=stop_after_attempt(self._politica.tentativas),
            wait=wait_exponential(min=self._politica.espera_inicial_segundos),
            retry=retry_if_exception_type((httpx.TransportError, _Transitorio)),
            reraise=True,
        )
        async for tentativa in tentativas:
            with tentativa:
                async with asyncio.timeout(self._politica.timeout_segundos):
                    resposta = await self._http.post("/evaluate", json=corpo)
                if resposta.status_code in STATUS_TRANSITORIOS:
                    raise _Transitorio(resposta.status_code)
                resposta.raise_for_status()
                dados: dict[str, Any] = resposta.json()
                return dados
        raise AssertionError("o laço de retry sempre retorna ou levanta")

    def _interpretar(self, dados: dict[str, Any], pergunta: Pergunta) -> Resultado:
        try:
            bruto = _RESPOSTA.validate_python(dados["answers"][CHAVE_DA_PERGUNTA])
            uso = _Uso.model_validate(dados.get("usage", {}))
        except (KeyError, ValidationError) as erro:
            raise FalhaNoLLM("resposta de decisão fora do formato") from erro
        custo = float(dados.get("providerMetadata", {}).get("gateway", {}).get("cost", 0))
        self._controle.registrar_custo(custo, uso.inputTokens, uso.outputTokens)
        return _converter(bruto, pergunta)


def _converter(bruto: _Union, pergunta: Pergunta) -> Resultado:
    match bruto:
        case _Booleana():
            return ResultadoBooleano(probabilidade=bruto.probability)
        case _Escolha():
            return ResultadoEscolha(escolha=bruto.choice, probabilidades=bruto.probabilities)
        case _Nota():
            return ResultadoNota(
                nota=bruto.score, niveis=len(pergunta.niveis or bruto.probabilities)
            )


class ClienteFalso:
    def __init__(self, *resultados: Resultado | Exception) -> None:
        self._fila = deque(resultados)
        self.perguntas: list[tuple[str, Pergunta]] = []

    async def perguntar(self, estado: str, pergunta: Pergunta) -> Resultado:
        self.perguntas.append((estado, pergunta))
        if not self._fila:
            raise FalhaNoLLM("o cliente falso ficou sem respostas")
        proximo = self._fila.popleft()
        if isinstance(proximo, Exception):
            raise proximo
        return proximo
