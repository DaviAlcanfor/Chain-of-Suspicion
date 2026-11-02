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
from ..mapas import MANSAO
from .construtor import (
    DIAS_DO_CASO,
    PRIMEIRO_DIA,
    Ids,
    ator,
    escalar,
    estadia,
    hora,
    periodo,
)

APRESENTACAO = (
    "Sexta-feira, 23h00. Na Mansão Villaça, o patriarca Otávio Alves reuniu a família para "
    "anunciar mudanças no testamento. Pouco depois foi encontrado morto no escritório, com "
    "um golpe no peito. Estavam na casa o médico da família, Dr. Renato Faria; a herdeira "
    "Vera Lúcia Pinheiro; o sobrinho Caio Teles; e o caseiro Joaquim Pires. A delegada "
    "Helena Duarte assumiu o caso. A tempestade derrubou a linha telefônica e ninguém pode sair."
)

SOLUCAO = (
    "O Dr. Renato desviava medicamentos controlados da família havia anos. Otávio descobriu "
    "e ia denunciá-lo ao conselho de medicina e mudar o testamento. Renato pegou o abridor "
    "de cartas de prata e atacou Otávio no escritório às 23h. Joaquim ouviu passos apressados "
    "no hall; a manga do paletó de Renato ficou suja. Vera tem dívidas de jogo e telefonou "
    "escondida a um agiota (pista falsa). Provas decisivas: anotações de Otávio, o abridor "
    "sumido e o lenço manchado."
)


def construir() -> CasoPronto:
    ids = Ids(ChaveCaso.O_TESTAMENTO)
    L = MANSAO.id_do_local
    renato, otavio = ids.personagem(P.RENATO), ids.personagem(P.OTAVIO)
    vera, caio = ids.personagem(P.VERA), ids.personagem(P.CAIO)
    joaquim, helena = ids.personagem(P.JOAQUIM), ids.personagem(P.HELENA)
    desvio, abridor = ids.fato("desvio"), ids.fato("abridor")
    renato_escritorio, ligacao = ids.fato("renato_escritorio"), ids.fato("ligacao_de_vera")
    passos = ids.fato("passos")
    anotacoes, lenco, abridor_p = ids.pista("anotacoes"), ids.pista("lenco"), ids.pista("abridor")
    recibo, taca = ids.pista("recibo"), ids.pista("taca")

    caso = Caso(
        id=ids.caso(),
        seed=2,
        calendario=Calendario(inicio=PRIMEIRO_DIA, dias=DIAS_DO_CASO),
        mapa=MANSAO.construir(),
        crime=Crime(
            vitima_id=otavio,
            instante=hora("23:00"),
            local_id=L("escritorio"),
            metodo=MetodoCrime.ARMA_BRANCA,
            motivo_fato_id=desvio,
        ),
        culpado_id=renato,
        fatos=[
            Fato(
                id=desvio,
                descricao="Otávio descobriu que Renato desviava medicamentos controlados e ia denunciá-lo",
            ),
            Fato(id=abridor, descricao="O abridor de cartas de prata sumiu da mesa do escritório"),
            Fato(
                id=renato_escritorio,
                descricao="Renato entrou no escritório às 22:50 e saiu com a manga suja",
            ),
            Fato(
                id=ligacao,
                descricao="Vera saiu do quarto às 22:50 para telefonar escondida a um agiota",
            ),
            Fato(
                id=passos, descricao="Joaquim ouviu passos apressados vindos do escritório às 23:00"
            ),
        ],
        linha_do_tempo=[
            Evento(
                id=ids.evento("entrada"),
                instante=hora("22:50"),
                local_id=L("escritorio"),
                fato_id=renato_escritorio,
            ),
            Evento(id=ids.evento("crime"), instante=hora("23:00"), local_id=L("escritorio")),
        ],
        personagens=[
            ator(
                ids,
                P.RENATO,
                Papel.ASSASSINO,
                objetivo=Objetivo(tipo=TipoObjetivo.EVITAR_ACUSACAO),
                sabe={desvio, abridor, renato_escritorio},
                segredos=[Segredo(fato_id=renato_escritorio, revela_se=[abridor_p, lenco])],
                limite_estresse=1.4,
            ),
            ator(
                ids,
                P.VERA,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.PROTEGER_SEGREDO, fato_id=ligacao),
                sabe={ligacao},
                segredos=[Segredo(fato_id=ligacao, revela_se=[recibo])],
                limite_estresse=0.7,
            ),
            ator(ids, P.CAIO, Papel.INOCENTE, objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR)),
            ator(
                ids,
                P.JOAQUIM,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
                sabe={passos},
            ),
            ator(
                ids,
                P.HELENA,
                Papel.DETETIVE,
                objetivo=Objetivo(tipo=TipoObjetivo.ENCONTRAR_CULPADO),
            ),
            ator(ids, P.OTAVIO, Papel.VITIMA),
        ],
        agenda=[
            estadia(renato, L("sala_de_jantar"), periodo("22:20", "22:40")),
            estadia(renato, L("escritorio"), periodo("22:50", "23:20")),
            estadia(otavio, L("biblioteca"), periodo("22:00", "22:35")),
            estadia(otavio, L("escritorio"), periodo("22:45", "23:20")),
            estadia(vera, L("quarto"), periodo("22:20", "22:50")),
            estadia(vera, L("jardim"), periodo("23:00", "23:20")),
            estadia(caio, L("sala_de_jantar"), periodo("22:20", "23:20")),
            estadia(joaquim, L("hall"), periodo("22:20", "23:20")),
        ],
        alibis=[
            Alibi(
                personagem_id=renato,
                local_id=L("sala_de_jantar"),
                periodo=periodo("22:30", "23:10"),
                desmentido_por=[renato_escritorio],
            ),
            Alibi(
                personagem_id=vera,
                local_id=L("quarto"),
                periodo=periodo("22:20", "23:10"),
                desmentido_por=[ligacao],
            ),
            Alibi(
                personagem_id=caio, local_id=L("sala_de_jantar"), periodo=periodo("22:30", "23:10")
            ),
            Alibi(personagem_id=joaquim, local_id=L("hall"), periodo=periodo("22:20", "23:20")),
        ],
        pistas=[
            Pista(
                id=abridor_p,
                descricao="Marca do abridor de prata na mesa e na ferida",
                local_id=L("escritorio"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[abridor],
            ),
            Pista(
                id=lenco,
                descricao="Lenço manchado com as iniciais R.F.",
                local_id=L("sala_de_jantar"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[renato_escritorio],
                exige_pistas=[abridor_p],
            ),
            Pista(
                id=anotacoes,
                descricao="Anotações de Otávio sobre remédios que sumiam",
                local_id=L("biblioteca"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[desvio],
            ),
            Pista(
                id=recibo,
                descricao="Recibo de agiota no quarto de Vera",
                local_id=L("quarto"),
                tipo=TipoPista.FALSA,
                aponta_para=[ligacao],
            ),
            Pista(
                id=taca,
                descricao="Taça quebrada na sala de jantar",
                local_id=L("sala_de_jantar"),
                tipo=TipoPista.FALSA,
            ),
        ],
        cadeia_solucao=[desvio, abridor, renato_escritorio],
        condicao_acerto=CondicaoAcerto(
            culpado_id=renato,
            motivo_fato_id=desvio,
            provas_minimas=[anotacoes, lenco, abridor_p],
            quantas_provas=2,
        ),
    )
    return CasoPronto(
        chave=ChaveCaso.O_TESTAMENTO,
        titulo="O Testamento",
        mapa=MANSAO.chave,
        apresentacao=APRESENTACAO,
        solucao=SOLUCAO,
        entrada=L(MANSAO.entrada),
        escalacao={
            renato: escalar(P.RENATO, "médico da família"),
            vera: escalar(P.VERA, "herdeira, sobrinha-neta de Otávio"),
            caio: escalar(P.CAIO, "sobrinho e músico"),
            joaquim: escalar(P.JOAQUIM, "caseiro da mansão"),
            helena: escalar(P.HELENA, "delegada chamada para investigar"),
            otavio: escalar(P.OTAVIO, "patriarca da família e vítima"),
        },
        caso=caso,
    )
