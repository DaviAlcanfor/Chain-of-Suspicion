# AGENTS.md — `docs/`

Documentação do projeto. Parte é escrita à mão (ADRs, catálogo) e parte é **gerada**.

## Estrutura

| Caminho | Origem |
| --- | --- |
| `CATALOGO.md` | à mão: índice de pastas, `AGENTS.md` e quando ler cada um |
| `adr/NNNN-*.md` | à mão: decisões de arquitetura, numeradas e imutáveis |
| `elenco.md`, `mapas.md`, `casos/*.md` | **gerados** por `python tools/gerar_docs.py` |
| `arte/direcao.md` | à mão: direção de arte (decisões ainda pendentes) |

## Regras desta pasta

- Não edite à mão os arquivos gerados: mude `conteudo/` e rode o gerador. Um teste falha se divergirem.
- `casos/*.md` têm **spoilers** (a solução fica no fim). Não os cole em prompts de agentes de jogo.
- ADR nunca é editada: uma nova decisão cria outra ADR que a substitui e marca a antiga como substituída.
- ADR tem: status, contexto, decisão, consequências. Cite fontes e a data de verificação quando houver fato externo.
- Pasta nova com contexto próprio => `AGENTS.md`, `CLAUDE.md` irmão e linha em `CATALOGO.md`.
- Escreva em português, com frases curtas; explique conceitos de back e front devagar.
