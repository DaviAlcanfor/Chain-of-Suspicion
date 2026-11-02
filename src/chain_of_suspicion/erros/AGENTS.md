# AGENTS.md — `erros/`

Exceções de domínio e códigos de erro. Sem HTTP aqui.

## Arquivos

| Arquivo | O que tem |
| --- | --- |
| `excecoes.py` | `ErroJogo` e subclasses (`PartidaNaoEncontrada`, `AcaoRecusada`, `FalhaNoLLM`, `TempoEsgotadoNoLLM`, `OrcamentoEstourado`, `ProvedorIndisponivel`, `CasoIndisponivel`, `PartidaEmEstadoInvalido`) |
| `codigos.py` | `ErrorCode` (StrEnum) e `ErrorResponse` (corpo de erro da API) |

## Regras desta pasta

- Toda exceção nova herda de `ErroJogo` e declara `codigo: ClassVar[ErrorCode]`.
- Exceção nova => item em `ErrorCode` e linha em `api/handlers.py::STATUS_POR_ERRO`.
- A mensagem é lida pelo usuário final: sem stack, sem caminho, sem segredo.
- `FalhaNoLLM` (e `TempoEsgotadoNoLLM`) vira `ESPERAR` no grafo; `OrcamentoEstourado` encerra a partida.
- Erro inesperado (`Exception`) nunca vaza detalhe: o handler genérico devolve 500 fixo.

## Testes

`tests/config/test_config.py` (códigos) e `tests/api/test_api.py` (tradução para HTTP).
