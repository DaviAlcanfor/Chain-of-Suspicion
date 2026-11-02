from ..dominio.base import ModeloBase
from ..dominio.enums import Papel
from .modelos_llm import EsforcoRaciocinio, ModeloLLM


class PerfilLLM(ModeloBase, frozen=True):
    modelo: ModeloLLM
    esforco: EsforcoRaciocinio
    timeout_segundos: float


PERFIL_POR_PAPEL: dict[Papel, PerfilLLM] = {
    Papel.INOCENTE: PerfilLLM(
        modelo=ModeloLLM.GPT_6_LUNA, esforco=EsforcoRaciocinio.BAIXO, timeout_segundos=30
    ),
    Papel.DETETIVE: PerfilLLM(
        modelo=ModeloLLM.GPT_6_LUNA, esforco=EsforcoRaciocinio.ALTO, timeout_segundos=60
    ),
    Papel.ASSASSINO: PerfilLLM(
        modelo=ModeloLLM.GPT_6_LUNA, esforco=EsforcoRaciocinio.ALTO, timeout_segundos=60
    ),
    Papel.VITIMA: PerfilLLM(
        modelo=ModeloLLM.GPT_6_LUNA, esforco=EsforcoRaciocinio.NENHUM, timeout_segundos=30
    ),
}
