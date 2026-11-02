# 0005 — Injeção de dependência: Wireup ou Dishka

- Status: substituída pela 0007

## Contexto

A API precisa injetar provedores de LLM, repositório, relógio e configuração, e trocá-los por falsos em teste.

## O que foi verificado

Wireup: DI guiado por tipos, integração nativa com FastAPI (`wireup.integration.fastapi.setup(container, app)`), `Injected[T]`, contêiner assíncrono, ciclos de vida singleton/escopo/transiente, validação na partida da aplicação e `container.override` para testes.

Dishka **não foi avaliado**. Antes de decidir, comparar com os mesmos critérios.

## Critérios de decisão

1. Integração com FastAPI e com o laço assíncrono do LangGraph.
2. Escopo por partida (cada partida tem seu próprio escopo de dependências).
3. Validação de grafo de dependências na inicialização.
4. Facilidade de override em teste.
5. Manutenção ativa e documentação.

## Decisão provisória

Começar sem contêiner: construir dependências em uma função `montar_aplicacao()` e passá-las explicitamente. A spec 005 troca isso pelo contêiner escolhido. Dependência simples demais não justifica biblioteca no início.
