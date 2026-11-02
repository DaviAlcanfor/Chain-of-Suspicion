# Catálogo do projeto

Índice para decidir **o que ler** antes de mexer. O projeto é grande: cada pasta tem um `AGENTS.md` curto (até 60 linhas) e um `CLAUDE.md` irmão com `@AGENTS.md`. Leia o da raiz, ache a pasta aqui e leia só o dela.

## Contextos por pasta

| Pasta | Contexto | O que há dentro | Leia quando |
| --- | --- | --- | --- |
| raiz | [AGENTS.md](../AGENTS.md) | projeto, fluxo SDD, comandos | sempre |
| `src/chain_of_suspicion/` | [AGENTS.md](../src/chain_of_suspicion/AGENTS.md) | camadas, regras de código e de arquitetura | vai escrever Python |
| `src/chain_of_suspicion/dominio/` | [AGENTS.md](../src/chain_of_suspicion/dominio/AGENTS.md) | `Caso`, `Mundo`, ações, regras, eventos, ids, relógio, mapa | mexer em regra do jogo |
| `src/chain_of_suspicion/config/` | [AGENTS.md](../src/chain_of_suspicion/config/AGENTS.md) | settings (chave, LLM, jogo), modelos, perfis, preços | mudar modelo, limite ou variável de ambiente |
| `src/chain_of_suspicion/erros/` | [AGENTS.md](../src/chain_of_suspicion/erros/AGENTS.md) | `ErroJogo`, `ErrorCode`, `ErrorResponse` | criar ou traduzir erro |
| `src/chain_of_suspicion/conteudo/` | [AGENTS.md](../src/chain_of_suspicion/conteudo/AGENTS.md) | 12 personas, 3 mapas, 5 casos, gerador de docs | criar caso, persona, mapa ou aparência |
| `src/chain_of_suspicion/prompts/` | [AGENTS.md](../src/chain_of_suspicion/prompts/AGENTS.md) | `.md` de contexto, papéis e decisões, carregador | editar o que o modelo lê |
| `src/chain_of_suspicion/infra/` | [AGENTS.md](../src/chain_of_suspicion/infra/AGENTS.md) | cliente de chat e de decisão (Gateway), custo | tocar em chamada a modelo |
| `src/chain_of_suspicion/agentes/` | [AGENTS.md](../src/chain_of_suspicion/agentes/AGENTS.md) | grafo LangGraph, nós, agentes, tools de decisão | mexer no laço da partida |
| `src/chain_of_suspicion/servicos/` | [AGENTS.md](../src/chain_of_suspicion/servicos/AGENTS.md) | montar, rodar, pausar partidas | mudar ciclo de vida da partida |
| `src/chain_of_suspicion/api/` | [AGENTS.md](../src/chain_of_suspicion/api/AGENTS.md) | rotas HTTP/WebSocket, esquemas, erros HTTP | criar ou mudar endpoint |
| `src/chain_of_suspicion/di/` | [AGENTS.md](../src/chain_of_suspicion/di/AGENTS.md) | providers do Dishka | ligar dependência nova |
| `tests/` | [AGENTS.md](../tests/AGENTS.md) | subpastas espelhadas, helpers, falsos | escrever ou rodar testes |
| `specs/` | [AGENTS.md](../specs/AGENTS.md) | constituição, modelos e specs 001–009 | começar funcionalidade |
| `docs/` | [AGENTS.md](../docs/AGENTS.md) | ADRs, docs geradas, este catálogo | escrever ADR ou doc |
| `godot/` | [AGENTS.md](../godot/AGENTS.md) | cliente 3D e contratos que ele consome | trabalhar no cliente |

## Onde fica...

| Quero... | Vá para |
| --- | --- |
| adicionar um caso | `conteudo/casos/` (depois `python tools/gerar_docs.py`) |
| mudar a aparência de um personagem | `conteudo/elenco/catalogo.py` e enums em `elenco/aparencia.py` |
| mudar o que o assassino "pensa" | `prompts/papeis/assassino.md` |
| trocar o modelo de decisão | `config/llm.py` (`modelo_decisao`) e `config/modelos_llm.py` |
| criar uma pergunta de decisão | `infra/decisao/` + `agentes/tools/decisao.py` |
| criar um erro novo | `erros/excecoes.py`, `erros/codigos.py`, `api/handlers.py` |
| criar um endpoint | `api/rotas/` + `servicos/` (+ spec 005) |
| entender por que uma decisão foi tomada | `docs/adr/` |
| ver as decisões de arte (pendentes) | `docs/arte/direcao.md` |
| ver a solução de um caso (spoiler) | `docs/casos/` |

## Specs e ADRs (leia só as citadas pela tarefa)

| Spec | Assunto |
| --- | --- |
| 001, 002 | domínio do caso, calendário |
| 003 | motor de simulação (parcial: interrogatório, acusação, humano) |
| 004, 005, 006 | camada de LLM, API, cliente Godot |
| 007 | arquitetura do backend |
| 008 | conteúdo e decisão por turno |
| 009 | reorganização e contexto por pasta |

ADRs vigentes: 0001 (LangGraph), 0002 (Godot), 0003 (Postgres, adiada), 0004 (modelos), 0006 (juiz), 0007 (Dishka), 0008 (Python 3.14), 0010 (Gateway), 0011 (decisor escolhe), 0012 (contexto por pasta), 0013 (ferramentas). Substituídas: 0005 (por 0007), 0009 (por 0010).

## Regra de manutenção

Pasta nova com contexto próprio: crie `AGENTS.md` (até 60 linhas), `CLAUDE.md` com `@AGENTS.md` e uma linha na tabela acima. `tests/contexto/` falha se algo estiver fora de sincronia.
