from dataclasses import dataclass

from ..dominio.enums import TipoAcao
from ..dominio.eventos import EventoDePartida, TipoEvento
from ..dominio.ids import PersonagemId
from .estado import EstadoPartida


@dataclass(frozen=True)
class Rascunho:
    tipo: TipoEvento
    ator_id: PersonagemId | None = None
    acao: TipoAcao | None = None
    detalhe: str = ""


def emitir(estado: EstadoPartida, *rascunhos: Rascunho) -> list[EventoDePartida]:
    primeiro = len(estado["eventos"])
    instante = estado["mundo"].relogio.agora()
    return [
        EventoDePartida(
            seq=primeiro + posicao,
            tipo=rascunho.tipo,
            instante=instante,
            ator_id=rascunho.ator_id,
            acao=rascunho.acao,
            detalhe=rascunho.detalhe,
        )
        for posicao, rascunho in enumerate(rascunhos)
    ]
