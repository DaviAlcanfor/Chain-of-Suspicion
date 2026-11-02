# AGENTS.md

Instruções para qualquer agente de código (Claude Code, Codex, Cursor etc.) neste repositório. Este arquivo é curto de propósito: o resto do contexto fica em arquivos por pasta.

## O que é o projeto

Simulação de mistério de assassinato em que **agentes de IA jogam entre si**: um assassino, um detetive, inocentes e uma vítima. Um humano poderá assumir o lugar de um agente depois, pela mesma porta de ação. O backend é Python (FastAPI, LangGraph, Dishka); o cliente 3D é Godot, que só mostra e comanda, sem regra de jogo.

Dono do projeto: analista de dados, forte em Python, com pouca vivência em back-end e front-end. Quando um conceito de back ou front aparecer, explique devagar e do básico. Seja realista: aponte problemas em vez de concordar com tudo.

## Como carregar contexto (leia isto antes de abrir arquivos)

1. Leia este arquivo.
2. Abra `docs/CATALOGO.md` e ache a pasta da tarefa.
3. Leia **só** o `AGENTS.md` dessa pasta (e o do pai, se o catálogo mandar).
4. Não leia os `AGENTS.md` das outras pastas, nem specs ou ADRs que a tarefa não cita.

Ao criar uma pasta nova: crie `AGENTS.md` (até 60 linhas), um `CLAUDE.md` irmão com `@AGENTS.md` e uma linha no catálogo. Um teste confere isso.

## Fluxo obrigatório: Spec-Driven Development

Nenhuma funcionalidade nasce direto no código.

1. Leia `specs/constitution.md` (princípios que nunca mudam).
2. Ache ou crie a pasta `specs/NNN-nome/` da funcionalidade.
3. Escreva ou atualize, nesta ordem: `spec.md`, `plan.md`, `tasks.md` (modelos em `specs/_templates/`).
4. Só depois implemente, uma tarefa por vez, começando pelo teste.
5. Se o código divergir da spec, **a spec é corrigida primeiro**.
6. Decisão de arquitetura vira ADR em `docs/adr/`, numerada e imutável (a nova substitui a antiga).

Não implemente spec em `rascunho` sem pedir aprovação.

## Comandos

Ambiente: Python 3.14 em `.venv` (ADR 0008).

```bash
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m mypy
.venv/Scripts/python.exe -m ruff check .
.venv/Scripts/python.exe tools/gerar_docs.py
uvicorn chain_of_suspicion.main:app --reload
```

Uma tarefa só termina com `pytest`, `mypy` e `ruff` verdes. Se mexer em `conteudo/`, rode também `gerar_docs.py` (um teste falha se `docs/` divergir).

## O que não fazer

- Não adicionar dependência sem registrar o motivo no `plan.md` da spec.
- Não editar ADR antiga; crie outra que a substitui.
- Não colocar segredo, chave de API ou `.env` no repositório.
- Não declarar tarefa pronta sem rodar os três comandos acima.
- Não rodar `ruff format` em arquivos que você não criou (gera diff de formatação alheio).
