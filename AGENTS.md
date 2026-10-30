# AGENTS.md

Instruções para qualquer agente de código (Claude Code, Codex, Cursor etc.) que trabalhe neste repositório.

## O que é o projeto

Simulação de mistério de assassinato em que **agentes de IA jogam entre si**: um assassino, um detetive, inocentes e uma vítima. Um humano poderá assumir o lugar de um agente depois, por uma porta alternativa. O backend é Python; o cliente 3D é Godot, que só mostra e comanda, sem regra de jogo.

Dono do projeto: analista de dados, forte em Python, com pouca vivência em back-end e front-end. Quando um conceito de back ou front aparecer, explique devagar e do básico, sem pular etapas. Seja realista: aponte problemas em vez de concordar com tudo.

## Fluxo obrigatório: Spec-Driven Development

Nenhuma funcionalidade nasce direto no código.

1. Leia `specs/constitution.md` (princípios que nunca mudam).
2. Ache ou crie a pasta `specs/NNN-nome/` da funcionalidade.
3. Escreva ou atualize, nesta ordem: `spec.md` (o quê e por quê), `plan.md` (como), `tasks.md` (passos pequenos e testáveis). Use os modelos em `specs/_templates/`.
4. Só depois implemente, uma tarefa por vez, começando pelo teste.
5. Se o código divergir da spec, **a spec é corrigida primeiro**, depois o código.
6. Decisão de arquitetura vira ADR em `docs/adr/`, numerada e imutável (nova decisão substitui a antiga, não a edita).

Status das specs está no topo de cada `spec.md` (`rascunho`, `aprovada`, `implementada`). Não implemente spec em `rascunho` sem pedir aprovação.

## Mapa do repositório

```
src/jogo/        domínio e motor (Python)
tests/           pytest; caso_exemplo.py é o caso de referência
specs/           constituição, modelos e uma pasta por funcionalidade
docs/adr/        decisões de arquitetura
godot/           cliente 3D (projeto Godot 4)
```

## Comandos

```
pip install -e ".[dev]" --break-system-packages
python3 -m pytest -q
python3 -m mypy
ruff check .
```

Uma tarefa só termina com os três verdes.

## Regras de código (Python)

- Python 3.13, `mypy --strict` com plugin do pydantic, `ruff` limpo.
- Nada de `str` para o que é conceito do domínio: use `StrEnum`.
- Identificadores são `NewType` sobre `UUID` (`CasoId`, `LocalId`, `PersonagemId`...). Nunca passe `UUID` cru nem `str` como id.
- Locais, objetivos e ações são **mapeados**: existem em enum ou no `Mapa`, nunca em texto livre.
- Tempo sempre com `datetime` consciente de fuso (`AwareDatetime`) e via `Relogio`/`Calendario`. Nada de `datetime.now()` solto: injete o relógio.
- Máximo de 3 argumentos por função; sem parâmetro booleano de modo (`flag`); uma responsabilidade por função.
- Sem comentários que repetem o código. Nomes bons substituem comentário. Sem código comentado, sem TODO de banner.
- Modelos pydantic herdam de `ModeloBase` (`extra="forbid"`).
- Nomes de domínio em português; nomes técnicos (`Protocol`, `Container`) como a biblioteca os chama.

## Regras de arquitetura

- **Regra é código, não prompt.** O que é permitido (quem age, onde, quando, com quem) é decidido por `validar_acao` e pelo `Caso`. O LLM só propõe; o motor valida e aplica.
- **Isolamento de contexto.** Cada agente recebe apenas a `VisaoPersonagem` dele. Nunca entregue o `Caso` inteiro a um agente.
- **Verdade única.** A agenda (`Presenca`) diz quem está onde e quando. Estado de runtime vive em `Mundo`.
- **Julgamento determinístico.** `JuizDeterministico` decide se a acusação procede. Modelo de decisão (Jev, d1-ultra) só serve para classificar e decidir antes do LLM falar, nunca para sobrescrever regra.
- **Reprodutível.** Tudo parte de uma `seed` (`GeradorIds`, sorteios). Mesma seed, mesma partida.
- **Async por padrão** em tudo que faz I/O. Chamadas de LLM com timeout, retry (tenacity), limite de concorrência e teto de custo.
- **Cliente burro.** O Godot não calcula regra; só consome eventos e envia comandos pela API.

## O que não fazer

- Não adicionar dependência sem registrar o motivo no `plan.md` da spec.
- Não editar ADR antiga; crie outra que a substitui.
- Não colocar segredo, chave de API ou `.env` no repositório.
- Não declarar tarefa pronta sem rodar os três comandos acima.
