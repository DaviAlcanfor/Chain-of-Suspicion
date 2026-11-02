from pydantic import ValidationError

from ..dominio.acoes import Acao, AcaoInvalida
from ..dominio.base import ModeloBase
from ..dominio.enums import TipoAcao
from ..dominio.ids import LocalId, PersonagemId, PistaId


class ContextoDoTurno(ModeloBase):
    instante: str
    local_atual: str
    presentes: dict[str, PersonagemId]
    saidas: dict[str, LocalId]
    aqui: dict[str, LocalId]
    pistas: dict[str, PistaId]
    acoes_permitidas: list[TipoAcao]
    recusa_anterior: str | None = None


class PropostaDoAgente(ModeloBase):
    tipo: TipoAcao
    alvo_personagem: str | None = None
    alvo_local: str | None = None
    pista: str | None = None
    fala: str | None = None


class DecisaoDoTurno(ModeloBase):
    acao: TipoAcao
    alvo: str | None = None
    mentir: bool = False


class FalaGerada(ModeloBase):
    fala: str


def montar_acao(
    ator_id: PersonagemId, proposta: PropostaDoAgente, contexto: ContextoDoTurno
) -> Acao:
    try:
        return Acao(
            tipo=proposta.tipo,
            ator_id=ator_id,
            alvo_personagem_id=_resolver(proposta.alvo_personagem, contexto.presentes),
            alvo_local_id=_resolver(proposta.alvo_local, contexto.saidas | contexto.aqui),
            pista_id=_resolver(proposta.pista, contexto.pistas),
        )
    except ValidationError as erro:
        raise AcaoInvalida("proposta incompleta para a ação escolhida") from erro


def _resolver[Id](nome: str | None, conhecidos: dict[str, Id]) -> Id | None:
    if nome is None:
        return None
    if nome not in conhecidos:
        raise AcaoInvalida(f"'{nome}' não é uma opção válida neste turno")
    return conhecidos[nome]
