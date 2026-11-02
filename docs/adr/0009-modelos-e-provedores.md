# 0009 — Mapeamento de modelos e provedores

- Status: substituída pela 0010
- Complementa: 0004 (não a substitui; a escolha final do decisor continua por medição)

## Decisão

- Fala e raciocínio (`ModeloLLM`): `gpt-6-luna` (padrão) e `claude-haiku-5-5`.
- Decisão (`ModeloDecisao`): `jev`, `d1-ultra` (padrão) e `gpt-6-luna-decisions`.
- Cada modelo aponta para um `Provedor` (`openai`, `anthropic`, `typesafe`, `liquid`) em `PROVEDOR_DO_MODELO`; o construtor vem de `CONSTRUTORES`.
- Jev e d1-ultra são acessados por `base_url` configurável, assumindo API compatível com OpenAI (a confirmar).
- Provedor sem chave configurada fica fora do mapa em vez de receber chave vazia.

## Consequências

- Trocar de modelo é mudar configuração, não código do motor.
- Custos de Haiku 5.5, Jev e Luna-decisions não foram verificados e entram como zero até conferência.
