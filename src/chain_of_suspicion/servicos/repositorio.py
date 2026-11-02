from typing import Protocol

from ..dominio.ids import PartidaId
from ..erros.excecoes import PartidaNaoEncontrada
from .partida import Partida


class RepositorioPartidas(Protocol):
    def salvar(self, partida: Partida) -> None: ...

    def obter(self, partida_id: PartidaId) -> Partida: ...


class RepositorioEmMemoria:
    def __init__(self) -> None:
        self._partidas: dict[PartidaId, Partida] = {}

    def salvar(self, partida: Partida) -> None:
        self._partidas[partida.id] = partida

    def obter(self, partida_id: PartidaId) -> Partida:
        if partida_id not in self._partidas:
            raise PartidaNaoEncontrada(partida_id)
        return self._partidas[partida_id]
