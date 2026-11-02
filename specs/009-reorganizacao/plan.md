# Plano — 009 Reorganização

## Abordagem

Mudança mecânica por etapas, com a suíte rodando ao fim de cada uma: mover com `git mv` e reescrever imports por script; dividir settings; trocar strings de aparência por enums; criar as tools; escrever os `AGENTS.md`.

## Módulos e interfaces

| Módulo | Responsabilidade | Interface pública |
| --- | --- | --- |
| `dominio/` | regras puras | os mesmos nomes de antes, sob `chain_of_suspicion.dominio.*` |
| `config/api_keys.py`, `llm.py`, `jogo.py` | um grupo de settings cada | `APIKeySettings`, `LLMSettings`, `GameSettings` |
| `config/settings.py` | agrega | `Settings`, `settings` |
| `config/modelos_llm.py`, `perfis.py`, `precos.py` | enums, perfis por papel, preços | `ModeloLLM`, `ModeloDecisao`, `PERFIL_POR_PAPEL`, `PRECO_DO_MODELO` |
| `conteudo/elenco/aparencia.py` | enums e `Aparencia` | `CorDeCabelo`, `Paleta`, `HEX_DA_COR`, `Aparencia` |
| `agentes/tools/decisao.py` | tools de decisão | `criar_ferramentas(decisor)`, `ESQUEMA_DOS_ARGUMENTOS` |
| `AGENTS.md` por pasta, `docs/CATALOGO.md` | contexto por pasta | — |

## Modelos de dados

- `Aparencia`: idade, altura_cm, porte, cabelo (`CorDeCabelo`, `EstiloDeCabelo`), pele (`TomDePele`), roupa (`PecaDeRoupa` + `Paleta`), acessorios (`list[Acessorio]`), cor_principal (`Paleta`), nota_de_arte.

## Decisões e alternativas

| Decisão | Alternativa descartada | Motivo |
| --- | --- | --- |
| Pasta `dominio/` | `nucleo/`, `core/` | nome do conceito, em português |
| `turno.py` em `agentes/` | em `dominio/` | é contrato agente↔motor, não regra |
| Uma tool por pergunta | uma por tipo (boolean/choice/score) | cada pergunta tem argumentos e retorno próprios |
| `CLAUDE.md` com `@AGENTS.md` por pasta | só `AGENTS.md` | o Claude Code só lê contexto aninhado via `CLAUDE.md` |

## Dependências novas

Nenhuma.

## Estratégia de teste

Os testes existentes continuam valendo (só imports mudam). Novos: tools (resultado igual ao do decisor, schema validado), aparência (todo valor é enum, hex válido para cada cor), contexto (catálogo e `AGENTS.md` consistentes).
