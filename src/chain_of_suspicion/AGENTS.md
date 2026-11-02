# AGENTS.md — pacote `chain_of_suspicion`

Regras de código e de arquitetura válidas para **todas** as pastas de `src/chain_of_suspicion/`. Cada pasta tem o seu próprio `AGENTS.md` com o que é específico dela.

## Camadas e sentido das dependências

```text
api → servicos → agentes → infra / prompts / conteudo → config / erros → dominio
                di (monta tudo)        main.py (entrada)
```

Uma camada só importa as que estão à direita. `dominio/` não importa nenhuma outra.

## Regras de código (Python 3.14)

- `mypy --strict` com plugin do pydantic e `ruff` limpo.
- Nada de `str` para conceito do domínio: use `StrEnum`. Ids são `NewType` sobre `UUID`.
- Locais, objetivos e ações são **mapeados** (enum ou `Mapa`), nunca texto livre.
- Tempo sempre `AwareDatetime`, via `Relogio`/`Calendario`; nada de `datetime.now()` solto.
- Máximo de 3 argumentos por função e por construtor; sem parâmetro booleano de modo.
- Sem comentário que repete o código, sem código comentado, sem TODO de banner.
- Modelos pydantic herdam de `ModeloBase` (`extra="forbid"`); payload externo usa `BaseModel` com `extra="ignore"`.
- Nomes de domínio em português; nomes técnicos como a biblioteca os chama.
- Alias `type X = Annotated[...]` quebra o Dishka e o FastAPI: use atribuição comum.

## Regras de arquitetura

- **Regra é código, não prompt.** `validar_acao` e `Caso` decidem o que vale; o LLM só propõe.
- **Isolamento de contexto.** Cada agente recebe só a `VisaoPersonagem` dele.
- **Decisor escolhe, LLM fala** (ADR 0011). O decisor nunca sobrescreve regra.
- **Reprodutível.** Mesma seed, mesma partida; ids de conteúdo são `uuid5` determinísticos.
- **Async por padrão** em I/O; chamadas externas com timeout, retry, limite de concorrência e teto de custo.
- **Cliente burro.** O Godot só consome eventos e envia comandos pela API.
- Erros de domínio são `ErroJogo` (sem HTTP); só `api/handlers.py` os traduz para status.
- Dependências entram pelo contêiner Dishka (`di/`); nada de singleton global além de `settings`.

## Onde testar

Os testes espelham as pastas em `tests/<pasta>/`. LLM e rede sempre atrás de falsos (`ProvedorFalso`, `ClienteFalso`, `DecisorFalso`, `AgenteFalso`).
