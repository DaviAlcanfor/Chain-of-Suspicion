from ...config.perfis import PERFIL_POR_PAPEL, PerfilLLM
from ...config.settings import Settings
from ...dominio.enums import Papel
from .contrato import ProvedorLLM
from .controle import ControleDeUso
from .fabrica import construir_chat
from .langchain import PoliticaDeChamada, ProvedorLangChain


class CatalogoLLM:
    def __init__(self, cfg: Settings, controle: ControleDeUso) -> None:
        self._cfg = cfg
        self._controle = controle
        self._por_papel: dict[Papel, ProvedorLLM] = {}

    def para(self, papel: Papel) -> ProvedorLLM:
        if papel not in self._por_papel:
            self._por_papel[papel] = self._construir(PERFIL_POR_PAPEL[papel])
        return self._por_papel[papel]

    def _construir(self, perfil: PerfilLLM) -> ProvedorLLM:
        politica = PoliticaDeChamada(
            perfil.modelo, perfil.timeout_segundos, self._cfg.llm.tentativas_por_chamada
        )
        chat = construir_chat(perfil.modelo, perfil.esforco, self._cfg)
        return ProvedorLangChain(chat, politica, self._controle)
