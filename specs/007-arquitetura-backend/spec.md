# 007 — Arquitetura do backend (LLM, decisão, LangGraph, API, DI)

- Status: implementada (2026-11-02); partes substituídas pela spec 008 (settings, Gateway, agente em duas etapas, grafo com `context`)
- Depende de: 001, 003, 004, 005, ADR 0007, 0008, 0009

## Problema

O domínio (specs 001–002) existe, mas não há camada de prompts, de acesso a modelos, de grafo, de API nem de injeção de dependência. Sem uma estrutura definida cada uma nasceria acoplada às outras.

## Objetivos

- Fixar a organização de pastas do pacote `chain_of_suspicion` e o sentido das dependências.
- Entregar o esqueleto funcional de cada camada, testável com falsos, sem rede.
- Mapear em enum/`Literal` modelos, provedores, nós do grafo e erros.

## Fora de escopo

- Gerador de casos (a API recebe um `ProvedorDeCaso`; o real vem em spec futura).
- Ferramentas dos agentes (a pasta `agentes/tools/` fica reservada).
- Interrogatório como subgrafo, julgamento de acusação no laço e persistência em Postgres (spec 003 e ADR 0003).
- Autenticação.

## Requisitos

- R1. Pacote único `chain_of_suspicion`; dependência só no sentido `api → servicos → agentes → infra → config/erros → domínio`. O domínio não importa nenhuma camada nova.
- R2. `ModeloLLM`, `ModeloDecisao` e `Provedor` são `StrEnum`; `PROVEDOR_DO_MODELO` e `PERFIL_POR_PAPEL` são dicionários tipados. Nós do grafo são um `Literal`.
- R3. Prompts vivem em arquivos `.md` em `prompts/`, um por papel (detetive, assassino, inocente) mais os de decisão; o carregador monta parte estável antes da variável.
- R4. `ProvedorLLM` (Protocol assíncrono) com implementação LangChain e um falso; timeout, retry (tenacity), semáforo e contagem de tokens/custo.
- R5. `Decisor` (Protocol) responde `DecisaoAmeaca` e `DecisaoContradicao` via `ModeloDecisao`; há um falso.
- R6. Grafo LangGraph com nós escolher vez → decidir → validar e aplicar → avançar tempo; ação recusada volta a `decidir` até N tentativas e depois vira `ESPERAR`; timeout do LLM vira `ESPERAR`.
- R7. Hierarquia de exceções `ErroJogo` com `ErrorCode`; todo erro chega ao cliente como `ErrorResponse`; erro inesperado nunca vaza detalhe interno.
- R8. API FastAPI com as rotas da spec 005 (R1–R7, R9, R10), contratos pydantic e `/openapi.json`.
- R9. Dishka monta o contêiner; todo teste de API troca LLM, decisor, relógio e provedor de caso por falsos.
- R10. Configuração por variáveis de ambiente (`pydantic-settings`); chave ausente deixa o provedor fora do mapa, nunca com chave vazia.
- R11. Python 3.14 (ADR 0008).

## Critérios de aceite

- [x] `pytest`, `mypy --strict` e `ruff` verdes.
- [x] Partida com agentes falsos roda pelo grafo até o orçamento de passos acabar, sem rede.
- [x] Ação inválida proposta pelo agente nunca altera o `Mundo`.
- [x] Timeout do LLM resulta em `ESPERAR`, não em exceção na partida.
- [x] `GET /saude` responde `ok`; erro de domínio vira status e `ErrorCode` corretos; erro inesperado vira 500 genérico.
- [x] Reconexão no WebSocket com `ultimo_evento=N` entrega só eventos depois de N.
- [x] Rota de estado não contém segredo nem a verdade do caso.

## Riscos e perguntas em aberto

- Como Jev e d1-ultra são acessados (API compatível com OpenAI?). Assumido `base_url` configurável; ajustar o construtor se for outro.
- Preço do Haiku 5.5, Jev e do Luna-decisions não verificado; custo deles é registrado como 0 até alguém conferir.
- Escopo de DI "por partida" fica para a spec 003; hoje serviços são singleton.
- `POST /partidas/{id}/acoes` valida e aplica a ação na hora, fora da vez do laço; o `AgenteHumano` que ocupa a vez do personagem fica para a spec 003.
- O `Decisor` existe e está no contêiner, mas nenhum nó do grafo o chama ainda (depende do subgrafo de interrogatório, spec 003).
- Custo e tokens acumulam no `ControleDeUso` do processo, não por partida; o relatório de custo ao fim da partida depende do escopo por partida.
- Posições do `Mundo` só mudam por ações; a agenda (`Presenca`) define o ponto de partida, não a posição ao longo do tempo.
- Ferramentas dos agentes e acusação (`ACUSAR` + `JuizDeterministico`) no laço não foram feitas.
