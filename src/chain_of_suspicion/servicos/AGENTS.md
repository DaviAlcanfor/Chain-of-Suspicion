# AGENTS.md — `servicos/`

Casos de uso: montar, rodar e controlar partidas. Não conhece HTTP.

## Arquivos

| Arquivo | O que tem |
| --- | --- |
| `casos.py` | `ProvedorDeCaso` (Protocol), `CatalogoDeCasos` (caso pela seed: `seed % 5`) |
| `montador.py` | `MontadorDePartida`: caso → `Mundo` + detetive na entrada + agentes + limites |
| `partida.py` | `Partida`, `StatusPartida`, `EstadoVisivel`, `estado_visivel` |
| `repositorio.py` | `RepositorioPartidas` (Protocol), `RepositorioEmMemoria` |
| `partidas.py` | `ServicoDePartidas`: criar, obter, pausar, retomar, agir, eventos |

## Regras desta pasta

- A partida roda em `asyncio.Task` em segundo plano; a requisição nunca espera o fim.
- `Partida.publicar` renumera `seq`: é a única fonte de numeração dos eventos (o grafo só sugere).
- `EstadoVisivel` é o que o cliente pode ver: nunca fatos, culpado, método ou segredos. Um teste confere.
- `agir` (ação humana) valida e aplica na hora; o `AgenteHumano` na vez do personagem é da spec 003.
- Erro inesperado no laço encerra com `MotivoFim.ERRO_INTERNO` e evento final; nunca deixa a task morrer calada.
- Persistência é em memória (ADR 0003 adiada); trocar exige só outra implementação do Protocol.

## Testes

`tests/servicos/`.
