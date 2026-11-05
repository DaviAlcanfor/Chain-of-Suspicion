# Chain of Suspicion

Simulação de mistério de assassinato em que **agentes de IA jogam entre si**: um assassino, um detetive, inocentes e uma vítima. O backend é Python (FastAPI, LangGraph, Dishka); o cliente 3D é Godot e só mostra o que a API manda.

## Estado atual

| Parte | Situação |
| --- | --- |
| Domínio do caso, calendário, ações e regras | pronto (specs 001, 002) |
| Camadas de LLM, decisão, grafo, serviços e API | prontas e testadas com falsos (specs 004, 005, 007, 008) |
| 12 personas, 3 mapas e 5 casos | prontos, com docs geradas em `docs/` (spec 008) |
| Pistas, acusação e interrogatório no laço | **faltam** (spec 003) |
| Teste contra o Gateway real | **não feito** (falta chave) |
| Cliente Godot | esqueleto ligado à API (spec 006) e fatia de arte com partida gravada (spec 010) |
| Direção de arte | decidida em `docs/arte/direcao.md`; 1 de 24 salas e as 12 personas |

## Rodando

Precisa de [uv](https://docs.astral.sh/uv/) e [just](https://github.com/casey/just). O Python 3.14 vem do `.python-version`.

```bash
just instalar   # cria o .venv e instala tudo
just checar     # ruff + mypy + pytest (tudo precisa estar verde)
just rodar      # API em http://127.0.0.1:8000
just            # lista as outras tarefas
```

Para criar partidas de verdade, copie `.env.example` para `.env` e preencha `AI_GATEWAY_API_KEY` (chave do Vercel AI Gateway). Sem ela, `GET /saude` funciona e `POST /partidas` responde 503.

Sem `just`: troque `just checar` por `uv run ruff check . && uv run mypy && uv run pytest -q`.

## Como o repositório se organiza

- `src/chain_of_suspicion/`: o código, em camadas (`dominio`, `config`, `conteudo`, `prompts`, `infra`, `agentes`, `servicos`, `api`, `di`).
- `specs/`: uma pasta por funcionalidade (`spec.md`, `plan.md`, `tasks.md`).
- `docs/`: decisões (`adr/`), elenco, mapas e casos (gerados), e o catálogo.
- `tests/`: espelha as pastas do código.
- `godot/`: cliente 3D.

## Como trabalhamos

Spec-Driven Development: `specs/constitution.md` → `spec.md` → `plan.md` → `tasks.md` → código. Cada pasta tem um `AGENTS.md` curto; o ponto de partida é o `AGENTS.md` da raiz e o `docs/CATALOGO.md`, que dizem o que ler para cada tarefa.

## Godot

Abra a pasta `godot/` no Godot 4 (Importar → `project.godot`). Veja `godot/README.md`.
