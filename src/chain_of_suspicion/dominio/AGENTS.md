# AGENTS.md — `dominio/`

Regras puras do jogo. Sem I/O, sem rede, sem LangChain, FastAPI ou settings. Não importa nenhuma outra pasta do pacote.

## Módulos

| Módulo | O que tem |
| --- | --- |
| `base.py` | `ModeloBase` (pydantic, `extra="forbid"`) |
| `ids.py` | `CasoId`, `PersonagemId`, `LocalId`, `PartidaId`... (`NewType` de `UUID`), `GeradorIds(seed)` |
| `enums.py` | `Papel`, `TipoAcao`, `TipoObjetivo`, `MetodoCrime`, `TipoPressao`... |
| `relogio.py` | `Relogio` (Protocol), `RelogioSimulado`, `Intervalo` |
| `calendario.py` | `Calendario`: dias do caso, períodos do dia |
| `mapa.py` | `Mapa`, `Local`, `Conexao`, menor caminho (Dijkstra) |
| `caso.py` | `Caso` e **todas** as validações de consistência |
| `mundo.py` | `Mundo`: posições e mortos em runtime |
| `acoes.py` | `Acao`, `PERMISSOES`, `validar_acao`, `aplicar_acao` |
| `regras.py` | pressão, `VisaoPersonagem`, `JuizDeterministico` |
| `eventos.py` | `EventoDePartida`, `TipoEvento`, `MotivoFim` |

## Regras desta pasta

- Um `Caso` inconsistente não pode ser construído: a regra vai em validador, não em quem usa.
- Toda regra se testa sem LLM, sem rede e sem relógio real (injete `Relogio`).
- O detetive **não tem agenda** (a validação proíbe); ele entra no mundo por `CasoPronto.entrada`.
- Mudou uma regra? Atualize `specs/001-dominio-do-caso` antes do código.

## Testes

`tests/dominio/`. O caso de referência está em `tests/caso_exemplo.py`; os casos reais estão em `conteudo/casos/`.
