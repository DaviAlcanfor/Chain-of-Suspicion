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
from ..mapas import NAVIO
from .construtor import (
    DIAS_DO_CASO,
    PRIMEIRO_DIA,
    Ids,
    ator,
    escalar,
    estadia,
    hora,
    noite_adentro,
    periodo,
)

APRESENTACAO = (
    "Sábado, 00h30, em alto-mar. No baile de gala do cruzeiro Estrela do Sul, a socialite "
    "Vera Lúcia Pinheiro foi encontrada estrangulada na cabine VIP. A jornalista Beatriz "
    "Nogueira, o advogado Paulo Brandão, o músico Caio Teles e o comandante Davi Rangel "
    "estavam a bordo. O inspetor Alencar Moura, que viajava de férias, assumiu a investigação. "
    "O navio só chega ao porto de manhã: ninguém desce, ninguém é substituído."
)

SOLUCAO = (
    "Vera havia comprado o jornal de Beatriz e engavetaria a reportagem sobre suas fraudes, "
    "destruindo a carreira da jornalista. Beatriz usou a chave reserva do corredor às 00h20, "
    "entrou na cabine e estrangulou Vera com o cinto de seda do roupão dela. Paulo, que "
    "buscava um casaco, viu de costas uma mulher de jaqueta de couro. Davi mente sobre seu "
    "álibi porque deixou a ponte para se tratar na enfermaria (pista falsa). Provas "
    "decisivas: rascunho da reportagem, registro da chave reserva e o cinto de seda."
)


def construir() -> CasoPronto:
    ids = Ids(ChaveCaso.A_ULTIMA_DANCA)
    L = NAVIO.id_do_local
    beatriz, vera = ids.personagem(P.BEATRIZ), ids.personagem(P.VERA)
    davi, paulo = ids.personagem(P.DAVI), ids.personagem(P.PAULO)
    caio, alencar = ids.personagem(P.CAIO), ids.personagem(P.ALENCAR)
    motivo, cinto_f = ids.fato("reportagem_engavetada"), ids.fato("cinto_de_seda")
    cabine, davi_f, paulo_f = (
        ids.fato("beatriz_na_cabine"),
        ids.fato("davi_na_enfermaria"),
        ids.fato("paulo_viu"),
    )
    reportagem, chave, cinto = (
        ids.pista("reportagem"),
        ids.pista("chave_reserva"),
        ids.pista("cinto"),
    )
    prontuario, taca = ids.pista("prontuario"), ids.pista("taca")

    caso = Caso(
        id=ids.caso(),
        seed=3,
        calendario=Calendario(inicio=PRIMEIRO_DIA, dias=DIAS_DO_CASO),
        mapa=NAVIO.construir(),
        crime=Crime(
            vitima_id=vera,
            instante=hora("00:30", 2),
            local_id=L("cabine_vip"),
            metodo=MetodoCrime.ESTRANGULAMENTO,
            motivo_fato_id=motivo,
        ),
        culpado_id=beatriz,
        fatos=[
            Fato(
                id=motivo,
                descricao="Vera comprou o jornal de Beatriz e engavetaria a reportagem sobre suas fraudes",
            ),
            Fato(
                id=cinto_f, descricao="Vera foi estrangulada com o cinto de seda do próprio roupão"
            ),
            Fato(id=cabine, descricao="Beatriz entrou na cabine VIP às 00:20 com a chave reserva"),
            Fato(
                id=davi_f,
                descricao="Davi deixou a ponte sem avisar e passou a madrugada na enfermaria",
            ),
            Fato(
                id=paulo_f,
                descricao="Paulo viu de costas uma mulher de jaqueta de couro entrar na cabine às 00:20",
            ),
        ],
        linha_do_tempo=[
            Evento(
                id=ids.evento("entrada"),
                instante=hora("00:20", 2),
                local_id=L("corredor"),
                fato_id=cabine,
            ),
            Evento(id=ids.evento("crime"), instante=hora("00:30", 2), local_id=L("cabine_vip")),
        ],
        personagens=[
            ator(
                ids,
                P.BEATRIZ,
                Papel.ASSASSINO,
                objetivo=Objetivo(tipo=TipoObjetivo.EVITAR_ACUSACAO),
                sabe={motivo, cinto_f, cabine},
                segredos=[Segredo(fato_id=cabine, revela_se=[cinto, chave])],
                limite_estresse=1.3,
            ),
            ator(
                ids,
                P.DAVI,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.PROTEGER_SEGREDO, fato_id=davi_f),
                sabe={davi_f},
                segredos=[Segredo(fato_id=davi_f, revela_se=[prontuario])],
                limite_estresse=0.9,
            ),
            ator(
                ids,
                P.PAULO,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
                sabe={paulo_f},
            ),
            ator(ids, P.CAIO, Papel.INOCENTE, objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR)),
            ator(
                ids,
                P.ALENCAR,
                Papel.DETETIVE,
                objetivo=Objetivo(tipo=TipoObjetivo.ENCONTRAR_CULPADO),
            ),
            ator(ids, P.VERA, Papel.VITIMA),
        ],
        agenda=[
            estadia(beatriz, L("bar"), noite_adentro("23:50", "00:10")),
            estadia(beatriz, L("cabine_vip"), periodo("00:20", "00:45", 2)),
            estadia(vera, L("salao"), noite_adentro("23:30", "00:10")),
            estadia(vera, L("cabine_vip"), periodo("00:15", "00:45", 2)),
            estadia(davi, L("ponte"), noite_adentro("23:50", "00:05")),
            estadia(davi, L("enfermaria"), periodo("00:12", "00:50", 2)),
            estadia(davi, L("ponte"), periodo("00:56", "01:20", 2)),
            estadia(paulo, L("salao"), noite_adentro("23:50", "00:12")),
            estadia(paulo, L("corredor"), periodo("00:14", "00:24", 2)),
            estadia(paulo, L("salao"), periodo("00:26", "00:50", 2)),
            estadia(caio, L("salao"), noite_adentro("23:50", "00:50")),
        ],
        alibis=[
            Alibi(
                personagem_id=beatriz,
                local_id=L("bar"),
                periodo=noite_adentro("23:55", "00:35"),
                desmentido_por=[cabine],
            ),
            Alibi(
                personagem_id=davi,
                local_id=L("ponte"),
                periodo=periodo("00:00", "01:00", 2),
                desmentido_por=[davi_f],
            ),
            Alibi(personagem_id=caio, local_id=L("salao"), periodo=noite_adentro("23:55", "00:45")),
        ],
        pistas=[
            Pista(
                id=cinto,
                descricao="Cinto de seda do roupão usado no crime",
                local_id=L("cabine_vip"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[cinto_f],
            ),
            Pista(
                id=chave,
                descricao="Registro de uso da chave reserva às 00:20",
                local_id=L("corredor"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[cabine],
                exige_pistas=[cinto],
            ),
            Pista(
                id=reportagem,
                descricao="Rascunho da reportagem de Beatriz sobre as fraudes de Vera",
                local_id=L("bar"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[motivo],
            ),
            Pista(
                id=prontuario,
                descricao="Prontuário de Davi na enfermaria",
                local_id=L("enfermaria"),
                tipo=TipoPista.FALSA,
                aponta_para=[davi_f],
            ),
            Pista(
                id=taca,
                descricao="Taça de champanhe esquecida no salão",
                local_id=L("salao"),
                tipo=TipoPista.FALSA,
            ),
        ],
        cadeia_solucao=[motivo, cinto_f, cabine],
        condicao_acerto=CondicaoAcerto(
            culpado_id=beatriz,
            motivo_fato_id=motivo,
            provas_minimas=[reportagem, chave, cinto],
            quantas_provas=2,
        ),
    )
    return CasoPronto(
        chave=ChaveCaso.A_ULTIMA_DANCA,
        titulo="A Última Dança",
        mapa=NAVIO.chave,
        apresentacao=APRESENTACAO,
        solucao=SOLUCAO,
        entrada=L(NAVIO.entrada),
        escalacao={
            beatriz: escalar(P.BEATRIZ, "jornalista convidada ao baile"),
            davi: escalar(P.DAVI, "comandante do navio"),
            paulo: escalar(P.PAULO, "advogado de Vera"),
            caio: escalar(P.CAIO, "músico da banda do baile"),
            alencar: escalar(P.ALENCAR, "inspetor em viagem de férias"),
            vera: escalar(P.VERA, "socialite anfitriã do baile e vítima"),
        },
        caso=caso,
    )
