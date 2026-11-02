from pydantic import Field

from .ambiente import Ambiente
from .modelos_llm import ModeloDecisao

URL_DO_GATEWAY = "https://ai-gateway.vercel.sh/v1"


class LLMSettings(Ambiente):
    url_do_gateway: str = URL_DO_GATEWAY
    modelo_decisao: ModeloDecisao = ModeloDecisao.D1_ULTRA
    chamadas_simultaneas: int = Field(default=8, ge=1)
    tentativas_por_chamada: int = Field(default=3, ge=1)
    timeout_decisao_segundos: float = Field(default=15.0, gt=0.0)
    teto_de_custo_usd: float = Field(default=1.0, gt=0.0)
