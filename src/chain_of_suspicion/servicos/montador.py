from datetime import timedelta
from uuid import uuid4

from ..agentes.estado import ContextoDaPartida, LimitesDaPartida
from ..agentes.fabrica import FabricaDeAgentes
from ..config.jogo import GameSettings
from ..dominio.enums import Papel
from ..dominio.ids import PartidaId
from ..dominio.mundo import Mundo
from .casos import ProvedorDeCaso
from .partida import Partida


class MontadorDePartida:
    def __init__(
        self, casos: ProvedorDeCaso, agentes: FabricaDeAgentes, jogo: GameSettings
    ) -> None:
        self._casos = casos
        self._agentes = agentes
        self._antes_do_crime = timedelta(minutes=jogo.minutos_antes_do_crime)
        self._limites = LimitesDaPartida(
            passos=jogo.passos_por_partida,
            passo=timedelta(minutes=jogo.passo_em_minutos),
            tentativas_por_acao=jogo.tentativas_por_acao,
        )

    def montar(self, seed: int) -> Partida:
        pronto = self._casos.caso_para(seed)
        caso = pronto.caso
        mundo = Mundo.no_instante(caso, caso.crime.instante - self._antes_do_crime)
        detetive = next(p.id for p in caso.personagens if p.papel == Papel.DETETIVE)
        mundo.colocar(detetive, pronto.entrada)
        contexto = ContextoDaPartida(self._agentes.para(pronto), self._limites)
        return Partida(PartidaId(uuid4()), mundo, contexto)
