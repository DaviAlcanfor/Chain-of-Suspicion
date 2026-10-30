# Jogo investigativo

Simulação de mistério em que agentes de IA (assassino, detetive, inocentes) jogam entre si. Backend em Python, cliente 3D em Godot.

## Estado atual

| Spec | Tema | Status |
| --- | --- | --- |
| 001 | Domínio do caso | implementada |
| 002 | Calendário e relógio | implementada |
| 003 | Motor de simulação (LangGraph) | rascunho |
| 004 | Camada de LLM | rascunho |
| 005 | API FastAPI | rascunho |
| 006 | Cliente Godot | rascunho (esqueleto em `godot/`) |

## Rodando

```
pip install -e ".[dev]" --break-system-packages
python3 -m pytest -q
python3 -m mypy
ruff check .
```

## Como trabalhamos

Spec-Driven Development: `specs/constitution.md` → `spec.md` → `plan.md` → `tasks.md` → código. Detalhes em `AGENTS.md`. Decisões de arquitetura em `docs/adr/`.

## Godot

Abra a pasta `godot/` no Godot 4 (Importar → `project.godot`). Veja `godot/README.md`.
