# AGENTS.md — `tests/`

Testes com pytest. As subpastas espelham as pastas de `src/chain_of_suspicion/`.

## Estrutura

| Caminho | Cobre |
| --- | --- |
| `dominio/`, `config/`, `conteudo/`, `prompts/`, `infra/`, `agentes/`, `servicos/`, `api/` | a pasta de mesmo nome |
| `contexto/` | consistência de `AGENTS.md`, `CLAUDE.md` e `docs/CATALOGO.md` |
| `ajudas.py` | `settings_de_teste`, `pessoa`, `FabricaFalsa`, `VENENO` (caso 1 real) |
| `caso_exemplo.py` | caso de referência do domínio (mapa próprio, não é um `CasoPronto`) |

`pythonpath` do pytest inclui `src` e `tests`: `from ajudas import ...` funciona de qualquer subpasta. Nomes de arquivo de teste são únicos no repositório.

## Regras desta pasta

- Escreva o teste antes ou junto; cubra o caminho feliz e as falhas previstas na spec.
- Nenhum teste usa rede, relógio real nem `settings` global. LLM sempre atrás de falsos.
- Teste de API usa `TestClient` com `@provide(override=True)` no Dishka.
- Para saber se uma regra está protegida, tire-a: o teste deve falhar (teste de mutação manual).
- `asyncio_mode = "auto"`: funções `async def test_...` rodam sem decorador.
- Teste lento (> 1 s) é suspeito: procure `sleep` ou espera real.

## Comando

`just testar tests/<pasta>` (ou `uv run pytest -q tests/<pasta>`)
