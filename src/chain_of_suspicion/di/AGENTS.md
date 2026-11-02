# AGENTS.md — `di/`

Injeção de dependência com Dishka (ADR 0007). É o único lugar que conhece todas as camadas.

## Arquivo

`provedores.py`: `ProvedorDeConfiguracao`, `ProvedorDeLLM`, `ProvedorDePartidas` e `montar_container(*extras)`.

## Regras desta pasta

- Tudo em escopo `APP` (singleton). Escopo por partida entra com a spec 003.
- Provider cria recursos de forma preguiçosa: sem chave, só quem usa o Gateway falha (503); `/saude` continua ok.
- `httpx.AsyncClient` é gerado com `yield` para ser fechado no shutdown.
- Teste troca dependência com `@provide(override=True)` num `Provider` extra passado a `montar_container`.
- Sem lógica aqui: só ligar construtores. Regra nova vai para a camada dona dela.
- Construtor com mais de 3 dependências: agrupe (ex.: `MontadorDePartida`), não aumente a lista.

## Testes

`tests/api/test_api.py` (usa os overrides).
