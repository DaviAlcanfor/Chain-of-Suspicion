# 0012 — Contexto por pasta e `dominio/`

- Status: aceita

## Contexto

Um único `AGENTS.md` cresce com o projeto e entra inteiro no contexto de qualquer agente, mesmo quando ele só mexe numa pasta. Contexto longo piora a atenção do modelo e custa tokens.

## Decisão

- Um `AGENTS.md` curto (até 60 linhas) por pasta, mais um `CLAUDE.md` irmão com `@AGENTS.md`, porque o Claude Code só carrega contexto aninhado por `CLAUDE.md`; os demais agentes leem o `AGENTS.md`.
- O `AGENTS.md` da raiz fica com princípios, comandos e o ponteiro para `docs/CATALOGO.md`, que diz qual arquivo ler para cada tarefa.
- As regras puras vão para `dominio/`; a raiz do pacote só tem `main.py`.

## Consequências

- Quem trabalha em `api/` não carrega as regras de `conteudo/`, e vice-versa.
- Um teste confere que o catálogo, os `AGENTS.md` e os `CLAUDE.md` irmãos continuam consistentes.
- Ao criar uma pasta nova, é preciso criar os dois arquivos e uma linha no catálogo.
