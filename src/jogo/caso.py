from __future__ import annotations

from collections.abc import Sequence
from itertools import combinations, pairwise
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator

from .base import ModeloBase
from .calendario import Calendario
from .enums import MetodoCrime, Papel, TipoObjetivo, TipoPista
from .ids import CasoId, EventoId, FatoId, LocalId, PersonagemId, PistaId
from .mapa import Mapa
from .relogio import Intervalo

OBJETIVOS_PERMITIDOS: dict[Papel, frozenset[TipoObjetivo]] = {
    Papel.ASSASSINO: frozenset({TipoObjetivo.EVITAR_ACUSACAO}),
    Papel.DETETIVE: frozenset({TipoObjetivo.ENCONTRAR_CULPADO}),
    Papel.INOCENTE: frozenset({TipoObjetivo.PROTEGER_SEGREDO, TipoObjetivo.COLABORAR}),
    Papel.VITIMA: frozenset(),
}


class Fato(ModeloBase):
    id: FatoId
    descricao: str


class Evento(ModeloBase):
    id: EventoId
    instante: AwareDatetime
    local_id: LocalId
    fato_id: FatoId | None = None


class Crime(ModeloBase):
    vitima_id: PersonagemId
    instante: AwareDatetime
    local_id: LocalId
    metodo: MetodoCrime
    motivo_fato_id: FatoId


class Objetivo(ModeloBase):
    tipo: TipoObjetivo
    fato_id: FatoId | None = None

    @model_validator(mode="after")
    def _fato_so_para_proteger_segredo(self) -> Objetivo:
        protege_segredo = self.tipo == TipoObjetivo.PROTEGER_SEGREDO
        if protege_segredo and self.fato_id is None:
            raise ValueError("proteger segredo exige o fato protegido")
        if not protege_segredo and self.fato_id is not None:
            raise ValueError("só proteger segredo aponta para um fato")
        return self


class Segredo(ModeloBase):
    fato_id: FatoId
    revela_se: list[PistaId]


class Declaracao(ModeloBase):
    personagem_id: PersonagemId
    fato_id: FatoId
    afirmacao: str
    verdadeira: bool
    turno: int


class Personagem(ModeloBase):
    id: PersonagemId
    nome: str
    papel: Papel
    objetivo: Objetivo | None = None
    sabe: set[FatoId] = Field(default_factory=set)
    segredos: list[Segredo] = Field(default_factory=list)
    declaracoes: list[Declaracao] = Field(default_factory=list)
    estresse: float = Field(default=0.0, ge=0.0)
    limite_estresse: float = Field(default=1.0, gt=0.0)
    insistencias: int = Field(default=0, ge=0)
    hostil: bool = False

    @model_validator(mode="after")
    def _objetivo_combina_com_o_papel(self) -> Personagem:
        permitidos = OBJETIVOS_PERMITIDOS[self.papel]
        if not permitidos:
            if self.objetivo is not None:
                raise ValueError(f"{self.papel} não tem objetivo")
        elif self.objetivo is None or self.objetivo.tipo not in permitidos:
            raise ValueError(f"objetivo incompatível com o papel {self.papel}")
        return self


class Presenca(ModeloBase):
    personagem_id: PersonagemId
    local_id: LocalId
    periodo: Intervalo


class Alibi(ModeloBase):
    personagem_id: PersonagemId
    local_id: LocalId
    periodo: Intervalo
    desmentido_por: list[FatoId] = Field(default_factory=list)


class Pista(ModeloBase):
    id: PistaId
    descricao: str
    local_id: LocalId
    tipo: TipoPista
    aponta_para: list[FatoId] = Field(default_factory=list)
    exige_pistas: list[PistaId] = Field(default_factory=list)


class CondicaoAcerto(ModeloBase):
    culpado_id: PersonagemId
    motivo_fato_id: FatoId
    provas_minimas: list[PistaId]
    quantas_provas: int = Field(default=2, ge=1)


class Caso(ModeloBase):
    id: CasoId
    seed: int
    calendario: Calendario
    mapa: Mapa
    crime: Crime
    culpado_id: PersonagemId
    fatos: list[Fato]
    linha_do_tempo: list[Evento]
    personagens: list[Personagem]
    agenda: list[Presenca]
    alibis: list[Alibi]
    pistas: list[Pista]
    cadeia_solucao: list[FatoId]
    condicao_acerto: CondicaoAcerto

    @model_validator(mode="after")
    def _consistencia(self) -> Caso:
        self._checar_ids_unicos()
        self._checar_calendario()
        self._checar_papeis()
        self._checar_conhecimento()
        self._checar_locais()
        self._checar_agenda()
        self._checar_crime()
        self._checar_alibis()
        self._checar_pistas()
        self._checar_solucao()
        return self

    def personagem(self, personagem_id: PersonagemId) -> Personagem:
        return next(p for p in self.personagens if p.id == personagem_id)

    def fato(self, fato_id: FatoId) -> Fato:
        return next(f for f in self.fatos if f.id == fato_id)

    def estava_em(
        self, personagem_id: PersonagemId, local_id: LocalId, instante: AwareDatetime
    ) -> bool:
        return any(
            presenca.personagem_id == personagem_id
            and presenca.local_id == local_id
            and presenca.periodo.contem(instante)
            for presenca in self.agenda
        )

    def presentes_em(self, local_id: LocalId, instante: AwareDatetime) -> set[PersonagemId]:
        return {
            presenca.personagem_id
            for presenca in self.agenda
            if presenca.local_id == local_id and presenca.periodo.contem(instante)
        }

    def alibi_confere(self, alibi: Alibi) -> bool:
        return any(
            presenca.personagem_id == alibi.personagem_id
            and presenca.local_id == alibi.local_id
            and presenca.periodo.cobre(alibi.periodo)
            for presenca in self.agenda
        )

    def _com_papel(self, papel: Papel) -> list[Personagem]:
        return [p for p in self.personagens if p.papel == papel]

    def _ids_fatos(self) -> set[FatoId]:
        return {fato.id for fato in self.fatos}

    def _ids_pistas(self) -> set[PistaId]:
        return {pista.id for pista in self.pistas}

    def _agenda_de(self, personagem_id: PersonagemId) -> list[Presenca]:
        presencas = (p for p in self.agenda if p.personagem_id == personagem_id)
        return sorted(presencas, key=lambda p: p.periodo.inicio)

    def _checar_ids_unicos(self) -> None:
        colecoes: dict[str, Sequence[UUID]] = {
            "fatos": [fato.id for fato in self.fatos],
            "personagens": [personagem.id for personagem in self.personagens],
            "pistas": [pista.id for pista in self.pistas],
            "linha_do_tempo": [evento.id for evento in self.linha_do_tempo],
        }
        for nome, ids in colecoes.items():
            if len(ids) != len(set(ids)):
                raise ValueError(f"ids repetidos em {nome}")

    def _checar_calendario(self) -> None:
        janela = self.calendario.janela
        instantes = [self.crime.instante, *(e.instante for e in self.linha_do_tempo)]
        periodos = [
            *(p.periodo for p in self.agenda),
            *(a.periodo for a in self.alibis),
        ]
        if not all(janela.contem(instante) for instante in instantes):
            raise ValueError("crime ou evento fora dos dias do caso")
        if not all(janela.cobre(periodo) for periodo in periodos):
            raise ValueError("agenda ou álibi fora dos dias do caso")

    def _checar_papeis(self) -> None:
        for papel in (Papel.ASSASSINO, Papel.DETETIVE, Papel.VITIMA):
            if len(self._com_papel(papel)) != 1:
                raise ValueError(f"precisa haver exatamente um {papel}")
        if not self._com_papel(Papel.INOCENTE):
            raise ValueError("precisa haver ao menos um inocente")
        if self._com_papel(Papel.ASSASSINO)[0].id != self.culpado_id:
            raise ValueError("o culpado precisa ser o assassino")
        if self._com_papel(Papel.VITIMA)[0].id != self.crime.vitima_id:
            raise ValueError("a vítima do crime precisa ser a personagem vítima")

    def _checar_conhecimento(self) -> None:
        fatos = self._ids_fatos()
        pistas = self._ids_pistas()
        if self.crime.motivo_fato_id not in fatos:
            raise ValueError("motivo do crime aponta para fato inexistente")
        for personagem in self.personagens:
            if not personagem.sabe <= fatos:
                raise ValueError(f"{personagem.nome} sabe fato inexistente")
            for segredo in personagem.segredos:
                self._checar_segredo(personagem, segredo, pistas)
            self._checar_objetivo(personagem)

    @staticmethod
    def _checar_segredo(
        personagem: Personagem, segredo: Segredo, pistas: set[PistaId]
    ) -> None:
        if segredo.fato_id not in personagem.sabe:
            raise ValueError(f"{personagem.nome} guarda segredo que não sabe")
        if not set(segredo.revela_se) <= pistas:
            raise ValueError(f"segredo de {personagem.nome} exige pista inexistente")

    @staticmethod
    def _checar_objetivo(personagem: Personagem) -> None:
        objetivo = personagem.objetivo
        if objetivo is None or objetivo.fato_id is None:
            return
        if objetivo.fato_id not in {s.fato_id for s in personagem.segredos}:
            raise ValueError(f"{personagem.nome} protege fato que não é segredo seu")

    def _checar_locais(self) -> None:
        locais = {
            "crime": [self.crime.local_id],
            "linha_do_tempo": [e.local_id for e in self.linha_do_tempo],
            "agenda": [p.local_id for p in self.agenda],
            "alibis": [a.local_id for a in self.alibis],
            "pistas": [p.local_id for p in self.pistas],
        }
        for origem, ids in locais.items():
            if not all(self.mapa.existe(local_id) for local_id in ids):
                raise ValueError(f"{origem} cita local inexistente")
        fatos = self._ids_fatos()
        if any(e.fato_id and e.fato_id not in fatos for e in self.linha_do_tempo):
            raise ValueError("linha_do_tempo cita fato inexistente")

    def _checar_agenda(self) -> None:
        com_agenda = {p.id for p in self.personagens if p.papel != Papel.DETETIVE}
        if {p.personagem_id for p in self.agenda} - com_agenda:
            raise ValueError("agenda de personagem que não deveria ter agenda")
        for personagem_id in com_agenda:
            presencas = self._agenda_de(personagem_id)
            nome = self.personagem(personagem_id).nome
            if not presencas:
                raise ValueError(f"{nome} está sem agenda")
            self._checar_sem_sobreposicao(nome, presencas)
            self._checar_deslocamento(nome, presencas)

    @staticmethod
    def _checar_sem_sobreposicao(nome: str, presencas: list[Presenca]) -> None:
        for a, b in combinations(presencas, 2):
            if a.periodo.sobrepoe(b.periodo):
                raise ValueError(f"{nome} está em dois lugares ao mesmo tempo")

    def _checar_deslocamento(self, nome: str, presencas: list[Presenca]) -> None:
        for atual, seguinte in pairwise(presencas):
            necessario = self.mapa.tempo_minimo(atual.local_id, seguinte.local_id)
            folga = seguinte.periodo.inicio - atual.periodo.fim
            if necessario is None or folga < necessario:
                origem = self.mapa.nome(atual.local_id)
                destino = self.mapa.nome(seguinte.local_id)
                raise ValueError(f"{nome} não tem tempo de ir de {origem} para {destino}")

    def _checar_crime(self) -> None:
        for personagem_id in (self.culpado_id, self.crime.vitima_id):
            if not self.estava_em(personagem_id, self.crime.local_id, self.crime.instante):
                raise ValueError(
                    "assassino e vítima precisam estar no local do crime na hora do crime"
                )

    def _checar_alibis(self) -> None:
        fatos = self._ids_fatos()
        for alibi in self.alibis:
            nome = self.personagem(alibi.personagem_id).nome
            if not set(alibi.desmentido_por) <= fatos:
                raise ValueError(f"álibi de {nome} cita fato inexistente")
            confere = self.alibi_confere(alibi)
            if not confere and not alibi.desmentido_por:
                raise ValueError(f"álibi falso de {nome} sem fato que o desminta")
            if confere and alibi.desmentido_por:
                raise ValueError(f"álibi verdadeiro de {nome} não pode ser desmentido")

    def _checar_pistas(self) -> None:
        fatos = self._ids_fatos()
        pistas = self._ids_pistas()
        for pista in self.pistas:
            if not set(pista.aponta_para) <= fatos:
                raise ValueError(f"pista {pista.descricao} aponta para fato inexistente")
            if not set(pista.exige_pistas) <= pistas:
                raise ValueError(f"pista {pista.descricao} exige pista inexistente")
        if pistas - _pistas_alcancaveis(self.pistas):
            raise ValueError("há pistas inalcançáveis")

    def _checar_solucao(self) -> None:
        if not set(self.cadeia_solucao) <= self._ids_fatos():
            raise ValueError("cadeia de solução cita fato inexistente")
        cobertos = {
            fato_id
            for pista in self.pistas
            if pista.tipo == TipoPista.RELEVANTE
            for fato_id in pista.aponta_para
        }
        if not set(self.cadeia_solucao) <= cobertos:
            raise ValueError("há fato da cadeia sem nenhuma pista relevante")
        self._checar_condicao_de_acerto()

    def _checar_condicao_de_acerto(self) -> None:
        condicao = self.condicao_acerto
        if condicao.culpado_id != self.culpado_id:
            raise ValueError("condição de acerto com culpado diferente")
        if condicao.motivo_fato_id != self.crime.motivo_fato_id:
            raise ValueError("condição de acerto com motivo diferente")
        provas = set(condicao.provas_minimas)
        if not provas <= self._ids_pistas() or len(provas) < condicao.quantas_provas:
            raise ValueError("provas mínimas inválidas")


def _pistas_alcancaveis(pistas: list[Pista]) -> set[PistaId]:
    achadas: set[PistaId] = set()
    mudou = True
    while mudou:
        mudou = False
        for pista in pistas:
            if pista.id not in achadas and set(pista.exige_pistas) <= achadas:
                achadas.add(pista.id)
                mudou = True
    return achadas
