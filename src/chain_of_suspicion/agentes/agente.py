from collections import deque
from dataclasses import dataclass
from typing import Protocol

from ..dominio.acoes import CAMPOS_EXIGIDOS
from ..dominio.enums import Papel, TipoAcao
from ..dominio.regras import VisaoPersonagem
from ..infra.decisao.decisor import Decisor
from ..infra.llm.contrato import Mensagem, PapelMensagem, ProvedorLLM
from ..prompts.carregador import descrever_turno, estado_para_decisao, pedido_de_fala
from ..prompts.descricoes import ACOES_COM_FALA
from .turno import ContextoDoTurno, DecisaoDoTurno, FalaGerada, PropostaDoAgente

ACOES_FORA_DO_LACO = frozenset({TipoAcao.ACUSAR})
DESCRICAO_DO_ALVO = {
    "alvo_personagem_id": "pessoa presente aqui",
    "alvo_local_id": "local",
    "pista_id": "pista",
}


class Agente(Protocol):
    async def decidir(
        self, visao: VisaoPersonagem, contexto: ContextoDoTurno
    ) -> PropostaDoAgente: ...


@dataclass(frozen=True)
class FichaDoAgente:
    sistema: str
    persona: str


class AgenteEmDuasEtapas:
    def __init__(self, decisor: Decisor, fala: ProvedorLLM, ficha: FichaDoAgente) -> None:
        self._decisor = decisor
        self._fala = fala
        self._ficha = ficha

    async def decidir(self, visao: VisaoPersonagem, contexto: ContextoDoTurno) -> PropostaDoAgente:
        turno = descrever_turno(visao, contexto)
        estado = estado_para_decisao(self._ficha.persona, turno)
        acao = await self._decisor.escolher_acao(estado, _viaveis(contexto))
        alvos = await self._escolher_alvos(estado, acao, contexto)
        proposta = PropostaDoAgente(tipo=acao, **alvos)
        if acao not in ACOES_COM_FALA:
            return proposta
        mentir = await self._decidir_mentira(estado, visao, acao)
        decisao = DecisaoDoTurno(acao=acao, alvo=next(iter(alvos.values()), None), mentir=mentir)
        return proposta.model_copy(update={"fala": await self._falar(turno, decisao)})

    async def _escolher_alvos(
        self, estado: str, acao: TipoAcao, contexto: ContextoDoTurno
    ) -> dict[str, str]:
        escolhidos: dict[str, str] = {}
        for campo in CAMPOS_EXIGIDOS.get(acao, ()):
            opcoes = _opcoes(contexto, acao, campo)
            if len(opcoes) == 1:
                escolhidos[_atributo(campo)] = next(iter(opcoes))
                continue
            pergunta = f"{estado}\n\nAção decidida: {acao.value}."
            descritas = dict.fromkeys(opcoes, DESCRICAO_DO_ALVO[campo])
            escolhidos[_atributo(campo)] = await self._decisor.escolher_alvo(pergunta, descritas)
        return escolhidos

    async def _decidir_mentira(self, estado: str, visao: VisaoPersonagem, acao: TipoAcao) -> bool:
        if not visao.segredos and visao.papel != Papel.ASSASSINO:
            return False
        return await self._decisor.deve_mentir(f"{estado}\n\nAção decidida: {acao.value}.")

    async def _falar(self, turno: str, decisao: DecisaoDoTurno) -> str:
        mensagens = [
            Mensagem(papel=PapelMensagem.SISTEMA, conteudo=self._ficha.sistema),
            Mensagem(papel=PapelMensagem.USUARIO, conteudo=pedido_de_fala(turno, decisao)),
        ]
        return (await self._fala.gerar(mensagens, FalaGerada)).saida.fala


class AgenteFalso:
    def __init__(self, *propostas: PropostaDoAgente | Exception) -> None:
        self._fila = deque(propostas)
        self.contextos: list[ContextoDoTurno] = []

    async def decidir(self, visao: VisaoPersonagem, contexto: ContextoDoTurno) -> PropostaDoAgente:
        self.contextos.append(contexto)
        proxima = self._fila[0] if len(self._fila) == 1 else self._fila.popleft()
        if isinstance(proxima, Exception):
            raise proxima
        return proxima


def _atributo(campo: str) -> str:
    return {
        "alvo_personagem_id": "alvo_personagem",
        "alvo_local_id": "alvo_local",
        "pista_id": "pista",
    }[campo]


def _opcoes(contexto: ContextoDoTurno, acao: TipoAcao, campo: str) -> dict[str, object]:
    if campo == "alvo_personagem_id":
        return dict(contexto.presentes)
    if campo == "pista_id":
        return dict(contexto.pistas)
    return dict(contexto.saidas if acao == TipoAcao.MOVER else contexto.aqui)


def _viaveis(contexto: ContextoDoTurno) -> list[TipoAcao]:
    return [
        acao
        for acao in contexto.acoes_permitidas
        if acao not in ACOES_FORA_DO_LACO
        and all(_opcoes(contexto, acao, campo) for campo in CAMPOS_EXIGIDOS.get(acao, ()))
    ]
