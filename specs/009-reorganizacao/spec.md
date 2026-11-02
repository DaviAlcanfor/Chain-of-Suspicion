# 009 — Reorganização do código, aparência em enum, tools de decisão e contexto por pasta

- Status: implementada (2026-11-02)
- Depende de: 007, 008, ADR 0012

## Problema

O pacote cresceu: 13 módulos soltos na raiz de `src`, settings e modelos em um arquivo só, aparência dos personagens em texto livre e um único `AGENTS.md` grande, que consome contexto de qualquer agente que trabalhe em qualquer parte do projeto.

## Objetivos

- Regras puras agrupadas em `dominio/`; só o `main.py` fica na raiz.
- Settings e modelos de LLM em arquivos pequenos e separados.
- Aparência e cores das personas como enums, com texto livre só onde o LLM lê.
- Uma `StructuredTool` por tipo de pergunta de decisão, mapeada em `agentes/tools/`.
- Um `AGENTS.md` curto por pasta e `docs/CATALOGO.md` como índice, para cada agente carregar só o necessário.

## Fora de escopo

- Mudar comportamento do jogo, dos prompts ou da API.
- Usar as tools de decisão no fluxo (o código continua chamando o decisor direto, ADR 0011).

## Requisitos

- R1. `dominio/` contém `base, ids, enums, relogio, calendario, mapa, caso, mundo, acoes, regras, eventos`; nenhum módulo de `dominio/` importa outra camada.
- R2. `turno.py` vive em `agentes/`; a raiz de `src/chain_of_suspicion/` só tem `__init__.py` e `main.py`.
- R3. `config/` tem um arquivo por grupo de settings (`api_keys`, `llm`, `jogo`) e `settings.py` apenas as agrega; os modelos se dividem em `modelos_llm`, `perfis` e `precos`.
- R4. `Aparencia` usa enums (`CorDeCabelo`, `EstiloDeCabelo`, `TomDePele`, `PecaDeRoupa`, `Acessorio`, `Paleta`); cada cor tem seu hex em um mapa; `nota_de_arte` guarda o que o enum não cobre.
- R5. Cada `PerguntaDeDecisao` tem uma `StructuredTool` com schema de argumentos tipado, criada por `criar_ferramentas(decisor)`, com os schemas em `ESQUEMA_DOS_ARGUMENTOS`; chamar a tool devolve o mesmo resultado que o decisor.
- R6. Cada pasta de código, mais `tests/`, `specs/`, `docs/` e `godot/`, tem `AGENTS.md` de no máximo 60 linhas e um `CLAUDE.md` com `@AGENTS.md`.
- R7. `docs/CATALOGO.md` lista cada `AGENTS.md`, o que a pasta contém e quando ler; o `AGENTS.md` da raiz só tem princípios, comandos e esse ponteiro.
- R8. Os testes espelham as pastas do pacote.

## Critérios de aceite

- [x] `pytest`, `mypy --strict` e `ruff` verdes, com o mesmo número de testes ou mais.
- [x] A raiz de `src/chain_of_suspicion/` só tem `__init__.py` e `main.py`.
- [x] Nenhuma cor de persona é string solta; `docs/elenco.md` continua gerado e sem divergência.
- [x] Teste confere que todo `AGENTS.md` citado no catálogo existe, tem `CLAUDE.md` irmão e cabe em 60 linhas.

## Riscos e perguntas em aberto

- O Claude Code só carrega contexto aninhado via `CLAUDE.md`; sem os arquivos irmãos o `AGENTS.md` de pasta não seria lido por ele.
- As tools de decisão ficam sem uso no fluxo até um agente de LLM precisar chamá-las.
- `ContextoDoTurno.pistas` continua vazio e `ACUSAR` fora do laço (limites da spec 008, spec 003).
- Cada persona ganhou `TomDePele` e `PelosFaciais` novos; os valores são palpite do autor e devem ser revistos com o dono do projeto antes da arte.
- Os testes de `dominio/` ainda usam `tests/caso_exemplo.py` (mapa próprio), não os casos reais.
