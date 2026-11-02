from datetime import timedelta
from enum import StrEnum
from uuid import NAMESPACE_URL, uuid5

from ..dominio.base import ModeloBase
from ..dominio.ids import LocalId
from ..dominio.mapa import Conexao, Local, Mapa


class ChaveMapa(StrEnum):
    MANSAO = "mansao"
    NAVIO = "navio"
    POUSADA = "pousada"


class DefinicaoDeLocal(ModeloBase, frozen=True):
    chave: str
    nome: str
    descricao: str

    def cena_godot(self, mapa: ChaveMapa) -> str:
        return f"res://cenas/{mapa.value}/{self.chave}.tscn"


class Passagem(ModeloBase, frozen=True):
    de: str
    para: str
    minutos: int


class MapaPronto(ModeloBase, frozen=True):
    chave: ChaveMapa
    titulo: str
    descricao: str
    entrada: str
    locais: list[DefinicaoDeLocal]
    passagens: list[Passagem]

    def id_do_local(self, chave: str) -> LocalId:
        return LocalId(uuid5(NAMESPACE_URL, f"chain-of-suspicion/mapas/{self.chave.value}/{chave}"))

    def construir(self) -> Mapa:
        return Mapa(
            locais=[Local(id=self.id_do_local(d.chave), nome=d.nome) for d in self.locais],
            conexoes=[
                Conexao(
                    origem=self.id_do_local(p.de),
                    destino=self.id_do_local(p.para),
                    tempo=timedelta(minutes=p.minutos),
                )
                for p in self.passagens
            ],
        )


def _local(chave: str, nome: str, descricao: str) -> DefinicaoDeLocal:
    return DefinicaoDeLocal(chave=chave, nome=nome, descricao=descricao)


def _passagem(de: str, para: str, minutos: int) -> Passagem:
    return Passagem(de=de, para=para, minutos=minutos)


MANSAO = MapaPronto(
    chave=ChaveMapa.MANSAO,
    titulo="Mansão Villaça",
    descricao=(
        "Casarão de dois andares numa colina afastada da cidade, com madeira escura, "
        "tapetes pesados e corredores que rangem. A noite cai cedo e o único caminho "
        "até a estrada está bloqueado pela chuva."
    ),
    entrada="hall",
    locais=[
        _local("hall", "Hall", "Saguão amplo com escadaria de madeira e relógio de pêndulo."),
        _local(
            "biblioteca", "Biblioteca", "Estantes até o teto, lareira apagada e poltronas de couro."
        ),
        _local("escritorio", "Escritório", "Mesa de mogno, cofre embutido e papéis empilhados."),
        _local("sala_de_jantar", "Sala de Jantar", "Mesa para doze, candelabros e louça de gala."),
        _local("cozinha", "Cozinha", "Fogão a lenha, bancada de mármore e despensa abarrotada."),
        _local("jardim", "Jardim", "Canteiros, estufa de ervas e um banco sob a figueira."),
        _local(
            "quarto", "Quarto de Hóspedes", "Cama de dossel, penteadeira e janela para o jardim."
        ),
        _local("adega", "Adega", "Porão frio de pedra com garrafas empoeiradas."),
    ],
    passagens=[
        _passagem("hall", "biblioteca", 1),
        _passagem("hall", "escritorio", 2),
        _passagem("hall", "sala_de_jantar", 1),
        _passagem("sala_de_jantar", "cozinha", 1),
        _passagem("cozinha", "jardim", 2),
        _passagem("hall", "quarto", 2),
        _passagem("cozinha", "adega", 2),
    ],
)

NAVIO = MapaPronto(
    chave=ChaveMapa.NAVIO,
    titulo="Cruzeiro Estrela do Sul",
    descricao=(
        "Pequeno navio de cruzeiro em travessia noturna, com salão de baile, bar e "
        "cabines luxuosas. Em alto-mar não há para onde fugir nem como pedir ajuda."
    ),
    entrada="conves",
    locais=[
        _local(
            "conves",
            "Convés",
            "Pista aberta ao vento, com espreguiçadeiras e vista para o mar escuro.",
        ),
        _local(
            "salao", "Salão de Baile", "Pista de dança, palco para a banda e lustres de cristal."
        ),
        _local("bar", "Bar", "Balcão de madeira polida, banquetas e luz baixa."),
        _local(
            "corredor",
            "Corredor das Cabines",
            "Corredor estreito com carpete vermelho e portas numeradas.",
        ),
        _local("cabine_vip", "Cabine VIP", "Suíte com sacada fechada, cofre e cama de casal."),
        _local("ponte", "Ponte de Comando", "Painel de navegação, leme e cartas náuticas."),
        _local(
            "casa_de_maquinas", "Casa de Máquinas", "Barulho constante, vapor e cheiro de óleo."
        ),
        _local("enfermaria", "Enfermaria", "Maca, armário de remédios e luz branca."),
    ],
    passagens=[
        _passagem("conves", "salao", 1),
        _passagem("salao", "bar", 1),
        _passagem("salao", "corredor", 1),
        _passagem("corredor", "cabine_vip", 1),
        _passagem("conves", "ponte", 2),
        _passagem("conves", "casa_de_maquinas", 3),
        _passagem("corredor", "enfermaria", 2),
    ],
)

POUSADA = MapaPronto(
    chave=ChaveMapa.POUSADA,
    titulo="Pousada Serra Branca",
    descricao=(
        "Pousada de madeira no alto da serra, isolada por uma nevasca que derrubou a "
        "linha telefônica. Lareira acesa, cheiro de lenha e poucos hóspedes."
    ),
    entrada="recepcao",
    locais=[
        _local("recepcao", "Recepção", "Balcão de madeira, quadro de chaves e sino de latão."),
        _local(
            "lareira", "Salão da Lareira", "Poltronas gastas, tapete de lã e lareira crepitando."
        ),
        _local(
            "refeitorio", "Refeitório", "Mesas compridas, bules fumegantes e janelas embaçadas."
        ),
        _local("cozinha", "Cozinha", "Panelas de cobre, facas na parede e despensa fria."),
        _local(
            "corredor", "Corredor dos Quartos", "Piso de tábuas que rangem e portas com plaquinhas."
        ),
        _local(
            "quarto_12",
            "Quarto 12",
            "Aposento do dono, com escrivaninha, cofre pequeno e fotos antigas.",
        ),
        _local(
            "galpao",
            "Galpão de Lenha",
            "Barracão externo com lenha empilhada, machado e ferramentas.",
        ),
        _local("sotao", "Sótão", "Baús, caixas de documentos e uma janela redonda."),
    ],
    passagens=[
        _passagem("recepcao", "lareira", 1),
        _passagem("lareira", "refeitorio", 1),
        _passagem("refeitorio", "cozinha", 1),
        _passagem("recepcao", "corredor", 1),
        _passagem("corredor", "quarto_12", 1),
        _passagem("cozinha", "galpao", 2),
        _passagem("corredor", "sotao", 2),
    ],
)

MAPAS: dict[ChaveMapa, MapaPronto] = {m.chave: m for m in (MANSAO, NAVIO, POUSADA)}
