from __future__ import annotations

import heapq
from datetime import timedelta

from pydantic import model_validator

from .base import ModeloBase
from .ids import LocalId


class Local(ModeloBase):
    id: LocalId
    nome: str


class Conexao(ModeloBase):
    origem: LocalId
    destino: LocalId
    tempo: timedelta


class Mapa(ModeloBase):
    locais: list[Local]
    conexoes: list[Conexao]

    @model_validator(mode="after")
    def _consistencia(self) -> Mapa:
        ids = {local.id for local in self.locais}
        if len(ids) != len(self.locais):
            raise ValueError("ids de local repetidos")
        for conexao in self.conexoes:
            self._validar_conexao(conexao, ids)
        if self._alcancaveis_a_partir_de(self.locais[0].id) != ids:
            raise ValueError("há locais isolados no mapa")
        return self

    @staticmethod
    def _validar_conexao(conexao: Conexao, ids: set[LocalId]) -> None:
        if conexao.origem == conexao.destino:
            raise ValueError("conexão de um local com ele mesmo")
        if not {conexao.origem, conexao.destino} <= ids:
            raise ValueError("conexão com local inexistente")
        if conexao.tempo <= timedelta(0):
            raise ValueError("o tempo de deslocamento precisa ser positivo")

    def existe(self, local_id: LocalId) -> bool:
        return any(local.id == local_id for local in self.locais)

    def nome(self, local_id: LocalId) -> str:
        return next(local.nome for local in self.locais if local.id == local_id)

    def vizinhos(self, local_id: LocalId) -> set[LocalId]:
        return {destino for destino, _ in self._adjacencia()[local_id]}

    def tempo_minimo(self, origem: LocalId, destino: LocalId) -> timedelta | None:
        melhores = {origem: timedelta(0)}
        fila = [(timedelta(0), origem)]
        adjacencia = self._adjacencia()
        while fila:
            custo, atual = heapq.heappop(fila)
            if atual == destino:
                return custo
            if custo > melhores[atual]:
                continue
            for vizinho, tempo in adjacencia[atual]:
                novo_custo = custo + tempo
                if novo_custo < melhores.get(vizinho, timedelta.max):
                    melhores[vizinho] = novo_custo
                    heapq.heappush(fila, (novo_custo, vizinho))
        return None

    def _adjacencia(self) -> dict[LocalId, list[tuple[LocalId, timedelta]]]:
        adjacencia: dict[LocalId, list[tuple[LocalId, timedelta]]] = {
            local.id: [] for local in self.locais
        }
        for conexao in self.conexoes:
            adjacencia[conexao.origem].append((conexao.destino, conexao.tempo))
            adjacencia[conexao.destino].append((conexao.origem, conexao.tempo))
        return adjacencia

    def _alcancaveis_a_partir_de(self, inicio: LocalId) -> set[LocalId]:
        adjacencia = self._adjacencia()
        visitados = {inicio}
        pendentes = [inicio]
        while pendentes:
            for vizinho, _ in adjacencia[pendentes.pop()]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pendentes.append(vizinho)
        return visitados
