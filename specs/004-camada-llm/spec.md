# 004 — Camada de LLM

- Status: aprovada (estrutura em 007)
- Depende de: 003, ADR 0004

## Problema

Os agentes precisam de prompts, de acesso a modelos e de ferramentas, sem acoplar o motor a um fornecedor.

## Requisitos

- R1. `ProvedorLLM` é um `Protocol` assíncrono; implementações: GPT-6 Luna (raciocínio e fala), modelo de decisão (Jev ou d1-ultra) e um falso para testes.
- R2. O prompt de cada agente é gerado a partir da `VisaoPersonagem` e do papel, não escrito um por personagem. Papéis diferem em instruções e em ferramentas.
- R3. As ferramentas de um agente são derivadas de `PERMISSOES[papel]`; um papel nunca recebe ferramenta que não pode usar.
- R4. A saída do agente é estruturada (`Acao` mais fala opcional) e validada por pydantic antes de chegar ao motor.
- R5. "Decidir antes de falar": o modelo de decisão responde uma pergunta fechada (ex.: ameaça de 0 a 1; contradição sim/não) e o LLM só então produz a fala, recebendo essa decisão como contexto.
- R6. Toda chamada tem timeout, retry com backoff (tenacity), semáforo de concorrência e registro de tokens e custo.
- R7. Respostas são gravadas no log da partida para replay.
- R8. Prompt caching: parte estável do prompt (regras, papel) vem antes da parte variável.

## Critérios de aceite

- [ ] Troca de provedor sem mudar o motor.
- [ ] Estouro de timeout vira `ESPERAR`, não derruba a partida.
- [ ] Custo por partida é reportado ao fim.

## Perguntas em aberto

- Jev ou d1-ultra como decisor padrão? Medir em casos de teste antes de decidir (precisão e latência).
- Chamadas de inocentes em lote para reduzir custo?
