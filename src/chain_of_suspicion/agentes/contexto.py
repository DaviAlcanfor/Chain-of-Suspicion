from ..dominio.acoes import PERMISSOES
from ..dominio.ids import PersonagemId
from ..dominio.mundo import Mundo
from ..dominio.relogio import formatar_instante
from .turno import ContextoDoTurno


def montar_contexto(
    mundo: Mundo, ator_id: PersonagemId, recusa: str | None = None
) -> ContextoDoTurno:
    caso = mundo.caso
    local_id = mundo.posicoes[ator_id]
    permitidas = PERMISSOES[caso.personagem(ator_id).papel]
    return ContextoDoTurno(
        instante=formatar_instante(mundo.relogio.agora()),
        local_atual=caso.mapa.nome(local_id),
        presentes={
            caso.personagem(outro).nome: outro
            for outro, onde in mundo.posicoes.items()
            if onde == local_id and outro != ator_id and outro not in mundo.mortos
        },
        saidas={caso.mapa.nome(vizinho): vizinho for vizinho in caso.mapa.vizinhos(local_id)},
        aqui={caso.mapa.nome(local_id): local_id},
        pistas={},
        acoes_permitidas=sorted(permitidas),
        recusa_anterior=recusa,
    )
