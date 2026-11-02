from pydantic import Field

from .ambiente import Ambiente


class GameSettings(Ambiente):
    passos_por_partida: int = Field(default=50, ge=1)
    passo_em_minutos: int = Field(default=10, ge=1)
    tentativas_por_acao: int = Field(default=2, ge=0)
    minutos_antes_do_crime: int = Field(default=40, ge=0)
