import asyncio
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, cast

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel
from tenacity import (
    AsyncRetrying,
    stop_after_attempt,
    wait_exponential,
)

from ...config.modelos_llm import Modelo
from ...erros.excecoes import FalhaNoLLM, TempoEsgotadoNoLLM
from .contrato import Mensagem, PapelMensagem, RespostaLLM
from .controle import ControleDeUso


@dataclass(frozen=True)
class PoliticaDeChamada:
    modelo: Modelo
    timeout_segundos: float
    tentativas: int
    espera_inicial_segundos: float = 0.5


class ProvedorLangChain:
    def __init__(
        self, chat: BaseChatModel, politica: PoliticaDeChamada, controle: ControleDeUso
    ) -> None:
        self._chat = chat
        self._politica = politica
        self._controle = controle

    async def gerar[S: BaseModel](
        self, mensagens: Sequence[Mensagem], saida: type[S]
    ) -> RespostaLLM[S]:
        async with self._controle.vaga():
            try:
                bruto = await self._com_retry(mensagens, saida)
            except TimeoutError as erro:
                raise TempoEsgotadoNoLLM(f"{self._politica.modelo} estourou o tempo") from erro
            except Exception as erro:
                raise FalhaNoLLM(f"{self._politica.modelo} falhou") from erro
        return self._extrair(bruto, saida)

    async def _com_retry(self, mensagens: Sequence[Mensagem], saida: type[BaseModel]) -> Any:
        executor = self._chat.with_structured_output(saida, include_raw=True)
        entrada = [_converter(mensagem) for mensagem in mensagens]
        tentativas = AsyncRetrying(
            stop=stop_after_attempt(self._politica.tentativas),
            wait=wait_exponential(min=self._politica.espera_inicial_segundos),
            reraise=True,
        )
        async for tentativa in tentativas:
            with tentativa:
                async with asyncio.timeout(self._politica.timeout_segundos):
                    return await executor.ainvoke(entrada)

    def _extrair[S: BaseModel](self, bruto: dict[str, Any], saida: type[S]) -> RespostaLLM[S]:
        interpretado = bruto.get("parsed")
        if not isinstance(interpretado, saida):
            raise FalhaNoLLM(f"{self._politica.modelo} respondeu fora do formato")
        uso = _uso(bruto.get("raw"))
        self._controle.registrar(self._politica.modelo, *uso)
        return RespostaLLM(saida=interpretado, tokens_entrada=uso[0], tokens_saida=uso[1])


def _converter(mensagem: Mensagem) -> BaseMessage:
    if mensagem.papel == PapelMensagem.SISTEMA:
        return SystemMessage(content=mensagem.conteudo)
    return HumanMessage(content=mensagem.conteudo)


def _uso(bruto: object) -> tuple[int, int]:
    if not isinstance(bruto, AIMessage) or bruto.usage_metadata is None:
        return 0, 0
    metadados = cast(dict[str, int], bruto.usage_metadata)
    return metadados.get("input_tokens", 0), metadados.get("output_tokens", 0)
