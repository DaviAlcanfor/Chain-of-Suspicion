# 0001 — LangGraph para orquestrar a simulação

- Status: aceita

## Contexto

A partida é um laço com estado, ramificações (interrogatório, recusa de ação) e necessidade de reproduzir. Deep Agents é um *harness* construído sobre LangGraph, voltado a agentes que planejam e usam sistema de arquivos; aqui os papéis e as ações são fixos e as regras estão em código.

## Decisão

Usar LangGraph diretamente: grafo com estado tipado, subgrafo de interrogatório, checkpoints para pausar e retomar.

## Consequências

- Controle explícito de cada passo, fácil de testar com agentes falsos.
- Mais código nosso do que usando um harness pronto.
- Se um dia um agente precisar planejar livremente, ele pode ser um nó que usa Deep Agents por dentro.
