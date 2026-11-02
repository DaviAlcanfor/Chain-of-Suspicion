from typing import ClassVar

from ..dominio.ids import PartidaId
from .codigos import ErrorCode


class ErroJogo(Exception):
    codigo: ClassVar[ErrorCode] = ErrorCode.ERRO_INTERNO


class PartidaNaoEncontrada(ErroJogo):
    codigo = ErrorCode.PARTIDA_NAO_ENCONTRADA

    def __init__(self, partida_id: PartidaId) -> None:
        self.partida_id = partida_id
        super().__init__("Partida não encontrada.")


class PartidaEmEstadoInvalido(ErroJogo):
    codigo = ErrorCode.PARTIDA_EM_ESTADO_INVALIDO


class AcaoRecusada(ErroJogo):
    codigo = ErrorCode.ACAO_RECUSADA


class CasoIndisponivel(ErroJogo):
    codigo = ErrorCode.CASO_INDISPONIVEL


class ProvedorIndisponivel(ErroJogo):
    codigo = ErrorCode.PROVEDOR_INDISPONIVEL


class FalhaNoLLM(ErroJogo):
    codigo = ErrorCode.FALHA_NO_LLM


class TempoEsgotadoNoLLM(FalhaNoLLM):
    codigo = ErrorCode.TEMPO_ESGOTADO_NO_LLM


class OrcamentoEstourado(ErroJogo):
    codigo = ErrorCode.ORCAMENTO_ESTOURADO
