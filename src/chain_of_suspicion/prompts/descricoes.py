from ..dominio.enums import TipoAcao

DESCRICAO_DA_ACAO: dict[TipoAcao, str] = {
    TipoAcao.MOVER: "ir para um local vizinho",
    TipoAcao.CONVERSAR: "puxar conversa com alguém que está no mesmo local",
    TipoAcao.OBSERVAR: "ficar atento ao que acontece ao redor, sem falar nem sair do lugar",
    TipoAcao.ESPERAR: "não fazer nada de especial neste momento",
    TipoAcao.MATAR: "matar a vítima, que precisa estar no mesmo local",
    TipoAcao.ESCONDER_EVIDENCIA: "esconder uma pista no local em que está",
    TipoAcao.CULPAR_OUTRO: "plantar suspeita sobre outra pessoa presente",
    TipoAcao.EXAMINAR_LOCAL: "vasculhar o local em que está atrás de pistas",
    TipoAcao.INTERROGAR: "fazer perguntas diretas a alguém que está no mesmo local",
    TipoAcao.PRESSIONAR: "pressionar alguém para que revele o que esconde",
    TipoAcao.APRESENTAR_PROVA: "mostrar uma pista a alguém para confrontá-lo",
    TipoAcao.ACUSAR: "acusar alguém formalmente de ser o culpado",
}

ACOES_COM_FALA = frozenset(
    {
        TipoAcao.CONVERSAR,
        TipoAcao.CULPAR_OUTRO,
        TipoAcao.INTERROGAR,
        TipoAcao.PRESSIONAR,
        TipoAcao.APRESENTAR_PROVA,
        TipoAcao.ACUSAR,
    }
)
