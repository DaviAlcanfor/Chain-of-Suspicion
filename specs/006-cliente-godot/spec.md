# 006 — Cliente Godot

- Status: rascunho
- Depende de: 005

## Problema

Quero ver a simulação acontecendo num mundo 3D, e no futuro andar por ele.

## Estratégia em fases

O cliente só cresce depois que o motor joga uma partida inteira (specs 003 a 005). Antes disso, só o esqueleto em `godot/`.

- Fase 0 (existe): esqueleto que conecta na API e imprime eventos.
- Fase 1: cena fixa com os locais como salas e personagens como cápsulas que se teleportam conforme eventos de movimento.
- Fase 2: movimento animado entre salas, ciclo de dia e noite visual, balões de fala.
- Fase 3: jogador humano anda em primeira pessoa e envia ações pela API.

## Requisitos

- R1. O cliente não contém regra de jogo; toda mudança de estado vem de evento da API.
- R2. `ApiClient` cobre as chamadas HTTP; `EventStream` mantém o WebSocket, reconecta e retoma pelo número do último evento.
- R3. A configuração (URL base) fica fora do código, em `godot/config.cfg`.
- R4. Cada local do `Mapa` corresponde a uma cena de sala identificada pelo mesmo `LocalId` recebido da API.
- R5. O período do dia recebido nos eventos controla a luz da cena (fase 2).

## Critérios de aceite

- [ ] Fase 0: com a API no ar, rodar o projeto imprime o status da API e cada evento recebido.
- [ ] Fase 1: um evento `mover` muda a posição visível do personagem.

## Riscos

- Godot é novo para o dono do projeto: a fase 0 é pequena de propósito para aprender o ciclo cena → script → sinal antes de modelar qualquer sala.
