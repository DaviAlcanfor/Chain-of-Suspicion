# Plano — 007 Arquitetura do backend

## Abordagem

Camadas finas, uma pasta por responsabilidade. LangChain só aparece em `infra/llm` e `agentes/`; o motor de regras e a API falam com Protocols. Estilo copiado do `frigus-ai`: enum + dicionário de mapeamento + construtores por provedor, prompts em `.md`, handlers centrais de exceção.

## Módulos e interfaces

| Módulo | Responsabilidade | Interface pública |
| --- | --- | --- |
| `config/settings.py` | variáveis de ambiente | `Configuracoes` |
| `config/modelos.py` | enums e mapas de modelo/provedor/perfil | `ModeloLLM`, `ModeloDecisao`, `Provedor`, `PERFIL_POR_PAPEL` |
| `erros/` | exceções e códigos | `ErroJogo` e subclasses, `ErrorCode`, `ErrorResponse` |
| `prompts/` | textos por papel e carregador | `montar_prompt(papel, visao)` |
| `infra/llm/` | provedor LangChain, fábrica, custo, falso | `ProvedorLLM`, `ProvedorLangChain`, `ProvedorFalso` |
| `infra/decisao/` | modelo de decisão | `Decisor`, `DecisorLLM`, `DecisorFalso` |
| `eventos.py` | evento imutável da partida | `EventoDePartida`, `TipoEvento` |
| `agentes/` | `Agente`, grafo, nós, estado, `tools/` reservada | `Agente`, `construir_grafo` |
| `servicos/` | casos de uso e repositório | `ServicoDePartidas`, `RepositorioPartidas` |
| `api/` | FastAPI, esquemas, handlers, rotas | `criar_app` |
| `di/` | providers Dishka | `montar_container` |

## Modelos de dados

- `PerfilLLM`: modelo, esforço de raciocínio, timeout em segundos.
- `PropostaDoAgente`: tipo, alvos opcionais e fala opcional (o `ator_id` é posto pelo motor, nunca pelo LLM).
- `EventoDePartida`: `seq`, `tipo`, `instante` (`AwareDatetime`), `ator_id`, `detalhe`.
- `EstadoPartida` (TypedDict do grafo): mundo, eventos, vez, tentativas, passos restantes.

## Decisões e alternativas

| Decisão | Alternativa descartada | Motivo |
| --- | --- | --- |
| Dishka (ADR 0007) | Wireup | escopos nativos e integração FastAPI/WebSocket |
| Python 3.14 (ADR 0008) | 3.15 | beta; `zstandard` sem wheel no Windows |
| `Literal` para nós do grafo | `StrEnum` | valores viram `str` puro no estado do LangGraph |
| Persistência em memória | Postgres | ADR 0003 fica para outra spec |

## Dependências novas

| Pacote | Motivo |
| --- | --- |
| `langgraph`, `langchain-core` | grafo (ADR 0001) |
| `langchain-openai` | GPT-6 Luna e endpoints compatíveis (Jev, d1-ultra) |
| `langchain-anthropic` | Haiku |
| `fastapi`, `uvicorn` | API |
| `dishka` | DI |
| `tenacity` | retry (constituição, princípio 6) |
| `pydantic-settings` | configuração |
| `httpx` (dev) | cliente de teste da API |

## Estratégia de teste

Tudo sem rede: `ProvedorFalso`, `DecisorFalso` e `AgenteFalso` roteirizados. Unitário para mapeamentos, prompts, handlers de erro e nós; integração do grafo e da API (`TestClient`, WebSocket incluído) com o caso de exemplo.
