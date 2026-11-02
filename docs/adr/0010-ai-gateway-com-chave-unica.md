# 0010 — Vercel AI Gateway com chave única

- Status: aceita (verificado em 02/11/2026)
- Substitui: 0009

## Contexto

A ADR 0009 assumia um provedor por modelo, com chaves e `base_url` separados. O catálogo do Gateway (`/v1/models`) lista todos os modelos escolhidos, e a API de decisão (`POST /v1/evaluate`) aceita `boolean`, `choice` e `score`.

## Decisão

- Uma chave: `AI_GATEWAY_API_KEY`. Chat em `https://ai-gateway.vercel.sh/v1` (OpenAI-compatível); decisões em `POST /v1/evaluate`.
- Fala e raciocínio: `openai/gpt-6-luna` (padrão) e `anthropic/claude-haiku-5.5`.
- Decisão: `liquid/d1-ultra` (padrão), `typesafe-ai/jev` e `openai/gpt-6-luna-decisions`.
- Cada modelo é um item de `StrEnum` cujo valor é o ID do Gateway.

## Consequências

- Somem `Provedor`, as chaves e os `base_url` por provedor; `langchain-anthropic` deixa de ser necessário.
- O custo real vem em `providerMetadata.gateway.cost` e alimenta o teto de custo.
- A escolha do decisor padrão continua por medição (ADR 0004).
