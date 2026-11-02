# 0013 — Ferramentas do projeto: uv, just, CI e ganchos

- Status: aceita (versões conferidas em 02/11/2026)

## Contexto

O projeto rodava com `pip` e comandos soltos, sem versão de Python fixada, sem lock de dependências, sem CI e com quebras de linha misturadas (LF e CRLF) por causa do Windows.

## Decisão

- **uv** gerencia ambiente e dependências; `uv.lock` é versionado e o CI usa `uv sync --locked`. `.python-version` fixa o 3.14 (ADR 0008).
- Ferramentas de desenvolvimento ficam em `[dependency-groups].dev` (o `uv run` já as instala); `[build-system]` usa setuptools e inclui os `.md` dos prompts no pacote.
- **just** reúne as tarefas (`instalar`, `checar`, `testar`, `lint`, `tipos`, `docs`, `rodar`, `atualizar`, `hooks`), com shell PowerShell no Windows.
- **CI** no GitHub Actions: `ruff`, `mypy` e `pytest` em cada PR e em `main`.
- **pre-commit** leve (`ruff-check`, arquivos grandes, conflito de merge, fim de linha), instalado por `just hooks` via `uvx`, sem entrar nas dependências.
- `.gitattributes` (`eol=lf`) e `.editorconfig` fixam LF; arquivos de Godot usam tabulação.

## Consequências

- `pip install -e ".[dev]"` deixa de ser o caminho; o comando é `just instalar` (ou `uv sync`).
- Dependência nova exige `uv lock` e commit do `uv.lock`.
- Ficaram de fora, por ora: Docker, `CHANGELOG`, `CONTRIBUTING` (o `AGENTS.md` cumpre esse papel) e dependabot.
- O workflow do CI só pode ser validado no GitHub: ele não rodou localmente.
