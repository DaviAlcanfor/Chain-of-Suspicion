# Constituição do projeto

Princípios que valem para toda spec. Mudar um deles exige uma ADR.

1. **Regra no código.** Prompt nunca é a única barreira para uma regra de jogo. Se uma regra pode ser violada por um LLM desobediente, ela precisa de validação em código.
2. **O caso é a verdade.** Todo caso é gerado e validado antes de a partida começar. Um caso inconsistente (alguém em dois lugares, álibi sem desmentido, pista inalcançável) não deve nem ser criado.
3. **Cada agente sabe só o que sabe.** Contexto isolado por personagem. Vazamento de informação é bug.
4. **Determinismo primeiro.** Mesma seed e mesmas respostas de LLM geram a mesma partida. Respostas de LLM são gravadas no log da partida para reprodução.
5. **Sem rodar partida inteira para testar regra.** Regras se testam sem LLM. LLM entra atrás de uma interface (`Protocol`) com versão falsa para teste.
6. **Custo e tempo têm teto.** Toda chamada externa tem timeout, retry limitado, limite de concorrência e contagem de custo por partida.
7. **Cliente é só vitrine.** Godot ou qualquer outro cliente exibe eventos e envia comandos. Não decide nada.
8. **Humano é uma porta, não um caso especial.** Um humano ocupa o lugar de um agente usando o mesmo caminho de ação (`Acao` → `validar_acao`).
9. **Código limpo é requisito.** Tipos estritos, enums, ids tipados, funções pequenas, sem comentário redundante.
10. **Spec antes de código.** Ver `AGENTS.md`.

## Definição de pronto de uma tarefa

- Teste escrito antes ou junto, cobrindo o caminho feliz e as falhas previstas na spec.
- `pytest`, `mypy` e `ruff` verdes.
- Spec e ADR atualizadas se algo mudou.
