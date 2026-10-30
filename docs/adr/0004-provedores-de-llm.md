# 0004 — Provedores de LLM

- Status: aceita (valores conferidos em 30/10/2026; preços mudam, reconfira antes de orçar)

## Contexto

Há muitas chamadas simultâneas e o custo por partida precisa ser baixo. Dois papéis distintos: modelo que **fala e raciocina** e modelo que **decide** (respostas curtas e fechadas).

## Decisão

| Papel | Modelo | Dados relevantes |
| --- | --- | --- |
| Fala e raciocínio | **GPT-6 Luna** (`gpt-6-luna`, OpenAI) | US$ 0,10/M entrada, US$ 0,50/M saída, cache de entrada US$ 0,01/M; contexto de ~1M tokens; saída até 128k; esforço de raciocínio de `none` a `max`; saídas estruturadas e escolha de ferramenta; temperatura não configurável; acima de 272k tokens de entrada o preço da requisição sobe (US$ 0,20 / 0,75) |
| Decisão | **Jev** (TypeSafe AI) ou **d1-ultra** (Liquid AI) | d1-ultra: ~US$ 0,042/M entrada, contexto de 32k. Escolha final por medição (spec 004) |

Ambos ficam atrás de `ProvedorLLM` (Protocol assíncrono). O motor não importa SDK de fornecedor.

## Consequências

- Como a temperatura do Luna não é configurável, a variedade entre personagens vem do prompt e do papel, não de ajuste de temperatura.
- Esforço de raciocínio vira configuração por papel: baixo para inocentes, maior para detetive e assassino.
- Não confundir com **GPT-5.6 Luna**, modelo anterior e mais caro (US$ 0,20 / 1,20).

## Fontes

- https://apidog.com/blog/what-is-gpt-6-luna/
- https://www.sim.ai/models/openai/gpt-6-luna
