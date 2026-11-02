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
from .construtor import DIAS_DO_CASO, PRIMEIRO_DIA, Ids, ator, escalar, estadia, hora, periodo

APRESENTACAO = (
    "Sábado, 02h15, em alto-mar. Um disparo ecoou no conves_f do cruzeiro Estrela do Sul e o "
    "armador Otávio Alves foi achado morto, baleado. A bordo estavam o sócio e advogado "
    "Paulo Brandão, o comandante Davi Rangel, o marinheiro Joaquim Pires e a cozinheira "
    "Lia Moraes. A delegada Helena Duarte, que viajava em missão, assumiu o caso. "
    "A costa está a horas de distância."
)

SOLUCAO = (
    "Otávio ia vender a companhia e demitir Paulo, descoberto em fraudes contábeis. Paulo "
    "pegou o revólver do cofre da cabine do comandante, atravessou o salão às 02h00 de "
    "paletó pesado (Lia o viu do bar) e atirou em Otávio no conves_f. Joaquim estava no "
    "conves_f de popa, acertando a venda ilegal de óleo com um barco pesqueiro (pista falsa), "
    "e mente sobre o álibi para não ser demitido. Provas decisivas: o balanço adulterado, "
    "a pólvora no paletó e o cofre vazio."
)


def construir() -> CasoPronto:
    ids = Ids(ChaveCaso.SANGUE_NO_CONVES)
    L = NAVIO.id_do_local
    paulo, otavio = ids.personagem(P.PAULO), ids.personagem(P.OTAVIO)
    davi, joaquim = ids.personagem(P.DAVI), ids.personagem(P.JOAQUIM)
    lia, helena = ids.personagem(P.LIA), ids.personagem(P.HELENA)
    venda, pistola, conves_f = (
        ids.fato("venda_da_companhia"),
        ids.fato("revolver_do_cofre"),
        ids.fato("paulo_no_conves"),
    )
    oleo, lia_viu = ids.fato("venda_de_oleo"), ids.fato("lia_viu_paulo")
    balanco, polvora, revolver = (
        ids.pista("balanco"),
        ids.pista("polvora"),
        ids.pista("cofre_vazio"),
    )
    nota, marcas = ids.pista("nota_de_oleo"), ids.pista("marcas")

    caso = Caso(
        id=ids.caso(),
        seed=4,
        calendario=Calendario(inicio=PRIMEIRO_DIA, dias=DIAS_DO_CASO),
        mapa=NAVIO.construir(),
        crime=Crime(
            vitima_id=otavio,
            instante=hora("02:15", 2),
            local_id=L("conves"),
            metodo=MetodoCrime.ARMA_DE_FOGO,
            motivo_fato_id=venda,
        ),
        culpado_id=paulo,
        fatos=[
            Fato(
                id=venda,
                descricao="Otávio ia vender a companhia e demitir Paulo por fraudes contábeis",
            ),
            Fato(id=pistola, descricao="O revólver usado saiu do cofre da cabine do comandante"),
            Fato(id=conves_f, descricao="Paulo subiu ao conves_f às 02:05 com a arma sob o paletó"),
            Fato(
                id=oleo, descricao="Joaquim vendia óleo do navio a um barco pesqueiro naquela noite"
            ),
            Fato(
                id=lia_viu, descricao="Lia viu Paulo, de paletó pesado, atravessar o salão às 02:00"
            ),
        ],
        linha_do_tempo=[
            Evento(
                id=ids.evento("subida"),
                instante=hora("02:05", 2),
                local_id=L("conves"),
                fato_id=conves_f,
            ),
            Evento(id=ids.evento("crime"), instante=hora("02:15", 2), local_id=L("conves")),
        ],
        personagens=[
            ator(
                ids,
                P.PAULO,
                Papel.ASSASSINO,
                objetivo=Objetivo(tipo=TipoObjetivo.EVITAR_ACUSACAO),
                sabe={venda, pistola, conves_f},
                segredos=[Segredo(fato_id=conves_f, revela_se=[revolver, polvora])],
                limite_estresse=1.2,
            ),
            ator(
                ids,
                P.JOAQUIM,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.PROTEGER_SEGREDO, fato_id=oleo),
                sabe={oleo},
                segredos=[Segredo(fato_id=oleo, revela_se=[nota])],
                limite_estresse=0.8,
            ),
            ator(ids, P.DAVI, Papel.INOCENTE, objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR)),
            ator(
                ids,
                P.LIA,
                Papel.INOCENTE,
                objetivo=Objetivo(tipo=TipoObjetivo.COLABORAR),
                sabe={lia_viu},
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
            estadia(paulo, L("salao"), periodo("01:35", "02:00", 2)),
            estadia(paulo, L("conves"), periodo("02:05", "02:30", 2)),
            estadia(otavio, L("conves"), periodo("01:30", "02:30", 2)),
            estadia(davi, L("ponte"), periodo("01:35", "02:30", 2)),
            estadia(joaquim, L("casa_de_maquinas"), periodo("01:35", "01:50", 2)),
            estadia(joaquim, L("conves"), periodo("01:55", "02:30", 2)),
            estadia(lia, L("bar"), periodo("01:35", "02:30", 2)),
        ],
        alibis=[
            Alibi(
                personagem_id=paulo,
                local_id=L("salao"),
                periodo=periodo("01:40", "02:20", 2),
                desmentido_por=[conves_f],
            ),
            Alibi(
                personagem_id=joaquim,
                local_id=L("casa_de_maquinas"),
                periodo=periodo("01:40", "02:30", 2),
                desmentido_por=[oleo],
            ),
            Alibi(personagem_id=davi, local_id=L("ponte"), periodo=periodo("01:40", "02:30", 2)),
        ],
        pistas=[
            Pista(
                id=revolver,
                descricao="Cofre da cabine do comandante aberto e vazio",
                local_id=L("cabine_vip"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[pistola],
            ),
            Pista(
                id=polvora,
                descricao="Resíduo de pólvora na manga do paletó de Paulo",
                local_id=L("salao"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[conves_f],
                exige_pistas=[revolver],
            ),
            Pista(
                id=balanco,
                descricao="Balanço adulterado na mesa de Otávio",
                local_id=L("corredor"),
                tipo=TipoPista.RELEVANTE,
                aponta_para=[venda],
            ),
            Pista(
                id=nota,
                descricao="Nota de venda de óleo na casa de máquinas",
                local_id=L("casa_de_maquinas"),
                tipo=TipoPista.FALSA,
                aponta_para=[oleo],
            ),
            Pista(
                id=marcas,
                descricao="Marcas de sapato molhado no conves_f",
                local_id=L("conves"),
                tipo=TipoPista.FALSA,
            ),
        ],
        cadeia_solucao=[venda, pistola, conves_f],
        condicao_acerto=CondicaoAcerto(
            culpado_id=paulo,
            motivo_fato_id=venda,
            provas_minimas=[balanco, polvora, revolver],
            quantas_provas=2,
        ),
    )
    return CasoPronto(
        chave=ChaveCaso.SANGUE_NO_CONVES,
        titulo="Sangue no Convés",
        mapa=NAVIO.chave,
        apresentacao=APRESENTACAO,
        solucao=SOLUCAO,
        entrada=L(NAVIO.entrada),
        escalacao={
            paulo: escalar(P.PAULO, "sócio e advogado de Otávio"),
            joaquim: escalar(P.JOAQUIM, "marinheiro de máquinas"),
            davi: escalar(P.DAVI, "comandante do navio"),
            lia: escalar(P.LIA, "cozinheira de bordo"),
            helena: escalar(P.HELENA, "delegada em viagem de serviço"),
            otavio: escalar(P.OTAVIO, "armador dono do navio e vítima"),
        },
        caso=caso,
    )
