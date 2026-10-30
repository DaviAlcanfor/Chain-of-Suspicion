# 0003 — PostgreSQL para persistência

- Status: proposta (só entra quando a spec 005 precisar persistir)

## Decisão proposta

PostgreSQL, com:

- `uuid` nativo para os ids;
- `tstzrange` e *exclusion constraint* para impedir presença sobreposta de um personagem;
- `jsonb` para snapshots do `Caso` e do `Mundo`;
- tabela de eventos append-only como log da partida.

## Consequências

- Até lá, o repositório de partidas é uma interface (`Protocol`) com versão em memória.
- Não adiciona dependência antes da hora.
