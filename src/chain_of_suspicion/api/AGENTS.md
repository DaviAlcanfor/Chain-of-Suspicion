# AGENTS.md — `api/`

FastAPI para o Godot (e qualquer cliente). Só traduz HTTP/WebSocket para `servicos/`.

## Estrutura

| Caminho | O que tem |
| --- | --- |
| `app.py` | `criar_app(container)`: lifespan (grafo em `app.state.grafo`), Dishka, handlers, rotas |
| `esquemas.py` | `CriarPartida`, `PartidaResposta`, `Saude` |
| `handlers.py` | `STATUS_POR_ERRO`, `registrar_handlers` (erro de domínio → status + `ErrorResponse`) |
| `rotas/saude.py` | `GET /saude` |
| `rotas/partidas.py` | `POST /partidas`, `GET /partidas/{id}`, `/estado`, `POST /acoes`, `/pausar`, `/retomar` |
| `rotas/eventos.py` | `WS /partidas/{id}/eventos?ultimo_evento=N` |

## Regras desta pasta

- Rota fina: valida entrada, chama `ServicoDePartidas`, devolve modelo pydantic. Sem regra de jogo.
- Erro sempre como `ErrorResponse`; erro desconhecido vira 500 genérico (sem detalhe). Nova exceção => linha em `STATUS_POR_ERRO`.
- Dependência vem do Dishka (`FromDishka[...]`). Alias do tipo tem de ser atribuição comum, não `type X = ...`.
- WebSocket: partida inexistente fecha com código `4404`; reconexão com `ultimo_evento=N` recebe só `seq > N`.
- O corpo de `/estado` e dos eventos nunca expõe segredo nem a verdade do caso.
- Mudou contrato? Atualize `specs/005-api-fastapi` e o cliente em `godot/` (spec 006).
- Sem `AI_GATEWAY_API_KEY`, `POST /partidas` responde 503 `provedor_indisponivel`; `/saude` segue ok.

## Testes

`tests/api/` (`TestClient` com Dishka trocado por falsos).
