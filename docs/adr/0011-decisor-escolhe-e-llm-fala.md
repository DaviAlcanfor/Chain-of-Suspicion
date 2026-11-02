# 0011 — O decisor escolhe a ação; o LLM só fala

- Status: aceita

## Contexto

Na spec 007 o LLM escolhia ação e fala numa só chamada. O modelo de decisão (Jev, d1-ultra, Luna-decisions) responde perguntas fechadas com probabilidades, mais barato e rápido que um LLM de raciocínio.

## Decisão

Turno em duas etapas. (1) O decisor escolhe o tipo de ação entre as viáveis (`choice`) e os alvos (`choice`); para ações com fala responde também se o personagem deve mentir (`boolean`). (2) O LLM escreve a fala recebendo essas decisões como contexto, e só é chamado quando a ação envolve fala.

## Consequências

- `MOVER`, `ESPERAR` e `OBSERVAR` não gastam chamada de LLM.
- O decisor nunca sobrescreve regra: a escolha passa por `validar_acao`, e ação recusada volta com o motivo.
- A personalidade do personagem chega ao decisor pelo `state` (texto do turno), não por ajuste de modelo.
