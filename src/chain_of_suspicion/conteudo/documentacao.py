import json
from datetime import datetime
from pathlib import Path

from ..dominio.caso import Caso
from ..dominio.relogio import Intervalo
from .caso_pronto import CasoPronto, ChaveCaso
from .casos import CATALOGO
from .elenco import ELENCO
from .elenco.personas import Persona
from .mapas import MAPAS, MapaPronto

FORMATO = "%d/%m %H:%M"


def _hora(instante: datetime) -> str:
    return instante.strftime(FORMATO)


def _periodo(intervalo: Intervalo) -> str:
    return f"{_hora(intervalo.inicio)}–{intervalo.fim.strftime('%H:%M')}"


def documentar_persona(persona: Persona) -> str:
    a = persona.aparencia
    return "\n".join(
        [
            f"## {persona.nome_completo} (`{persona.chave.value}`)",
            "",
            f"**{persona.profissao}** · exibida no jogo como **{persona.nome}**",
            "",
            f"- Traços: {', '.join(t.value for t in persona.tracos)}",
            f"- Personalidade: {persona.personalidade}",
            f"- Jeito de falar: {persona.jeito_de_falar}",
            f"- Manias: {'; '.join(persona.manias)}",
            "",
            "**Aparência (para o Godot)**",
            "",
            "| Campo | Valor |",
            "| --- | --- |",
            f"| Idade | {a.idade} anos |",
            f"| Altura | {a.altura_cm} cm |",
            f"| Porte | {a.porte.value} |",
            f"| Pele | {a.pele.value} |",
            f"| Cabelo | {a.cabelo_cor.value}, {a.cabelo_estilo.value} |",
            f"| Pelos faciais | {a.pelos_faciais.value} |",
            f"| Roupa | {a.roupa.value} · {a.cor_da_roupa.value} (`{a.hex_da_roupa}`) |",
            f"| Acessórios | {', '.join(x.value for x in a.acessorios)} |",
            f"| Nota de arte | {a.nota_de_arte or '—'} |",
            f"| Cena/modelo | `{persona.modelo_godot}` |",
            "",
        ]
    )


def elenco_em_json() -> str:
    dados = {
        p.chave.value: {
            "nome": p.nome,
            **p.aparencia.model_dump(mode="json", exclude={"idade", "nota_de_arte"}),
            "hex_da_roupa": p.aparencia.hex_da_roupa,
        }
        for p in ELENCO.values()
    }
    return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"


def documentar_elenco() -> str:
    cabecalho = [
        "# Elenco",
        "",
        "> Gerado por `tools/gerar_docs.py`. Não edite à mão: mude `conteudo/elenco/catalogo.py`.",
        "",
        "Doze personas reaproveitadas entre os casos. O **papel** (assassino, detetive, "
        "inocente, vítima) é definido pelo caso, não pela persona; a aparência é sempre a mesma.",
        "",
    ]
    return "\n".join([*cabecalho, *(documentar_persona(p) for p in ELENCO.values())])


def documentar_mapa(mapa: MapaPronto) -> str:
    locais = [
        f"| `{d.chave}` | {d.nome} | {d.descricao} | `{d.cena_godot(mapa.chave)}` |"
        for d in mapa.locais
    ]
    passagens = [f"| {p.de} ↔ {p.para} | {p.minutos} min |" for p in mapa.passagens]
    return "\n".join(
        [
            f"## {mapa.titulo} (`{mapa.chave.value}`)",
            "",
            mapa.descricao,
            "",
            f"Entrada do detetive: `{mapa.entrada}`",
            "",
            "| Chave | Nome | Descrição | Cena do Godot |",
            "| --- | --- | --- | --- |",
            *locais,
            "",
            "| Passagem | Tempo |",
            "| --- | --- |",
            *passagens,
            "",
        ]
    )


def documentar_mapas() -> str:
    cabecalho = [
        "# Mapas",
        "",
        "> Gerado por `tools/gerar_docs.py`. Não edite à mão: mude `conteudo/mapas.py`.",
        "",
        "Cada local tem uma chave estável, que o servidor usa como id determinístico e o Godot "
        "usa para carregar a cena. Os tempos são de deslocamento entre locais vizinhos.",
        "",
    ]
    return "\n".join([*cabecalho, *(documentar_mapa(m) for m in MAPAS.values())])


def _quem(caso: Caso, ids: list) -> str:  # type: ignore[type-arg]
    return ", ".join(caso.personagem(i).nome for i in ids)


def documentar_caso(numero: int, pronto: CasoPronto) -> str:
    caso = pronto.caso
    mapa = MAPAS[pronto.mapa]
    elenco = [
        f"| {caso.personagem(pid).nome} | {e.persona.value} | {caso.personagem(pid).papel.value} "
        f"| {e.funcao} |"
        for pid, e in pronto.escalacao.items()
    ]
    fatos = [f"- {f.descricao}" for f in caso.fatos]
    linha = [
        f"- {_hora(e.instante)} · {caso.mapa.nome(e.local_id)}"
        + (f" · {caso.fato(e.fato_id).descricao}" if e.fato_id else " · o crime")
        for e in sorted(caso.linha_do_tempo, key=lambda e: e.instante)
    ]
    agenda = [
        f"| {caso.personagem(a.personagem_id).nome} | {caso.mapa.nome(a.local_id)} | "
        f"{_periodo(a.periodo)} |"
        for a in sorted(
            caso.agenda, key=lambda a: (caso.personagem(a.personagem_id).nome, a.periodo.inicio)
        )
    ]
    alibis = [
        f"| {caso.personagem(a.personagem_id).nome} | {caso.mapa.nome(a.local_id)} | "
        f"{_periodo(a.periodo)} | {'verdadeiro' if caso.alibi_confere(a) else 'falso'} | "
        f"{'; '.join(caso.fato(f).descricao for f in a.desmentido_por) or '—'} |"
        for a in caso.alibis
    ]
    pistas = [
        f"| {p.descricao} | {caso.mapa.nome(p.local_id)} | {p.tipo.value} | "
        f"{'; '.join(caso.fato(f).descricao for f in p.aponta_para) or '—'} | "
        f"{'; '.join(q.descricao for q in caso.pistas if q.id in p.exige_pistas) or '—'} |"
        for p in caso.pistas
    ]
    condicao = caso.condicao_acerto
    provas = [p.descricao for p in caso.pistas if p.id in condicao.provas_minimas]
    return "\n".join(
        [
            f"# Caso {numero}: {pronto.titulo}",
            "",
            "> Gerado por `tools/gerar_docs.py`. Contém **spoilers** (a solução está no fim).",
            "",
            f"- Chave: `{pronto.chave.value}`",
            f"- Mapa: {mapa.titulo} (`{pronto.mapa.value}`) · o detetive entra por `{mapa.entrada}`",
            f"- Crime: {caso.personagem(caso.crime.vitima_id).nome}, {caso.crime.metodo.value}, "
            f"{_hora(caso.crime.instante)}, {caso.mapa.nome(caso.crime.local_id)}",
            "",
            "## Apresentação (o que todos sabem)",
            "",
            pronto.apresentacao,
            "",
            "## Elenco",
            "",
            "| Personagem | Persona | Papel | Função na história |",
            "| --- | --- | --- | --- |",
            *elenco,
            "",
            "## Fatos do caso",
            "",
            *fatos,
            "",
            "## Linha do tempo",
            "",
            *linha,
            "",
            "## Agenda inicial",
            "",
            "| Personagem | Local | Período |",
            "| --- | --- | --- |",
            *agenda,
            "",
            "## Álibis",
            "",
            "| Personagem | Local | Período | Situação | Desmentido por |",
            "| --- | --- | --- | --- | --- |",
            *alibis,
            "",
            "## Pistas",
            "",
            "| Pista | Local | Tipo | Aponta para | Exige |",
            "| --- | --- | --- | --- | --- |",
            *pistas,
            "",
            "## Solução",
            "",
            f"Culpado: **{caso.personagem(caso.culpado_id).nome}**. "
            f"Cadeia: {'; '.join(caso.fato(f).descricao for f in caso.cadeia_solucao)}.",
            "",
            f'Para acusar com sucesso: motivo "{caso.fato(condicao.motivo_fato_id).descricao}" '
            f"e ao menos {condicao.quantas_provas} entre: {'; '.join(provas)}.",
            "",
            pronto.solucao,
            "",
        ]
    )


def nome_do_arquivo_do_caso(numero: int, chave: ChaveCaso) -> str:
    return f"casos/{numero:02d}-{chave.value.replace('_', '-')}.md"


def gerar_tudo() -> dict[str, str]:
    arquivos = {"elenco.md": documentar_elenco(), "mapas.md": documentar_mapas()}
    for numero, (chave, pronto) in enumerate(CATALOGO.items(), start=1):
        arquivos[nome_do_arquivo_do_caso(numero, chave)] = documentar_caso(numero, pronto)
    return arquivos


def escrever(pasta: Path) -> list[Path]:
    escritos = []
    for nome, texto in gerar_tudo().items():
        destino = pasta / nome
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8", newline="\n")
        escritos.append(destino)
    return escritos
