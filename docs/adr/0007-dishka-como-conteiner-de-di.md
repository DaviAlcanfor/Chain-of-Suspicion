# 0007 — Dishka como contêiner de injeção de dependência

- Status: aceita
- Substitui: 0005

## Contexto

A ADR 0005 deixou Wireup ou Dishka em aberto. Ambos foram instalados e importados em Python 3.14 junto com FastAPI e LangGraph.

## Decisão

Dishka. Escopos nativos (`APP`, `REQUEST`, etc.) e integração oficial com FastAPI e WebSocket; o grafo de dependências é validado ao subir. Testes trocam providers inteiros por falsos.

## Consequências

- Serviços e provedores de LLM são singleton no escopo `APP`.
- Escopo por partida (critério 2 da 0005) não é usado ainda; entra com o motor (spec 003).
- Se Dishka atrapalhar, a troca para Wireup fica restrita à pasta `di/`.
