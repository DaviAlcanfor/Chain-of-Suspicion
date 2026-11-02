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
    "Sexta-feira, 22h10. Na Mansão Villaça, uma casa afastada isolada pela chuva, o "
    "empresário Otávio Alves foi encontrado morto na biblioteca, caído ao lado de uma taça. "
    "Todos que estavam na casa naquela noite ainda estão lá: a viúva Marta Villaça, "
    "acionista da empresa de Otávio; o advogado Paulo Brandão; a cozinheira Lia Moraes; e "
    "o sobrinho Caio Teles. O inspetor Alencar Moura chegou para investigar. A estrada "
    "está bloqueada: o culpado está entre eles."
)

SOLUCAO = (
    "Marta devia uma fortuna a Otávio, que ameaçou cobrar na justiça. Ela colheu uma planta "
    "venenosa da estufa do jardim, entrou na biblioteca às 21h55 e envenenou a taça dele. "
    "Marta jura que ficou no quarto, mas a câmera do hall a mostra indo à biblioteca. "
    "Paulo mente sobre o álibi porque escondeu uma carta comprometedora no quarto; "
    "é uma pista falsa. Provas decisivas: extrato da dívida, imagem de Marta, copo com resíduo."
)


def construir() -> CasoPronto:
    ids = Ids(ChaveCaso.VENENO_NA_BIBLIOTECA)
    L = MANSAO.id_do_local
    marta, otavio = ids.personagem(P.MARTA), ids.personagem(P.OTAVIO)
    paulo, lia = ids.personagem(P.PAULO), ids.personagem(P.LIA)
    caio, alencar = ids.personagem(P.CAIO), ids.personagem(P.ALENCAR)
    divida, veneno, biblio = ids.fato("divida"), ids.fato("veneno"), ids.fato("biblio")
    carta, lia_cozinha = ids.fato("carta"), ids.fato("lia_cozinha")
    copo, camera, extrato = ids.pista("copo"), ids.pista("camera"), ids.pista("extrato")
    planta, carta_p, luvas = ids.pista("planta"), ids.pista("carta"), ids.pista("luvas")

    caso = Caso(
        id=ids.caso(),
        seed=1,
        calendario=Calendario(inicio=PRIMEIRO_DIA, dias=DIAS_DO_CASO),
        mapa=MANSAO.construir(),
        crime=Crime(
            vitima_id=otavio,
            instante=hora("22:10"),
            local_id=L("biblioteca"),
            metodo=MetodoCrime.ENVENENAMENTO,
            motivo_fato_id=divida,
        ),
        culpado_id=marta,
        fatos=[
            Fato(
                id=divida,
                descricao="Marta devia uma fortuna a Otávio, que ameaçou cobrar na justiça",
            ),
            Fato(id=veneno, descricao="O veneno foi extraído de uma planta da estufa do jardim"),
            Fato(id=biblio, descricao="Marta entrou na biblioteca às 21:55"),
            Fato(id=carta, descricao="Paulo escondeu uma carta comprometedora no quarto"),
            Fato(id=lia_cozinha, descricao="Lia ficou na cozinha das 21:30 às 22:30"),
        ],
        linha_do_tempo=[
            Evento(
                id=ids.evento("entrada"),
                instante=hora("21:55"),
                local_id=L("biblioteca"),
                fato_id=biblio,
            ),
            Evento(id=ids.evento("crime"), instante=hora("22:10"), local_id=L("biblioteca")),
        ],
        personagens=[
            ator(
                ids,
                P.MARTA,
                Papel.ASSASSINO,
                objetivo=Objetivo(tipo=TipoObjetivo.EVITAR_ACUSACAO),
                sabe={divida, veneno, biblio},
                segredos=[Segredo(fato_id=biblio, revela_se=[copo, camera])],
                limite_estresse=1.5,
            ),
            ator(
                ids,
                P.PAULO,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.PROTEGER_SEGREDO, fato_id=carta),
                sabe={carta, lia_cozinha},
                segredos=[Segredo(fato_id=carta, revela_se=[carta_p])],
                limite_estresse=0.8,
            ),
            ator(
                ids,
                P.LIA,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
                sabe={lia_cozinha},
            ),
            ator(ids, P.CAIO, Papel.INOCENTE, objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR)),
            ator(
                ids,
                P.ALENCAR,
                Papel.DETETIVE,
                objetivo=Objetivo(tipo=TipoObjetivo.ENCONTRAR_CULPADO),
            ),
            ator(ids, P.OTAVIO, Papel.VITIMA),
        ],
        agenda=[
            estadia(marta, L("quarto"), periodo("21:30", "21:50")),
            estadia(marta, L("biblioteca"), periodo("21:55", "22:30")),
            estadia(otavio, L("escritorio"), periodo("21:00", "21:45")),
            estadia(otavio, L("biblioteca"), periodo("21:50", "22:30")),
            estadia(paulo, L("quarto"), periodo("21:30", "21:45")),
            estadia(paulo, L("cozinha"), periodo("21:50", "22:30")),
            estadia(lia, L("cozinha"), periodo("21:30", "22:30")),
            estadia(caio, L("jardim"), periodo("21:30", "22:30")),
        ],
        alibis=[
            Alibi(
                personagem_id=marta,
                local_id=L("quarto"),
                periodo=periodo("21:35", "22:20"),
                desmentido_por=[biblio],
            ),
            Alibi(
                personagem_id=paulo,
                local_id=L("cozinha"),
                periodo=periodo("21:30", "22:30"),
                desmentido_por=[carta],
            ),
            Alibi(personagem_id=lia, local_id=L("cozinha"), periodo=periodo("21:30", "22:30")),
        ],
        pistas=[
            Pista(
                id=copo,
                descricao="Copo com resíduo",
                local_id=L("biblioteca"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[veneno],
            ),
            Pista(
                id=camera,
                descricao="Imagem de Marta entrando na biblioteca",
                local_id=L("hall"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[biblio],
                exige_pistas=[copo],
            ),
            Pista(
                id=extrato,
                descricao="Extrato com a dívida de Marta",
                local_id=L("escritorio"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[divida],
            ),
            Pista(
                id=planta,
                descricao="Planta venenosa arrancada na estufa",
                local_id=L("jardim"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[veneno],
            ),
            Pista(
                id=carta_p,
                descricao="Carta escondida",
                local_id=L("quarto"),
                tipo=TipoPista.FALSA,
                aponta_para=[carta],
            ),
            Pista(
                id=luvas,
                descricao="Luvas na lixeira da cozinha",
                local_id=L("cozinha"),
                tipo=TipoPista.FALSA,
            ),
        ],
        cadeia_solucao=[divida, veneno, biblio],
        condicao_acerto=CondicaoAcerto(
            culpado_id=marta,
            motivo_fato_id=divida,
            provas_minimas=[extrato, camera, copo],
            quantas_provas=2,
        ),
    )
    return CasoPronto(
        chave=ChaveCaso.VENENO_NA_BIBLIOTECA,
        titulo="Veneno na Biblioteca",
        mapa=MANSAO.chave,
        apresentacao=APRESENTACAO,
        solucao=SOLUCAO,
        entrada=L(MANSAO.entrada),
        escalacao={
            marta: escalar(P.MARTA, "viúva e acionista da empresa de Otávio"),
            paulo: escalar(P.PAULO, "advogado da família"),
            lia: escalar(P.LIA, "cozinheira da mansão"),
            caio: escalar(P.CAIO, "sobrinho de Otávio"),
            alencar: escalar(P.ALENCAR, "inspetor chamado para investigar"),
            otavio: escalar(P.OTAVIO, "dono da mansão e vítima"),
        },
        caso=caso,
    )
