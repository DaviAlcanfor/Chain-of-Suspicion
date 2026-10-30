# 003 — Motor de simulação

- Status: rascunho
- Depende de: 001, 002

## Problema

Falta o laço que faz os agentes jogarem: avançar o tempo, dar a vez a cada personagem, validar o que ele propõe e registrar o que aconteceu.

## Objetivos

- Rodar uma partida completa sem humano e sem rede (com agentes falsos) e com LLM (spec 004).
- Registrar tudo num log de eventos que permita reproduzir a partida.

## Fora de escopo

- Prompts, provedores de LLM e HTTP.

## Requisitos

- R1. O motor é um grafo LangGraph com estado tipado: `Mundo`, log de eventos, vez atual, orçamento restante.
- R2. Em cada passo: escolher quem age → montar `VisaoPersonagem` → pedir decisão ao agente (`Protocol Agente`) → `validar_acao` → aplicar ou registrar recusa.
- R3. Ação recusada não altera o mundo; o agente recebe o motivo e tem no máximo N novas tentativas, depois assume `ESPERAR`.
- R4. Interrogatório é um subgrafo: detetive pressiona, modelo de decisão estima ameaça, `aplicar_pressao` decide se o segredo sai, o personagem responde.
- R5. A partida termina com acusação julgada, estouro de dias do caso ou estouro de orçamento (passos, tokens ou custo).
- R6. Todo evento é imutável, com id, instante, ator, ação e resultado; o log é append-only.
- R7. Dada a mesma seed e as mesmas respostas de agente gravadas, a partida sai idêntica.
- R8. O motor aceita um `Agente` humano no lugar de qualquer agente de IA sem mudar o laço.

## Critérios de aceite

- [ ] Partida completa com agentes falsos termina em acusação certa e em acusação errada.
- [ ] Reexecutar com o log gravado reproduz o mesmo final.
- [ ] Ação inválida proposta pelo agente nunca altera o `Mundo`.

## Perguntas em aberto

- Turnos por passo de tempo fixo ou por evento? Proposta inicial: passo de tempo fixo configurável (ex.: 10 min simulados).
- Os inocentes agem a cada passo ou só quando algo os envolve (para economizar chamadas)?
