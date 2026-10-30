# 002 — Calendário e relógio

- Status: implementada

## Problema

O relógio sozinho não basta: o caso dura vários dias, há dia e noite, e os personagens se movem ao longo deles.

## Requisitos

- R1. `Relogio` é um `Protocol` com `RelogioReal` e `RelogioSimulado`; o simulado só avança.
- R2. `Calendario` define início, número de dias e horários de nascer e pôr do sol.
- R3. `Calendario.dia_do_caso` conta de 1; `periodo` devolve `PeriodoDoDia` (madrugada, manhã, tarde, noite); `eh_noite` vale para madrugada e noite.
- R4. `Caso` recusa crime, evento, agenda ou álibi fora da janela de dias.
- R5. Deslocamento e sobreposição valem através da meia-noite.
- R6. `Mundo` expõe `dia` e `periodo` a partir do relógio e recusa instante fora do caso.
- R7. A `VisaoPersonagem` descreve horários como "dia N, HH:MM (período)".

## Critérios de aceite

- [x] Testes cobrem fronteiras de período, virada de dia, agenda em vários dias e rejeição fora da janela.

## Ideias para depois (não fazem parte desta spec)

- Regras que dependem de período: visibilidade menor à noite, locais fechados de madrugada, ações que só ocorrem de dia.
- Fusos diferentes entre sessões de jogo.
