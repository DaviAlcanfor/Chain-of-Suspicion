from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from ...config.modelos_llm import MODELOS_COM_ESFORCO, EsforcoRaciocinio, ModeloLLM
from ...config.settings import Settings
from ...erros.excecoes import ProvedorIndisponivel


def construir_chat(modelo: ModeloLLM, esforco: EsforcoRaciocinio, cfg: Settings) -> BaseChatModel:
    if not cfg.api_keys.configurada:
        raise ProvedorIndisponivel("AI_GATEWAY_API_KEY não configurada")
    return ChatOpenAI(
        model=modelo.value,
        api_key=cfg.api_keys.ai_gateway_api_key,
        base_url=cfg.llm.url_do_gateway,
        reasoning_effort=esforco.value if modelo in MODELOS_COM_ESFORCO else None,
    )
