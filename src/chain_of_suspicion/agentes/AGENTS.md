# AGENTS.md — `agentes/`

O laço da partida (LangGraph) e os agentes que decidem dentro dele.

## Estrutura

| Caminho | O que tem |
| --- | --- |
| `turno.py` | `ContextoDoTurno`, `PropostaDoAgente`, `DecisaoDoTurno`, `FalaGerada`, `montar_acao` |
| `agente.py` | `Agente` (Protocol), `AgenteEmDuasEtapas`, `AgenteFalso` |
| `fabrica.py` | `FabricaDeAgentes` / `FabricaDeAgentesLLM`: um agente por personagem que age |
| `contexto.py` | `montar_contexto(mundo, ator)`: quem está aqui, saídas, ações permitidas |
| `estado.py` | `EstadoPartida`, `ContextoDaPartida`, `LimitesDaPartida`, `NomeNo` |
| `emissor.py` | `emitir`: cria `EventoDePartida` numerados |
| `grafo.py` | `construir_grafo()`, `executar()` (stream de eventos) |
| `nos/rodada.py`, `nos/acao.py` | nós: iniciar rodada, escolher vez, decidir, aplicar, avançar tempo |
| `tools/decisao.py` | uma `StructuredTool` por `PerguntaDeDecisao` |

## Fluxo do turno

escolher vez → decidir (decisor escolhe ação e alvo; LLM fala se a ação tem fala) → `validar_acao` → aplica ou recusa (volta com o motivo; passou do limite vira `ESPERAR`) → avançar tempo.

## Regras desta pasta

- O grafo é compilado **uma vez** (`app.state.grafo`); agentes e limites entram por `context=`, nunca por closure.
- Nós são funções puras sobre `EstadoPartida`; o `Mundo` é mutado só por `aplicar_acao`.
- `ACUSAR` está fora do laço até a spec 003; `ContextoDoTurno.pistas` é vazio (limite conhecido).
- Cada agente vê só a `VisaoPersonagem` dele; o contexto do caso no prompt é público.
- Tools de decisão existem e são testadas, mas o fluxo chama o decisor direto (ADR 0011).
- O mypy não aceita `add_node` do LangGraph: o `type: ignore` mora só em `grafo.py::_adicionar_no`.

## Testes

`tests/agentes/` (inclui uma partida completa em cada um dos 5 casos).
