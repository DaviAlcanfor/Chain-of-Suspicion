from enum import StrEnum

from pydantic import Field

from ...dominio.base import ModeloBase


class Porte(StrEnum):
    MAGRO = "magro"
    MEDIO = "medio"
    ROBUSTO = "robusto"
    ATLETICO = "atletico"


class TomDePele(StrEnum):
    CLARO = "claro"
    MEDIO_CLARO = "medio_claro"
    MEDIO = "medio"
    MEDIO_ESCURO = "medio_escuro"
    ESCURO = "escuro"


class CorDeCabelo(StrEnum):
    PRETO = "preto"
    CASTANHO = "castanho"
    CASTANHO_CLARO = "castanho_claro"
    LOIRO_PLATINADO = "loiro_platinado"
    RUIVO = "ruivo"
    GRISALHO = "grisalho"
    BRANCO = "branco"


class EstiloDeCabelo(StrEnum):
    CURTO = "curto"
    PENTEADO_PARA_TRAS = "penteado_para_tras"
    REPARTIDO_DE_LADO = "repartido_de_lado"
    RALO = "ralo"
    VOLUMOSO = "volumoso"
    COQUE = "coque"
    RABO_DE_CAVALO = "rabo_de_cavalo"
    ONDULADO_NOS_OMBROS = "ondulado_nos_ombros"
    ONDULADO_COMPRIDO = "ondulado_comprido"
    ONDAS_DE_FESTA = "ondas_de_festa"


class PelosFaciais(StrEnum):
    NENHUM = "nenhum"
    BIGODE = "bigode"
    BIGODE_CAIDO = "bigode_caido"
    BARBA_RENTE = "barba_rente"
    BARBA_APARADA = "barba_aparada"


class PecaDeRoupa(StrEnum):
    TAILLEUR = "tailleur"
    TERNO = "terno"
    AVENTAL_SOBRE_VESTIDO = "avental_sobre_vestido"
    CAMISA_DE_LINHO_E_JEANS = "camisa_de_linho_e_jeans"
    SOBRETUDO_E_GRAVATA = "sobretudo_e_gravata"
    COLETE_DE_TWEED = "colete_de_tweed"
    BLAZER_E_CAMISA = "blazer_e_camisa"
    PALETO_E_GRAVATA_BORBOLETA = "paleto_e_gravata_borboleta"
    JAQUETA_DE_COURO = "jaqueta_de_couro"
    MACACAO_DE_BRIM = "macacao_de_brim"
    VESTIDO_DE_NOITE = "vestido_de_noite"
    UNIFORME_DE_COMANDANTE = "uniforme_de_comandante"


class Acessorio(StrEnum):
    COLAR_DE_PEROLAS = "colar_de_perolas"
    ANEL_DE_SAFIRA = "anel_de_safira"
    OCULOS_DE_ARO_FINO = "oculos_de_aro_fino"
    PASTA_DE_COURO = "pasta_de_couro"
    BRINCOS_DE_ARGOLA = "brincos_de_argola"
    PULSEIRAS_DE_COURO = "pulseiras_de_couro"
    CADERNETA = "caderneta"
    CHAPEU_DE_FELTRO = "chapeu_de_feltro"
    BENGALA_DE_EBANO = "bengala_de_ebano"
    RELOGIO_DE_BOLSO = "relogio_de_bolso"
    DISTINTIVO = "distintivo"
    RELOGIO_DE_PULSO = "relogio_de_pulso"
    MALETA_MEDICA = "maleta_medica"
    ESTETOSCOPIO = "estetoscopio"
    GRAVADOR = "gravador"
    MOCHILA_DE_LONA = "mochila_de_lona"
    MOLHO_DE_CHAVES = "molho_de_chaves"
    CHAPEU_DE_PALHA = "chapeu_de_palha"
    LEQUE = "leque"
    BRINCOS_LONGOS = "brincos_longos"
    BATOM_VERMELHO = "batom_vermelho"
    BONE_DE_COMANDANTE = "bone_de_comandante"
    BINOCULO = "binoculo"


class Paleta(StrEnum):
    AZUL_MARINHO = "azul_marinho"
    CINZA_CHUMBO = "cinza_chumbo"
    TERRACOTA = "terracota"
    AMARELO_OCRE = "amarelo_ocre"
    MARROM_TERRA = "marrom_terra"
    MARROM_ESCURO = "marrom_escuro"
    PRETO_FOSCO = "preto_fosco"
    VERDE_FLORESTA = "verde_floresta"
    FERRUGEM = "ferrugem"
    BEGE_AREIA = "bege_areia"
    VINHO = "vinho"
    AZUL_PETROLEO = "azul_petroleo"


HEX_DA_COR: dict[Paleta, str] = {
    Paleta.AZUL_MARINHO: "#1F2F5C",
    Paleta.CINZA_CHUMBO: "#6B6F76",
    Paleta.TERRACOTA: "#C8553D",
    Paleta.AMARELO_OCRE: "#D9A441",
    Paleta.MARROM_TERRA: "#7A5A3A",
    Paleta.MARROM_ESCURO: "#4A3B2A",
    Paleta.PRETO_FOSCO: "#222222",
    Paleta.VERDE_FLORESTA: "#2E5D4B",
    Paleta.FERRUGEM: "#B5412E",
    Paleta.BEGE_AREIA: "#8C7B5A",
    Paleta.VINHO: "#8E1B3A",
    Paleta.AZUL_PETROLEO: "#1D4E5F",
}


class Aparencia(ModeloBase, frozen=True):
    idade: int = Field(ge=18)
    altura_cm: int = Field(ge=140, le=210)
    porte: Porte
    pele: TomDePele
    cabelo_cor: CorDeCabelo
    cabelo_estilo: EstiloDeCabelo
    pelos_faciais: PelosFaciais = PelosFaciais.NENHUM
    roupa: PecaDeRoupa
    cor_da_roupa: Paleta
    acessorios: list[Acessorio] = Field(min_length=1)
    nota_de_arte: str = ""

    @property
    def hex_da_roupa(self) -> str:
        return HEX_DA_COR[self.cor_da_roupa]
