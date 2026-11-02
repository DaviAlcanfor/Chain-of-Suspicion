from ..dominio.base import ModeloBase
from .modelos_llm import Modelo, ModeloLLM


class Preco(ModeloBase, frozen=True):
    entrada_por_milhao: float
    saida_por_milhao: float


SEM_PRECO = Preco(entrada_por_milhao=0.0, saida_por_milhao=0.0)

PRECO_DO_MODELO: dict[Modelo, Preco] = {
    ModeloLLM.GPT_6_LUNA: Preco(entrada_por_milhao=0.10, saida_por_milhao=0.50),
}
