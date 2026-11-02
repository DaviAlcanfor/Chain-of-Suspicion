from __future__ import annotations

from typing import Protocol

from pydantic import Field

from .base import ModeloBase
from .caso import Caso, Declaracao, Objetivo, Personagem, Segredo
from .enums import Papel, TipoPressao
from .ids import FatoId, LocalId, PersonagemId, PistaId
from .relogio import Intervalo

PESO_PRESSAO = {
    TipoPressao.CONFRONTAR_PROVA: 0.5,
    TipoPressao.APONTAR_CONTRADICAO: 0.4,
    TipoPressao.INSISTIR: 0.1,
}
INSISTENCIAS_ATE_TRAVAR = 3
MARGEM_INCERTEZA = 0.15
CERTEZA_NEUTRA = 0.5


class Pressao(ModeloBase):
    tipo: TipoPressao
    prova_id: PistaId | None = None


class DecisaoAmeaca(ModeloBase):
    ameaca: float = Field(ge=0.0, le=1.0)


class DecisaoContradicao(ModeloBase):
    contradiz: bool
    confianca: float = Field(ge=0.0, le=1.0)


class EstadoJogador(ModeloBase):
    pistas: set[PistaId] = Field(default_factory=set)
    depoimentos: list[Declaracao] = Field(default_factory=list)
    turno: int = 0


class VisaoPersonagem(ModeloBase):
    nome: str
    papel: Papel
    objetivo: Objetivo | None
    fatos_que_sabe: list[str]
    segredos: list[str]
    onde_estive: list[str]
    alibi_declarado: str | None
    o_que_ja_disse: list[str]
    estresse: float
    hostil: bool


class Acusacao(ModeloBase):
    culpado_id: PersonagemId
    motivo_fato_id: FatoId
    provas: list[PistaId]


class Veredito(ModeloBase):
    correta: bool


class Juiz(Protocol):
    def julgar(self, caso: Caso, estado: EstadoJogador, acusacao: Acusacao) -> Veredito: ...


class JuizDeterministico:
    def julgar(self, caso: Caso, estado: EstadoJogador, acusacao: Acusacao) -> Veredito:
        condicao = caso.condicao_acerto
        provas = set(acusacao.provas)
        if not provas <= estado.pistas:
            return Veredito(correta=False)
        provas_validas = provas & set(condicao.provas_minimas)
        acertou = (
            acusacao.culpado_id == condicao.culpado_id
            and acusacao.motivo_fato_id == condicao.motivo_fato_id
            and len(provas_validas) >= condicao.quantas_provas
        )
        return Veredito(correta=acertou)


def aplicar_pressao(
    personagem: Personagem, pressao: Pressao, ameaca: float
) -> Segredo | None:
    if personagem.hostil:
        return None
    _registrar_insistencia(personagem, pressao)
    if personagem.hostil:
        return None
    personagem.estresse += PESO_PRESSAO[pressao.tipo] * _ameaca_confiavel(ameaca)
    return _segredo_liberado(personagem, pressao)


def _registrar_insistencia(personagem: Personagem, pressao: Pressao) -> None:
    if pressao.tipo != TipoPressao.INSISTIR:
        personagem.insistencias = 0
        return
    personagem.insistencias += 1
    personagem.hostil = personagem.insistencias > INSISTENCIAS_ATE_TRAVAR


def _ameaca_confiavel(ameaca: float) -> float:
    incerta = abs(ameaca - CERTEZA_NEUTRA) < MARGEM_INCERTEZA
    return 0.0 if incerta else ameaca


def _segredo_liberado(personagem: Personagem, pressao: Pressao) -> Segredo | None:
    if personagem.estresse < personagem.limite_estresse or pressao.prova_id is None:
        return None
    return next(
        (s for s in personagem.segredos if pressao.prova_id in s.revela_se), None
    )


def visao_do_personagem(caso: Caso, personagem_id: PersonagemId) -> VisaoPersonagem:
    personagem = caso.personagem(personagem_id)
    return VisaoPersonagem(
        nome=personagem.nome,
        papel=personagem.papel,
        objetivo=personagem.objetivo,
        fatos_que_sabe=[caso.fato(f).descricao for f in sorted(personagem.sabe)],
        segredos=[caso.fato(s.fato_id).descricao for s in personagem.segredos],
        onde_estive=_onde_estive(caso, personagem_id),
        alibi_declarado=_alibi_declarado(caso, personagem_id),
        o_que_ja_disse=[d.afirmacao for d in personagem.declaracoes],
        estresse=personagem.estresse,
        hostil=personagem.hostil,
    )


def _onde_estive(caso: Caso, personagem_id: PersonagemId) -> list[str]:
    return [
        _descrever(caso, presenca.local_id, presenca.periodo)
        for presenca in caso.agenda
        if presenca.personagem_id == personagem_id
    ]


def _alibi_declarado(caso: Caso, personagem_id: PersonagemId) -> str | None:
    return next(
        (
            _descrever(caso, alibi.local_id, alibi.periodo)
            for alibi in caso.alibis
            if alibi.personagem_id == personagem_id
        ),
        None,
    )


def _descrever(caso: Caso, local_id: LocalId, periodo: Intervalo) -> str:
    inicio = caso.calendario.descrever(periodo.inicio)
    fim = caso.calendario.descrever(periodo.fim)
    return f"{caso.mapa.nome(local_id)}, de {inicio} até {fim}"
