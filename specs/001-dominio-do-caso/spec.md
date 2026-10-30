# 001 — Domínio do caso

- Status: implementada
- Depende de: 002-calendario

## Problema

Para agentes jogarem sozinhos, o mundo precisa existir como dado validado, com regras em código: quem é o culpado, onde cada um estava, o que cada um sabe, que ações cada papel pode fazer.

## Objetivos

- Representar o caso completo (`Caso`) como verdade única e rejeitar casos inconsistentes na criação.
- Dar a cada agente uma visão restrita (`VisaoPersonagem`).
- Validar ações em código (`validar_acao`) e julgar acusações sem LLM (`JuizDeterministico`).

## Fora de escopo

- Gerar casos automaticamente (spec futura).
- Qualquer chamada a LLM.

## Requisitos

- R1. Um caso tem exatamente um assassino, um detetive e uma vítima, e ao menos um inocente.
- R2. Todo id é `NewType` sobre `UUID`; papéis, métodos, objetivos, pistas e ações são enums.
- R3. A agenda mapeia cada personagem (menos o detetive) a locais e intervalos, sem sobreposição e com tempo de deslocamento suficiente pelo `Mapa`.
- R4. Assassino e vítima estão no local do crime no instante do crime.
- R5. Álibi falso precisa de fato que o desminta; álibi verdadeiro não pode ser desmentido.
- R6. Toda pista é alcançável e todo fato da cadeia de solução tem ao menos uma pista relevante.
- R7. Cada papel só executa as ações de `PERMISSOES`; ações com alvo exigem mesmo local; só a vítima do caso pode ser morta; `MOVER` só vai a vizinho direto.
- R8. Pressão sobe estresse; segredo só sai acima do limite, com a prova certa, e se o modelo de decisão estiver confiante além da margem de incerteza. Insistir além de 3 vezes torna o personagem hostil.
- R9. `JuizDeterministico` aprova só com culpado certo, motivo certo e provas mínimas distintas que o jogador realmente encontrou.
- R10. `VisaoPersonagem` não contém fatos que o personagem não sabe.

## Critérios de aceite

- [x] 87 testes passam, `mypy --strict` e `ruff` limpos.
- [x] Cada regra de R1 a R10 tem ao menos um teste que falha se a regra for removida.
