from functools import cache
from importlib import resources

from ..agentes.turno import ContextoDoTurno, DecisaoDoTurno
from ..conteudo.caso_pronto import CasoPronto
from ..conteudo.elenco import ELENCO
from ..conteudo.mapas import MAPAS
from ..dominio.ids import PersonagemId
from ..dominio.regras import Pressao, VisaoPersonagem

_PACOTE = "chain_of_suspicion.prompts"
SEPARADOR = "\n\n"
MARCADOR_SECAO = "## "


@cache
def _ler(subpasta: str, nome: str) -> str:
    pasta = resources.files(_PACOTE) / subpasta if subpasta else resources.files(_PACOTE)
    return (pasta / f"{nome}.md").read_text(encoding="utf-8").strip()


@cache
def _secoes(subpasta: str, nome: str) -> dict[str, str]:
    secoes: dict[str, list[str]] = {}
    atual: list[str] | None = None
    for linha in _ler(subpasta, nome).splitlines():
        if linha.startswith(MARCADOR_SECAO):
            atual = secoes.setdefault(linha.removeprefix(MARCADOR_SECAO).strip(), [])
        elif atual is not None:
            atual.append(linha)
    return {titulo: "\n".join(linhas).strip() for titulo, linhas in secoes.items()}


def contexto_do_caso(pronto: CasoPronto) -> str:
    mapa = MAPAS[pronto.mapa]
    elenco = "\n".join(
        f"- {pronto.caso.personagem(pessoa).nome}: {escalado.funcao}"
        for pessoa, escalado in pronto.escalacao.items()
    )
    return _ler("", "base").format(
        titulo_do_mapa=mapa.titulo,
        descricao_do_mapa=mapa.descricao,
        apresentacao=pronto.apresentacao,
        elenco=elenco,
    )


def montar_sistema(pronto: CasoPronto, personagem_id: PersonagemId) -> str:
    papel = pronto.caso.personagem(personagem_id).papel
    escalado = pronto.escalacao[personagem_id]
    persona = ELENCO[escalado.persona]
    do_papel = _secoes("papeis", papel.value)
    comum = _secoes("papeis", "comum")
    nome = pronto.caso.personagem(personagem_id).nome
    return SEPARADOR.join(
        [
            contexto_do_caso(pronto),
            f"# VOCÊ\n\nVocê é {nome}, {escalado.funcao}. {persona.ficha()}",
            f"# SEU PAPEL\n\n## PAPEL\n\n{do_papel['PAPEL']}",
            f"## OBJETIVO\n\n{do_papel['OBJETIVO']}",
            f"## COMO DECIDIR\n\n{do_papel['COMO DECIDIR']}",
            f"## REGRAS\n\n{comum['REGRAS']}\n{do_papel['REGRAS']}",
            f"## FORMATO\n\n{comum['FORMATO']}",
        ]
    )


def ficha_da_persona(pronto: CasoPronto, personagem_id: PersonagemId) -> str:
    escalado = pronto.escalacao[personagem_id]
    return ELENCO[escalado.persona].ficha()


def descrever_turno(visao: VisaoPersonagem, contexto: ContextoDoTurno) -> str:
    partes = [
        f"Você é {visao.nome}. Agora: {contexto.instante}, em {contexto.local_atual}.",
        _linha("Seu objetivo", [visao.objetivo.tipo.value] if visao.objetivo else []),
        _linha("O que você sabe", visao.fatos_que_sabe),
        _linha("Seus segredos", visao.segredos),
        _linha("Onde você esteve", visao.onde_estive),
        f"Seu álibi declarado: {visao.alibi_declarado or 'nenhum'}",
        _linha("O que você já disse", visao.o_que_ja_disse),
        _linha("Presentes aqui", list(contexto.presentes)),
        _linha("Saídas", list(contexto.saidas)),
        _linha("Pistas ao alcance", list(contexto.pistas)),
    ]
    if contexto.recusa_anterior:
        partes.append(f"Sua ação anterior foi recusada: {contexto.recusa_anterior}")
    return "\n".join(partes)


def estado_para_decisao(ficha: str, turno: str) -> str:
    return f"{ficha}\n\n{turno}"


def pedido_de_fala(turno: str, decisao: DecisaoDoTurno) -> str:
    linhas = [f"Decisão deste turno: você vai {decisao.acao.value}"]
    if decisao.alvo:
        linhas[0] += f" com foco em {decisao.alvo}"
    linhas.append("Você decidiu esconder a verdade." if decisao.mentir else "Você vai ser sincero.")
    corpo = "\n".join(linhas)
    return f"{turno}\n\n{corpo}\nDiga o que o personagem fala agora."


def prompt_ameaca(visao: VisaoPersonagem, pressao: Pressao) -> str:
    return _ler("decisao", "ameaca").format(
        nome=visao.nome,
        estresse=visao.estresse,
        segredos="; ".join(visao.segredos) or "nenhum",
        declaracoes="; ".join(visao.o_que_ja_disse) or "nada",
        pressao=pressao.tipo.value,
    )


def prompt_contradicao(declaracao: str, fato: str) -> str:
    return _ler("decisao", "contradicao").format(declaracao=declaracao, fato=fato)


def _linha(titulo: str, itens: list[str]) -> str:
    return f"{titulo}: {'; '.join(itens) if itens else 'nenhum'}"

