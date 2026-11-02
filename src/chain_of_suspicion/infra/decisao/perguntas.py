from enum import StrEnum

from ...dominio.base import ModeloBase


class PerguntaDeDecisao(StrEnum):
    ESCOLHER_ACAO = "escolher_acao"
    ESCOLHER_ALVO = "escolher_alvo"
    DEVE_MENTIR = "deve_mentir"
    AMEACA = "ameaca"
    CONTRADICAO = "contradicao"


class TipoDePergunta(StrEnum):
    BOOLEAN = "boolean"
    CHOICE = "choice"
    SCORE = "score"


TIPO_DA_PERGUNTA: dict[PerguntaDeDecisao, TipoDePergunta] = {
    PerguntaDeDecisao.ESCOLHER_ACAO: TipoDePergunta.CHOICE,
    PerguntaDeDecisao.ESCOLHER_ALVO: TipoDePergunta.CHOICE,
    PerguntaDeDecisao.DEVE_MENTIR: TipoDePergunta.BOOLEAN,
    PerguntaDeDecisao.AMEACA: TipoDePergunta.SCORE,
    PerguntaDeDecisao.CONTRADICAO: TipoDePergunta.BOOLEAN,
}

INSTRUCAO_DA_PERGUNTA: dict[PerguntaDeDecisao, str] = {
    PerguntaDeDecisao.ESCOLHER_ACAO: (
        "Qual é a melhor ação para este personagem fazer agora, de acordo com a "
        "personalidade, o objetivo e o que ele sabe?"
    ),
    PerguntaDeDecisao.ESCOLHER_ALVO: (
        "Qual destas opções este personagem escolheria agora para a ação decidida?"
    ),
    PerguntaDeDecisao.DEVE_MENTIR: (
        "Este personagem mentiria ou esconderia a verdade nesta situação?"
    ),
    PerguntaDeDecisao.AMEACA: ("O quanto esta pressão ameaça os segredos do personagem?"),
    PerguntaDeDecisao.CONTRADICAO: ("A declaração contradiz o fato verdadeiro?"),
}

NIVEIS_DE_AMEACA = ["nenhuma", "baixa", "média", "alta", "máxima"]
LIMIAR_BOOLEANO = 0.5


class Pergunta(ModeloBase, frozen=True):
    tipo: PerguntaDeDecisao
    opcoes: dict[str, str] | None = None
    niveis: list[str] | None = None

    def payload(self) -> dict[str, object]:
        corpo: dict[str, object] = {
            "type": TIPO_DA_PERGUNTA[self.tipo].value,
            "instructions": INSTRUCAO_DA_PERGUNTA[self.tipo],
        }
        if self.opcoes is not None:
            corpo["criteria"] = self.opcoes
        if self.niveis is not None:
            corpo["criteria"] = self.niveis
        return corpo


class ResultadoBooleano(ModeloBase, frozen=True):
    probabilidade: float

    @property
    def verdadeiro(self) -> bool:
        return self.probabilidade >= LIMIAR_BOOLEANO


class ResultadoEscolha(ModeloBase, frozen=True):
    escolha: str
    probabilidades: dict[str, float]


class ResultadoNota(ModeloBase, frozen=True):
    nota: float
    niveis: int

    @property
    def normalizada(self) -> float:
        return min(1.0, max(0.0, self.nota / (self.niveis - 1)))


type Resultado = ResultadoBooleano | ResultadoEscolha | ResultadoNota
