# AGENTS.md — `specs/`

Uma pasta por funcionalidade, com `spec.md` (o quê e por quê), `plan.md` (como) e `tasks.md` (passos).

## Estrutura

| Caminho | O que tem |
| --- | --- |
| `constitution.md` | princípios que nunca mudam (mudar exige ADR) |
| `_templates/` | modelos de `spec.md`, `plan.md`, `tasks.md` |
| `001`–`010` | ver a lista em `docs/CATALOGO.md` |

## Regras desta pasta

- Status no topo da spec: `rascunho`, `aprovada`, `implementada`. Não implemente `rascunho` sem aprovação.
- Requisitos têm id (`R1`...), cabem numa frase e são verificáveis; critérios de aceite são checklist.
- Tarefas referenciam requisitos e são pequenas e testáveis.
- Código divergiu da spec? **Corrija a spec primeiro.**
- Registre limites conhecidos em "Riscos e perguntas em aberto"; spec não afirma mais do que o código faz.
- Dependência nova entra no `plan.md`, com motivo.
- Spec nova ganha número seguinte (`011-...`) e linha no catálogo.

## Leitura mínima por tarefa

A constituição + a spec da funcionalidade + o `AGENTS.md` da pasta de código. Não leia as demais specs.
