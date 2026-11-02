# Plano — 008 Conteúdo do jogo e decisão por turno

## Abordagem

Cinco blocos independentes: settings e Gateway, cliente de decisão, conteúdo (personas, mapas, casos), prompts por seção e turno em duas etapas. O domínio (`Caso`, `Mundo`) não muda; o conteúdo é montado em cima dele.

## Módulos e interfaces

| Módulo | Responsabilidade | Interface pública |
| --- | --- | --- |
| `config/settings.py` | settings agrupadas | `APIKeySettings`, `LLMSettings`, `GameSettings`, `settings` |
| `config/modelos.py` | IDs do Gateway e perfis | `ModeloLLM`, `ModeloDecisao`, `PERFIL_POR_PAPEL` |
| `infra/decisao/perguntas.py` | tipos de pergunta e resultados | `PerguntaDeDecisao`, `ResultadoBooleano/Escolha/Nota` |
| `infra/decisao/cliente.py` | HTTP para `/v1/evaluate` | `ClienteDeDecisao`, `ClienteHttp`, `ClienteFalso` |
| `infra/decisao/decisor.py` | decisões do jogo | `Decisor`, `DecisorGateway`, `DecisorFalso` |
| `conteudo/personas.py`, `elenco.py` | personas e aparência | `Persona`, `Aparencia`, `ELENCO` |
| `conteudo/mapas.py` | mapas com cenas | `MapaPronto`, `MAPAS` |
| `conteudo/casos/` | 5 casos + construtor de ids | `CasoPronto`, `CATALOGO` |
| `prompts/` | seções por papel + base | `montar_sistema`, `descrever_turno` |
| `agentes/agente.py` | turno em duas etapas | `AgenteEmDuasEtapas` |
| `servicos/casos.py` | escolha do caso pela seed | `CatalogoDeCasos` |

## Modelos de dados

- `Aparencia`: idade, altura_cm, `Porte`, cabelo, roupa, acessorios, cor_principal (hex), modelo_godot.
- `Persona`: chave (`ChavePersona`), nome, profissao, personalidade (`Traco`s), jeito_de_falar, manias, aparencia.
- `CasoPronto`: chave, titulo, mapa, apresentacao, solucao (só docs), entrada_do_detetive, escalacao, caso.
- `ContextoDaPartida` (context do LangGraph): agentes e limites.

## Decisões e alternativas

| Decisão | Alternativa descartada | Motivo |
| --- | --- | --- |
| Chave única do Gateway (ADR 0010) | Chave por provedor | Uma credencial, uma conta de custo |
| Decisor escolhe, LLM fala (ADR 0011) | LLM escolhe a ação | Barato, rápido e a regra continua no código |
| Casos como módulos Python | JSON/YAML | Reuso de ids e validação por tipo |
| Docs geradas dos dados | Docs escritas à mão | Não divergem |
| `httpx` direto para decisões | LangChain | A API de decisão não é de chat |

## Dependências novas

`httpx` passa de dev para runtime (cliente do Gateway). `langchain-anthropic` sai (todos os modelos de chat passam pelo endpoint OpenAI-compatível do Gateway).

## Estratégia de teste

Cliente de decisão testado com `httpx.MockTransport`; decisor e agente com `ClienteFalso`; casos por teste paramétrico (validação, solução alcançável, partida com agentes falsos); prompts por inspeção de seções e ausência de segredos.
