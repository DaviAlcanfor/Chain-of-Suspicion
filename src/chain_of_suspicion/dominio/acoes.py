from __future__ import annotations

from pydantic import model_validator

from .base import ModeloBase
from .enums import Papel, TipoAcao
from .ids import LocalId, PersonagemId, PistaId
from .mundo import Mundo

ACOES_COMUNS = frozenset(
    {TipoAcao.MOVER, TipoAcao.CONVERSAR, TipoAcao.OBSERVAR, TipoAcao.ESPERAR}
)

PERMISSOES: dict[Papel, frozenset[TipoAcao]] = {
    Papel.INOCENTE: ACOES_COMUNS,
    Papel.ASSASSINO: ACOES_COMUNS
    | {TipoAcao.MATAR, TipoAcao.ESCONDER_EVIDENCIA, TipoAcao.CULPAR_OUTRO},
    Papel.DETETIVE: ACOES_COMUNS
    | {
        TipoAcao.EXAMINAR_LOCAL,
        TipoAcao.INTERROGAR,
        TipoAcao.PRESSIONAR,
        TipoAcao.APRESENTAR_PROVA,
        TipoAcao.ACUSAR,
    },
    Papel.VITIMA: frozenset(),
}

CAMPOS_EXIGIDOS: dict[TipoAcao, tuple[str, ...]] = {
    TipoAcao.MOVER: ("alvo_local_id",),
    TipoAcao.CONVERSAR: ("alvo_personagem_id",),
    TipoAcao.MATAR: ("alvo_personagem_id",),
    TipoAcao.CULPAR_OUTRO: ("alvo_personagem_id",),
    TipoAcao.ESCONDER_EVIDENCIA: ("alvo_local_id", "pista_id"),
    TipoAcao.EXAMINAR_LOCAL: ("alvo_local_id",),
    TipoAcao.INTERROGAR: ("alvo_personagem_id",),
    TipoAcao.PRESSIONAR: ("alvo_personagem_id",),
    TipoAcao.APRESENTAR_PROVA: ("alvo_personagem_id", "pista_id"),
    TipoAcao.ACUSAR: ("alvo_personagem_id",),
}

EXIGEM_MESMO_LOCAL_DO_ALVO = frozenset(
    {
        TipoAcao.CONVERSAR,
        TipoAcao.MATAR,
        TipoAcao.INTERROGAR,
        TipoAcao.PRESSIONAR,
        TipoAcao.APRESENTAR_PROVA,
    }
)

EXIGEM_ESTAR_NO_LOCAL_ALVO = frozenset(
    {TipoAcao.EXAMINAR_LOCAL, TipoAcao.ESCONDER_EVIDENCIA}
)


class AcaoInvalida(ValueError):
    pass


class Acao(ModeloBase):
    tipo: TipoAcao
    ator_id: PersonagemId
    alvo_personagem_id: PersonagemId | None = None
    alvo_local_id: LocalId | None = None
    pista_id: PistaId | None = None

    @model_validator(mode="after")
    def _campos_do_tipo(self) -> Acao:
        for campo in CAMPOS_EXIGIDOS.get(self.tipo, ()):
            if getattr(self, campo) is None:
                raise ValueError(f"{self.tipo} exige {campo}")
        return self


def validar_acao(mundo: Mundo, acao: Acao) -> None:
    ator = mundo.caso.personagem(acao.ator_id)
    if acao.ator_id in mundo.mortos:
        raise AcaoInvalida("quem morreu não age")
    if acao.tipo not in PERMISSOES[ator.papel]:
        raise AcaoInvalida(f"{ator.papel} não pode {acao.tipo}")
    if acao.tipo in EXIGEM_MESMO_LOCAL_DO_ALVO:
        _validar_mesmo_local(mundo, acao)
    if acao.tipo in EXIGEM_ESTAR_NO_LOCAL_ALVO:
        _validar_estar_no_local(mundo, acao)
    if acao.tipo == TipoAcao.MOVER:
        _validar_movimento(mundo, acao)
    if acao.tipo == TipoAcao.MATAR:
        _validar_morte(mundo, acao)


def aplicar_acao(mundo: Mundo, acao: Acao) -> None:
    validar_acao(mundo, acao)
    if acao.tipo == TipoAcao.MOVER and acao.alvo_local_id is not None:
        mundo.colocar(acao.ator_id, acao.alvo_local_id)
    if acao.tipo == TipoAcao.MATAR and acao.alvo_personagem_id is not None:
        mundo.mortos.add(acao.alvo_personagem_id)


def _posicao(mundo: Mundo, personagem_id: PersonagemId) -> LocalId:
    posicao = mundo.posicoes.get(personagem_id)
    if posicao is None:
        nome = mundo.caso.personagem(personagem_id).nome
        raise AcaoInvalida(f"{nome} não está em nenhum local agora")
    return posicao


def _validar_mesmo_local(mundo: Mundo, acao: Acao) -> None:
    alvo_id = acao.alvo_personagem_id
    if alvo_id is None:
        return
    if alvo_id in mundo.mortos:
        raise AcaoInvalida("o alvo já morreu")
    if _posicao(mundo, acao.ator_id) != _posicao(mundo, alvo_id):
        raise AcaoInvalida("ator e alvo precisam estar no mesmo local")


def _validar_estar_no_local(mundo: Mundo, acao: Acao) -> None:
    if _posicao(mundo, acao.ator_id) != acao.alvo_local_id:
        raise AcaoInvalida("o ator precisa estar no local da ação")


def _validar_movimento(mundo: Mundo, acao: Acao) -> None:
    origem = _posicao(mundo, acao.ator_id)
    if acao.alvo_local_id not in mundo.caso.mapa.vizinhos(origem):
        raise AcaoInvalida("não há caminho direto até o destino")


def _validar_morte(mundo: Mundo, acao: Acao) -> None:
    if acao.alvo_personagem_id != mundo.caso.crime.vitima_id:
        raise AcaoInvalida("só a vítima do caso pode ser morta")
