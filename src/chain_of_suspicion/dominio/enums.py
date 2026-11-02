from enum import StrEnum


class Papel(StrEnum):
    DETETIVE = "detetive"
    ASSASSINO = "assassino"
    INOCENTE = "inocente"
    VITIMA = "vitima"


class PeriodoDoDia(StrEnum):
    MADRUGADA = "madrugada"
    MANHA = "manha"
    TARDE = "tarde"
    NOITE = "noite"


class TipoPista(StrEnum):
    RELEVANTE = "relevante"
    FALSA = "falsa"


class TipoPressao(StrEnum):
    CONFRONTAR_PROVA = "confrontar_prova"
    APONTAR_CONTRADICAO = "apontar_contradicao"
    INSISTIR = "insistir"


class MetodoCrime(StrEnum):
    ENVENENAMENTO = "envenenamento"
    ARMA_BRANCA = "arma_branca"
    ARMA_DE_FOGO = "arma_de_fogo"
    ESTRANGULAMENTO = "estrangulamento"


class TipoObjetivo(StrEnum):
    EVITAR_ACUSACAO = "evitar_acusacao"
    PROTEGER_SEGREDO = "proteger_segredo"
    COLABORAR = "colaborar"
    ENCONTRAR_CULPADO = "encontrar_culpado"


class TipoAcao(StrEnum):
    MOVER = "mover"
    CONVERSAR = "conversar"
    OBSERVAR = "observar"
    ESPERAR = "esperar"
    MATAR = "matar"
    ESCONDER_EVIDENCIA = "esconder_evidencia"
    CULPAR_OUTRO = "culpar_outro"
    EXAMINAR_LOCAL = "examinar_local"
    INTERROGAR = "interrogar"
    PRESSIONAR = "pressionar"
    APRESENTAR_PROVA = "apresentar_prova"
    ACUSAR = "acusar"
