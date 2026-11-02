from enum import StrEnum


class ModeloLLM(StrEnum):
    GPT_6_LUNA = "openai/gpt-6-luna"
    CLAUDE_HAIKU = "anthropic/claude-haiku-5.5"


class ModeloDecisao(StrEnum):
    JEV = "typesafe-ai/jev"
    D1_ULTRA = "liquid/d1-ultra"
    GPT_6_LUNA_DECISIONS = "openai/gpt-6-luna-decisions"


type Modelo = ModeloLLM | ModeloDecisao


class EsforcoRaciocinio(StrEnum):
    NENHUM = "none"
    BAIXO = "low"
    MEDIO = "medium"
    ALTO = "high"
    MAXIMO = "max"


MODELOS_COM_ESFORCO = frozenset({ModeloLLM.GPT_6_LUNA})
