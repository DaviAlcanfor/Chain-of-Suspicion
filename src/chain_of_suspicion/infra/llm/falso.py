from collections import deque
from collections.abc import Sequence
from typing import cast

from pydantic import BaseModel

from ...erros.excecoes import FalhaNoLLM
from .contrato import Mensagem, RespostaLLM


class ProvedorFalso:
    def __init__(self, *respostas: BaseModel | Exception) -> None:
        self._fila = deque(respostas)
        self.pedidos: list[Sequence[Mensagem]] = []

    async def gerar[S: BaseModel](
        self, mensagens: Sequence[Mensagem], saida: type[S]
    ) -> RespostaLLM[S]:
        self.pedidos.append(mensagens)
        if not self._fila:
            raise FalhaNoLLM("o provedor falso ficou sem respostas")
        proxima = self._fila.popleft()
        if isinstance(proxima, Exception):
            raise proxima
        return RespostaLLM(saida=cast(S, proxima))
