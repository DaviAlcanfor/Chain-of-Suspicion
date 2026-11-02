# 005 — API FastAPI

- Status: aprovada (estrutura em 007)
- Depende de: 003, 004, ADR 0005

## Problema

O cliente (Godot, e depois qualquer outro) precisa iniciar partidas, acompanhar o que acontece e, no futuro, jogar como humano.

## Conceito rápido (para quem vem de dados)

Uma API é um programa que fica escutando pedidos por rede. HTTP serve para "pedido e resposta" (criar partida, consultar estado). WebSocket é uma conexão aberta em que o servidor empurra novidades sem ser perguntado, ideal para transmitir eventos ao vivo.

## Requisitos

- R1. `POST /partidas` cria uma partida a partir de uma seed e de uma configuração; devolve `partida_id`.
- R2. `GET /partidas/{id}` devolve status (`criada`, `em_andamento`, `encerrada`), dia atual e período.
- R3. `GET /partidas/{id}/estado` devolve o estado visível ao cliente: posições, mortos, últimas falas. Nunca devolve segredos nem a verdade do caso em partida em andamento.
- R4. `WS /partidas/{id}/eventos` transmite cada evento do log em JSON, em ordem, com número sequencial para o cliente retomar de onde parou.
- R5. `POST /partidas/{id}/acoes` aceita uma `Acao` de um jogador humano; passa pelo mesmo `validar_acao` dos agentes.
- R6. `POST /partidas/{id}/pausar` e `/retomar` controlam a simulação.
- R7. Esquemas de entrada e saída são modelos pydantic; contratos publicados em `/openapi.json`.
- R8. Dependências (provedores de LLM, repositório, relógio) são injetadas pelo contêiner de DI escolhido na ADR 0005, com troca por falsos nos testes.
- R9. Partidas rodam como tarefas assíncronas em segundo plano; a requisição HTTP nunca espera a partida terminar.
- R10. `GET /saude` devolve `{"status": "ok"}`; é o que o esqueleto do Godot consulta.

## Critérios de aceite

- [ ] Teste de contrato: o evento enviado pelo WebSocket valida contra o esquema publicado.
- [ ] Cliente reconectando com `ultimo_evento=N` recebe só os eventos depois de N.
- [ ] Rota de estado nunca contém fatos secretos (teste de vazamento).

## Perguntas em aberto

- Autenticação: não necessária enquanto roda local; decidir antes de qualquer deploy.
