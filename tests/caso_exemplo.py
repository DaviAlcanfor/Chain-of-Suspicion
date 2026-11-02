from datetime import UTC, datetime, timedelta
from typing import Any

from chain_of_suspicion.dominio.calendario import Calendario
from chain_of_suspicion.dominio.caso import (
    Alibi,
    Caso,
    CondicaoAcerto,
    Crime,
    Evento,
    Fato,
    Objetivo,
    Personagem,
    Pista,
    Presenca,
    Segredo,
)
from chain_of_suspicion.dominio.enums import MetodoCrime, Papel, TipoObjetivo, TipoPista
from chain_of_suspicion.dominio.ids import GeradorIds
from chain_of_suspicion.dominio.mapa import Conexao, Local, Mapa
from chain_of_suspicion.dominio.relogio import Intervalo

_ids = GeradorIds(42)

BIBLIOTECA, CORREDOR, COZINHA, ESCRITORIO, JARDIM, QUARTO = (
    _ids.local() for _ in range(6)
)
MARTA, PAULO, LIA, CAIO, INSPETOR, ALVES = (_ids.personagem() for _ in range(6))
F_DIVIDA, F_VENENO, F_BIBLIO, F_CARTA, F_LIA_COZINHA = (_ids.fato() for _ in range(5))
P_COPO, P_CAMERA, P_EXTRATO, P_JARDIM, P_CARTA, P_LUVAS = (_ids.pista() for _ in range(6))
E_BIBLIO, E_CRIME = (_ids.evento() for _ in range(2))
CASO_ID = _ids.caso()


PRIMEIRO_DIA = datetime(2026, 10, 30, tzinfo=UTC)
DIAS_DO_CASO = 3


def hora(texto: str, dia: int = 1) -> datetime:
    horas, minutos = map(int, texto.split(":"))
    return PRIMEIRO_DIA + timedelta(days=dia - 1, hours=horas, minutes=minutos)


def janela(de: str, ate: str) -> Intervalo:
    return Intervalo(inicio=hora(de), fim=hora(ate))


def _minutos(quantidade: int) -> timedelta:
    return timedelta(minutes=quantidade)


def _mapa() -> Mapa:
    return Mapa(
        locais=[
            Local(id=BIBLIOTECA, nome="Biblioteca"),
            Local(id=CORREDOR, nome="Corredor"),
            Local(id=COZINHA, nome="Cozinha"),
            Local(id=ESCRITORIO, nome="Escritório"),
            Local(id=JARDIM, nome="Jardim"),
            Local(id=QUARTO, nome="Quarto"),
        ],
        conexoes=[
            Conexao(origem=BIBLIOTECA, destino=CORREDOR, tempo=_minutos(1)),
            Conexao(origem=COZINHA, destino=CORREDOR, tempo=_minutos(1)),
            Conexao(origem=ESCRITORIO, destino=CORREDOR, tempo=_minutos(2)),
            Conexao(origem=QUARTO, destino=CORREDOR, tempo=_minutos(2)),
            Conexao(origem=JARDIM, destino=COZINHA, tempo=_minutos(2)),
        ],
    )


def _personagens() -> list[Personagem]:
    return [
        Personagem(
            id=MARTA,
            nome="Marta",
            papel=Papel.ASSASSINO,
            objetivo=Objetivo(tipo=TipoObjetivo.EVITAR_ACUSACAO),
            sabe={F_DIVIDA, F_VENENO, F_BIBLIO},
            segredos=[Segredo(fato_id=F_BIBLIO, revela_se=[P_COPO, P_CAMERA])],
            limite_estresse=1.5,
        ),
        Personagem(
            id=PAULO,
            nome="Paulo",
            papel=Papel.INOCENTE,
            objetivo=Objetivo(tipo=TipoObjetivo.PROTEGER_SEGREDO, fato_id=F_CARTA),
            sabe={F_CARTA, F_LIA_COZINHA},
            segredos=[Segredo(fato_id=F_CARTA, revela_se=[P_CARTA])],
            limite_estresse=0.8,
        ),
        Personagem(
            id=LIA,
            nome="Lia",
            papel=Papel.INOCENTE,
            objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
            sabe={F_LIA_COZINHA},
        ),
        Personagem(
            id=CAIO,
            nome="Caio",
            papel=Papel.INOCENTE,
            objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
        ),
        Personagem(
            id=INSPETOR,
            nome="Inspetor",
            papel=Papel.DETETIVE,
            objetivo=Objetivo(tipo=TipoObjetivo.ENCONTRAR_CULPADO),
        ),
        Personagem(id=ALVES, nome="Sr. Alves", papel=Papel.VITIMA),
    ]


def _agenda() -> list[Presenca]:
    return [
        Presenca(personagem_id=MARTA, local_id=QUARTO, periodo=janela("21:30", "21:50")),
        Presenca(personagem_id=MARTA, local_id=BIBLIOTECA, periodo=janela("21:55", "22:30")),
        Presenca(personagem_id=ALVES, local_id=ESCRITORIO, periodo=janela("21:00", "21:45")),
        Presenca(personagem_id=ALVES, local_id=BIBLIOTECA, periodo=janela("21:50", "22:30")),
        Presenca(personagem_id=PAULO, local_id=QUARTO, periodo=janela("21:30", "21:45")),
        Presenca(personagem_id=PAULO, local_id=COZINHA, periodo=janela("21:50", "22:30")),
        Presenca(personagem_id=LIA, local_id=COZINHA, periodo=janela("21:30", "22:30")),
        Presenca(personagem_id=CAIO, local_id=JARDIM, periodo=janela("21:30", "22:30")),
    ]


def _alibis() -> list[Alibi]:
    return [
        Alibi(
            personagem_id=MARTA,
            local_id=QUARTO,
            periodo=janela("21:35", "22:20"),
            desmentido_por=[F_BIBLIO],
        ),
        Alibi(
            personagem_id=PAULO,
            local_id=COZINHA,
            periodo=janela("21:30", "22:30"),
            desmentido_por=[F_CARTA],
        ),
        Alibi(personagem_id=LIA, local_id=COZINHA, periodo=janela("21:30", "22:30")),
    ]


def _pistas() -> list[Pista]:
    return [
        Pista(
            id=P_COPO,
            descricao="Copo com resíduo",
            local_id=BIBLIOTECA,
            tipo=TipoPista.RELEVANTE,
            aponta_para=[F_VENENO],
        ),
        Pista(
            id=P_CAMERA,
            descricao="Imagem de Marta entrando",
            local_id=CORREDOR,
            tipo=TipoPista.RELEVANTE,
            aponta_para=[F_BIBLIO],
            exige_pistas=[P_COPO],
        ),
        Pista(
            id=P_EXTRATO,
            descricao="Extrato com dívida",
            local_id=ESCRITORIO,
            tipo=TipoPista.RELEVANTE,
            aponta_para=[F_DIVIDA],
        ),
        Pista(
            id=P_JARDIM,
            descricao="Planta venenosa no jardim",
            local_id=JARDIM,
            tipo=TipoPista.RELEVANTE,
            aponta_para=[F_VENENO],
        ),
        Pista(
            id=P_CARTA,
            descricao="Carta escondida",
            local_id=QUARTO,
            tipo=TipoPista.FALSA,
            aponta_para=[F_CARTA],
        ),
        Pista(
            id=P_LUVAS,
            descricao="Luvas na lixeira",
            local_id=COZINHA,
            tipo=TipoPista.FALSA,
        ),
    ]


def construir_caso() -> Caso:
    return Caso(
        id=CASO_ID,
        seed=42,
        calendario=Calendario(inicio=PRIMEIRO_DIA, dias=DIAS_DO_CASO),
        mapa=_mapa(),
        crime=Crime(
            vitima_id=ALVES,
            instante=hora("22:10"),
            local_id=BIBLIOTECA,
            metodo=MetodoCrime.ENVENENAMENTO,
            motivo_fato_id=F_DIVIDA,
        ),
        culpado_id=MARTA,
        fatos=[
            Fato(id=F_DIVIDA, descricao="Marta devia dinheiro ao Sr. Alves"),
            Fato(id=F_VENENO, descricao="O veneno veio do jardim da casa"),
            Fato(id=F_BIBLIO, descricao="Marta entrou na biblioteca às 21:55"),
            Fato(id=F_CARTA, descricao="Paulo escondeu uma carta no quarto"),
            Fato(id=F_LIA_COZINHA, descricao="Lia ficou na cozinha das 21:30 às 22:30"),
        ],
        linha_do_tempo=[
            Evento(id=E_BIBLIO, instante=hora("21:55"), local_id=BIBLIOTECA, fato_id=F_BIBLIO),
            Evento(id=E_CRIME, instante=hora("22:10"), local_id=BIBLIOTECA),
        ],
        personagens=_personagens(),
        agenda=_agenda(),
        alibis=_alibis(),
        pistas=_pistas(),
        cadeia_solucao=[F_DIVIDA, F_VENENO, F_BIBLIO],
        condicao_acerto=CondicaoAcerto(
            culpado_id=MARTA,
            motivo_fato_id=F_DIVIDA,
            provas_minimas=[P_EXTRATO, P_CAMERA, P_COPO],
            quantas_provas=2,
        ),
    )


CASO = construir_caso()


def variar(**mudancas: Any) -> Caso:
    return Caso.model_validate(CASO.model_dump() | mudancas)
