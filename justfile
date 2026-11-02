set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# Lista as tarefas
default:
    @just --list

# Cria o .venv e instala tudo (inclui as ferramentas de desenvolvimento)
instalar:
    uv sync

# Roda os testes (ex.: just testar tests/agentes -x)
testar *args:
    uv run pytest -q {{args}}

# Verifica estilo e erros comuns
lint:
    uv run ruff check .

# Verifica os tipos (mypy --strict)
tipos:
    uv run mypy

# Tudo o que precisa estar verde antes de dar uma tarefa por pronta
checar: lint tipos testar

# Regenera docs/elenco.md, docs/mapas.md e docs/casos/
docs:
    uv run python tools/gerar_docs.py

# Sobe a API em http://127.0.0.1:8000 (precisa de AI_GATEWAY_API_KEY no .env para criar partidas)
rodar:
    uv run uvicorn chain_of_suspicion.main:app --reload

# Atualiza as dependências dentro dos limites do pyproject e regrava o uv.lock
atualizar:
    uv lock --upgrade

# Liga os ganchos de pré-commit neste clone
hooks:
    uvx pre-commit install
