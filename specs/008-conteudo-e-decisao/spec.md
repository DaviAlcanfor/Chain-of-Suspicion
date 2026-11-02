# 008 — Conteúdo do jogo, prompts por seção e decisão por turno

- Status: implementada (2026-11-02)
- Depende de: 001, 004, 007, ADR 0010, 0011

## Problema

A spec 007 entregou a estrutura, mas não há casos jogáveis, personagens com personalidade e aparência, prompts robustos nem uso do modelo de decisão dentro do turno do agente. Também descobrimos que o Gateway da Vercel dá acesso a todos os modelos com uma chave só.

## Objetivos

- Settings organizadas (`APIKeySettings`, `LLMSettings`, `GameSettings`, objeto `settings`) com uma única chave: `AI_GATEWAY_API_KEY`.
- Cliente de decisão sobre `POST /v1/evaluate` com perguntas `boolean`, `choice` e `score`, uma por tipo de decisão.
- Turno em duas etapas: o decisor escolhe ação e alvo; o LLM só escreve a fala, e só quando a ação envolve fala.
- Prompts com seções (`PAPEL`, `OBJETIVO`, `COMO DECIDIR`, `REGRAS`, `FORMATO`) e `base.md` como contexto do caso.
- Elenco de 12 personas (personalidade, voz e aparência catalogada para o Godot), 3 mapas e 5 casos completos e documentados.
- Grafo compilado uma vez e guardado em `app.state.grafo`.

## Fora de escopo

- Subgrafo de interrogatório, acusação no laço e `AgenteHumano` (spec 003).
- Arte e cenas do Godot (só o catálogo de chaves e descrições).
- Pergunta de decisão `SUSPEITA` (nenhum nó a usa ainda).

## Requisitos

- R1. Uma única chave (`AI_GATEWAY_API_KEY`) autentica chat e decisões; IDs de modelo são os do Gateway (`provedor/modelo`).
- R2. `settings` agrega `APIKeySettings`, `LLMSettings` e `GameSettings`; testes injetam instâncias próprias.
- R3. Cada tipo de decisão é um item de `PerguntaDeDecisao`; as respostas são tipadas (`ResultadoBooleano`, `ResultadoEscolha`, `ResultadoNota`).
- R4. O custo real devolvido pelo Gateway é somado no `ControleDeUso`; o teto de custo vale também para decisões.
- R5. O decisor só escolhe entre ações viáveis; `validar_acao` continua sendo a regra. Se há uma única opção de alvo, não há chamada.
- R6. O LLM só é chamado para ações com fala; antes dela o decisor responde se o personagem deve mentir.
- R7. O prompt do sistema é montado de seções fixas; o contexto do caso traz só fatos públicos, nunca segredos.
- R8. Há 12 `Persona`s; cada uma tem personalidade, jeito de falar e `Aparencia` completa. Papel é definido pelo caso, não pela persona.
- R9. Há 3 `MapaPronto` (mansão, navio, pousada) com chave de cena do Godot por local; ids de local são determinísticos.
- R10. Há 5 `CasoPronto` válidos pelos validadores de `Caso`, cada um com apresentação pública, escalação e solução documentada em `docs/casos/`.
- R11. `CatalogoDeCasos` escolhe o caso pela seed; o detetive entra no mundo por um local de entrada do caso.
- R12. O grafo é compilado no startup (`app.state.grafo`); os agentes de cada partida entram pelo `context` do LangGraph.

## Critérios de aceite

- [x] `pytest`, `mypy --strict` e `ruff` verdes.
- [x] Todos os casos passam na validação e têm ao menos uma solução alcançável (condição de acerto cumprível).
- [x] Partida completa com os 5 casos e agentes falsos roda sem erro, inclusive com o detetive agindo.
- [x] Turno com `MOVER` não chama o LLM; turno com `CONVERSAR` chama decisor (ação, alvo, mentir) e depois o LLM.
- [x] Contexto do caso no prompt não contém segredo nem o culpado.
- [x] Docs dos casos, do elenco e dos mapas são geradas dos dados (`tools/gerar_docs.py`) e não divergem.

## Riscos e perguntas em aberto

- Qualidade do decisor em escolher ação coerente com a personalidade: medir em partida real (precisa de chave).
- Custo por turno é maior (várias chamadas pequenas); medir antes de subir `passos_por_partida`.
- Qual persona o Godot usa para cada modelo 3D: só chaves reservadas em `Aparencia.modelo_godot`.
- Nada foi testado contra o Gateway real (faltou chave): o formato de `/v1/evaluate` e do chat segue a documentação, validado só com `httpx.MockTransport`.
- As chaves das opções de `choice` são nomes em português com espaço e acento (ex.: "Sala de Jantar"); a doc mostra identificadores simples. Se o Gateway rejeitar, mapear para códigos.
- Os agentes ainda não encontram pistas: `ContextoDoTurno.pistas` é vazio e o `Mundo` não guarda pistas descobertas. `EXAMINAR_LOCAL` é um evento sem efeito e `ESCONDER_EVIDENCIA`/`APRESENTAR_PROVA` nunca são oferecidas. Resolver na spec 003, junto de `ACUSAR` (excluída do laço).
- As perguntas `AMEACA` e `CONTRADICAO` existem no decisor, mas nenhum nó as chama (dependem do interrogatório, spec 003).
- Custo e tokens continuam acumulando por processo, não por partida.
- `modelo_godot` e `cena_godot` são nomes reservados; não há arte nem cenas ainda.
