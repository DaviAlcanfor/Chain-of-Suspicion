# AGENTS.md — `prompts/`

Textos que vão para os modelos. Markdown com seções fixas, carregado por `carregador.py`.

## Arquivos

| Arquivo | Uso |
| --- | --- |
| `base.md` | contexto do caso (cenário, o que aconteceu, elenco) — parte estável do prompt |
| `papeis/comum.md` | `## REGRAS` e `## FORMATO` de todos os papéis |
| `papeis/<papel>.md` | `## PAPEL`, `## OBJETIVO`, `## COMO DECIDIR`, `## REGRAS` de cada papel |
| `decisao/*.md` | modelos de estado das perguntas de decisão (`{campos}` do `str.format`) |
| `carregador.py` | `montar_sistema`, `descrever_turno`, `pedido_de_fala`, `prompt_ameaca`... |
| `descricoes.py` | `DESCRICAO_DA_ACAO` e `ACOES_COM_FALA` |

## Ordem do prompt de sistema

contexto do caso → `# VOCÊ` (nome, função, ficha da persona) → PAPEL → OBJETIVO → COMO DECIDIR → REGRAS → FORMATO. A parte estável vem antes da variável (prompt caching).

## Regras desta pasta

- O prompt nunca é a única barreira de uma regra de jogo (constituição, princípio 1).
- O contexto do caso é público: nada de segredo, culpado ou fato do caso. Um teste confere.
- Todo `.md` começa com um título `#` e usa `##` para as seções que o carregador lê.
- Não use `{` `}` literais em templates de `decisao/` (`str.format`).
- O LLM só dá voz: fala curta (1 a 3 frases), em primeira pessoa, sem citar "jogo", "IA" ou "ação".
- Mudou o nome de uma seção? Atualize `carregador.py` e `tests/prompts/`.

## Testes

`tests/prompts/`.
