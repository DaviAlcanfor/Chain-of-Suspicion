# AGENTS.md — `infra/`

Acesso a modelos de fora: chat (LangChain) e decisão (HTTP). Tudo passa pelo Vercel AI Gateway com uma chave só.

## Estrutura

| Caminho | O que tem |
| --- | --- |
| `llm/contrato.py` | `ProvedorLLM` (Protocol), `Mensagem`, `RespostaLLM` |
| `llm/langchain.py` | `ProvedorLangChain`: timeout, retry (tenacity), saída estruturada, custo |
| `llm/fabrica.py` | `construir_chat`: `ChatOpenAI` apontado para o Gateway |
| `llm/catalogo.py` | `CatalogoLLM`: provedor por papel (cache) |
| `llm/controle.py` | `ControleDeUso`: semáforo, tokens, custo, teto |
| `llm/falso.py` | `ProvedorFalso` (roteirizado) |
| `decisao/perguntas.py` | `PerguntaDeDecisao`, `Pergunta`, `Resultado*` |
| `decisao/cliente.py` | `ClienteDeDecisao`, `ClienteHttp` (`POST /v1/evaluate`), `ClienteFalso` |
| `decisao/decisor.py` | `Decisor`, `DecisorGateway`, `DecisorFalso` |

## Regras desta pasta

- Todo I/O é `async`, com timeout, retry limitado, semáforo e custo registrado em `ControleDeUso`.
- `FalhaNoLLM`/`TempoEsgotadoNoLLM` saem daqui; quem chama decide o que fazer (o grafo vira `ESPERAR`).
- Resposta fora do formato é `FalhaNoLLM`, nunca valor inventado. Escolha fora das opções também.
- Pergunta nova de decisão: item em `PerguntaDeDecisao` + tipo e instrução + método no `Decisor` + tool em `agentes/tools/decisao.py`.
- Nenhum código fora daqui importa SDK de fornecedor (`langchain_openai`, `httpx`).
- Nunca teste contra a rede: `httpx.MockTransport`, `ProvedorFalso`, `ClienteFalso`.

## Testes

`tests/infra/`.
