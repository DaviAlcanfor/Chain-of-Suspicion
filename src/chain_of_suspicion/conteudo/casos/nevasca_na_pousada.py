from ...dominio.calendario import Calendario
from ...dominio.caso import (
    Alibi,
    Caso,
    CondicaoAcerto,
    Crime,
    Evento,
    Fato,
    Objetivo,
    Pista,
    Segredo,
)
from ...dominio.enums import MetodoCrime, Papel, TipoObjetivo, TipoPista
from ..caso_pronto import CasoPronto, ChaveCaso
from ..elenco.personas import ChavePersona as P
from ..mapas import POUSADA
from .construtor import DIAS_DO_CASO, PRIMEIRO_DIA, Ids, ator, escalar, estadia, hora, periodo

APRESENTACAO = (
    "Sexta-feira, 21h20. Na Pousada Serra Branca, cercada por uma nevasca que derrubou o "
    "telefone e fechou a estrada, o dono Joaquim Pires desabou no refeitório depois de "
    "tomar o chá da noite e não resistiu. Estavam na pousada a cozinheira Lia Moraes, a "
    "jornalista Beatriz Nogueira, o médico Dr. Renato Faria e a socialite Vera Lúcia "
    "Pinheiro. O inspetor aposentado Alencar Moura, hóspede, assumiu a investigação."
)

SOLUCAO = (
    "Lia desviava dinheiro da pousada havia anos e Joaquim descobriu pelos livros-caixa. "
    "Ela colheu raiz de cicuta no galpão, escondeu o frasco atrás das panelas e levou "
    "a bandeja de chá ao refeitório às 21h10. O Dr. Renato a viu mexendo num frasco na "
    "cozinha. Beatriz mente sobre o álibi porque revirava documentos do sótão atrás de uma "
    "reportagem (pista falsa). Provas decisivas: livro-caixa rasurado, bandeja só com as "
    "digitais de Lia e o frasco escondido."
)


def construir() -> CasoPronto:
    ids = Ids(ChaveCaso.NEVASCA_NA_POUSADA)
    L = POUSADA.id_do_local
    lia, joaquim = ids.personagem(P.LIA), ids.personagem(P.JOAQUIM)
    beatriz, renato = ids.personagem(P.BEATRIZ), ids.personagem(P.RENATO)
    vera, alencar = ids.personagem(P.VERA), ids.personagem(P.ALENCAR)
    desvio, cha, bandeja_f = (
        ids.fato("desvio_de_dinheiro"),
        ids.fato("cha_envenenado"),
        ids.fato("lia_levou_cha"),
    )
    sotao_f, renato_viu = ids.fato("beatriz_no_sotao"), ids.fato("renato_viu_frasco")
    frasco, bandeja, livro = ids.pista("frasco"), ids.pista("bandeja"), ids.pista("livro_caixa")
    cicuta, pasta, xicara = ids.pista("cicuta"), ids.pista("pasta"), ids.pista("xicara_extra")

    caso = Caso(
        id=ids.caso(),
        seed=5,
        calendario=Calendario(inicio=PRIMEIRO_DIA, dias=DIAS_DO_CASO),
        mapa=POUSADA.construir(),
        crime=Crime(
            vitima_id=joaquim,
            instante=hora("21:20"),
            local_id=L("refeitorio"),
            metodo=MetodoCrime.ENVENENAMENTO,
            motivo_fato_id=desvio,
        ),
        culpado_id=lia,
        fatos=[
            Fato(id=desvio, descricao="Joaquim descobriu que Lia desviava dinheiro da pousada"),
            Fato(
                id=cha,
                descricao="O chá do dono foi envenenado com raiz de cicuta colhida no galpão",
            ),
            Fato(id=bandeja_f, descricao="Lia levou a bandeja de chá ao refeitório às 21:10"),
            Fato(
                id=sotao_f,
                descricao="Beatriz revirava documentos no sótão em busca de uma reportagem",
            ),
            Fato(id=renato_viu, descricao="Renato viu Lia mexer num frasco sozinha na cozinha"),
        ],
        linha_do_tempo=[
            Evento(
                id=ids.evento("cha"),
                instante=hora("21:10"),
                local_id=L("refeitorio"),
                fato_id=bandeja_f,
            ),
            Evento(id=ids.evento("crime"), instante=hora("21:20"), local_id=L("refeitorio")),
        ],
        personagens=[
            ator(
                ids,
                P.LIA,
                Papel.ASSASSINO,
                objetivo=Objetivo(tipo=TipoObjetivo.EVITAR_ACUSACAO),
                sabe={desvio, cha, bandeja_f},
                segredos=[Segredo(fato_id=bandeja_f, revela_se=[frasco, bandeja])],
                limite_estresse=1.2,
            ),
            ator(
                ids,
                P.BEATRIZ,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.PROTEGER_SEGREDO, fato_id=sotao_f),
                sabe={sotao_f},
                segredos=[Segredo(fato_id=sotao_f, revela_se=[pasta])],
                limite_estresse=0.8,
            ),
            ator(
                ids,
                P.RENATO,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
                sabe={renato_viu},
            ),
            ator(ids, P.VERA, Papel.INOCENTE, objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR)),
            ator(
                ids,
                P.ALENCAR,
                Papel.DETETIVE,
                objetivo=Objetivo(tipo=TipoObjetivo.ENCONTRAR_CULPADO),
            ),
            ator(ids, P.JOAQUIM, Papel.VITIMA),
        ],
        agenda=[
            estadia(lia, L("cozinha"), periodo("20:40", "21:05")),
            estadia(lia, L("refeitorio"), periodo("21:10", "21:40")),
            estadia(joaquim, L("quarto_12"), periodo("20:30", "21:05")),
            estadia(joaquim, L("refeitorio"), periodo("21:10", "21:40")),
            estadia(beatriz, L("sotao"), periodo("20:40", "21:10")),
            estadia(beatriz, L("lareira"), periodo("21:15", "21:40")),
            estadia(renato, L("cozinha"), periodo("20:40", "21:00")),
            estadia(renato, L("lareira"), periodo("21:05", "21:40")),
            estadia(vera, L("lareira"), periodo("20:40", "21:40")),
        ],
        alibis=[
            Alibi(
                personagem_id=lia,
                local_id=L("cozinha"),
                periodo=periodo("20:50", "21:30"),
                desmentido_por=[bandeja_f],
            ),
            Alibi(
                personagem_id=beatriz,
                local_id=L("lareira"),
                periodo=periodo("20:45", "21:30"),
                desmentido_por=[sotao_f],
            ),
            Alibi(personagem_id=vera, local_id=L("lareira"), periodo=periodo("20:45", "21:35")),
        ],
        pistas=[
            Pista(
                id=frasco,
                descricao="Frasco de raiz moída escondido atrás das panelas",
                local_id=L("cozinha"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[cha],
            ),
            Pista(
                id=bandeja,
                descricao="Bandeja com a xícara do dono, só com as digitais de Lia",
                local_id=L("refeitorio"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[bandeja_f],
                exige_pistas=[frasco],
            ),
            Pista(
                id=livro,
                descricao="Livro-caixa com rasuras no quarto do dono",
                local_id=L("quarto_12"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[desvio],
            ),
            Pista(
                id=cicuta,
                descricao="Moitas de cicuta recém-arrancadas junto ao galpão",
                local_id=L("galpao"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[cha],
            ),
            Pista(
                id=pasta,
                descricao="Pasta de documentos revirada no sótão",
                local_id=L("sotao"),
                tipo=TipoPista.FALSA,
                aponta_para=[sotao_f],
            ),
            Pista(
                id=xicara,
                descricao="Xícara extra esquecida na lareira",
                local_id=L("lareira"),
                tipo=TipoPista.FALSA,
            ),
        ],
        cadeia_solucao=[desvio, cha, bandeja_f],
        condicao_acerto=CondicaoAcerto(
            culpado_id=lia,
            motivo_fato_id=desvio,
            provas_minimas=[livro, bandeja, frasco],
            quantas_provas=2,
        ),
    )
    return CasoPronto(
        chave=ChaveCaso.NEVASCA_NA_POUSADA,
        titulo="Nevasca na Pousada",
        mapa=POUSADA.chave,
        apresentacao=APRESENTACAO,
        solucao=SOLUCAO,
        entrada=L(POUSADA.entrada),
        escalacao={
            lia: escalar(P.LIA, "cozinheira da pousada"),
            beatriz: escalar(P.BEATRIZ, "jornalista hospedada"),
            renato: escalar(P.RENATO, "médico hospedado"),
            vera: escalar(P.VERA, "hóspede de longa data"),
            alencar: escalar(P.ALENCAR, "inspetor aposentado, hóspede"),
            joaquim: escalar(P.JOAQUIM, "dono da pousada e vítima"),
        },
        caso=caso,
    )
