# AGENTS.md — `config/`

Settings e mapas de modelos. Um arquivo por assunto; `settings.py` só junta.

## Arquivos

| Arquivo | O que tem |
| --- | --- |
| `ambiente.py` | `Ambiente`: base `BaseSettings` (lê `.env`) |
| `api_keys.py` | `APIKeySettings`: `AI_GATEWAY_API_KEY` (única chave do projeto) |
| `llm.py` | `LLMSettings`: URL do Gateway, modelo de decisão, concorrência, retries, teto de custo |
| `jogo.py` | `GameSettings`: passos, minutos por passo, tentativas por ação, início antes do crime |
| `settings.py` | `Settings` (agrega) e o objeto `settings` |
| `modelos_llm.py` | `ModeloLLM`, `ModeloDecisao` (IDs do Gateway), `EsforcoRaciocinio` |
| `perfis.py` | `PERFIL_POR_PAPEL`: modelo, esforço e timeout por papel |
| `precos.py` | `PRECO_DO_MODELO` (US$ por milhão de tokens) |

## Regras desta pasta

- Uma chave só, do Vercel AI Gateway (ADR 0010). Nunca crie chave por provedor.
- Valor do enum de modelo é o ID exato do Gateway (`provedor/modelo`). Confira em `https://ai-gateway.vercel.sh/v1/models`.
- Segredo é `SecretStr`; nunca logue nem imprima.
- Testes não usam o `settings` global: montam `Settings` próprios (`tests/ajudas.py::settings_de_teste`).
- Preço desconhecido fica fora de `PRECO_DO_MODELO` (conta como zero); não chute.

## Testes

`tests/config/`.
