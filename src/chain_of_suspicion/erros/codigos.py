from enum import StrEnum

from ..dominio.base import ModeloBase


class ErrorCode(StrEnum):
    PARTIDA_NAO_ENCONTRADA = "partida_nao_encontrada"
    PARTIDA_EM_ESTADO_INVALIDO = "partida_em_estado_invalido"
    ACAO_RECUSADA = "acao_recusada"
    CASO_INDISPONIVEL = "caso_indisponivel"
    PROVEDOR_INDISPONIVEL = "provedor_indisponivel"
    TEMPO_ESGOTADO_NO_LLM = "tempo_esgotado_no_llm"
    FALHA_NO_LLM = "falha_no_llm"
    ORCAMENTO_ESTOURADO = "orcamento_estourado"
    REQUISICAO_INVALIDA = "requisicao_invalida"
    ERRO_INTERNO = "erro_interno"


class ErrorResponse(ModeloBase):
    detail: str
    code: ErrorCode
