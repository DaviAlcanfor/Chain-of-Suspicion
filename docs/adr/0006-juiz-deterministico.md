# 0006 — Juiz determinístico

- Status: aceita

## Contexto

Alguém precisa dizer se a acusação do detetive procede. Ideia inicial: um modelo "Deus" (Jev) olhando de cima.

## Decisão

O veredito é calculado em código (`JuizDeterministico`) a partir de `CondicaoAcerto`: culpado certo, motivo certo, provas mínimas distintas e realmente encontradas. `Juiz` é um `Protocol`, então outro juiz pode ser plugado.

Modelo de decisão pode, no máximo, avaliar justificativa em texto livre, como informação extra, sem alterar o veredito.

## Consequências

- Resultado reproduzível e sem custo.
- Acusação com justificativa criativa porém diferente da condição pré-definida não é aceita; se isso virar problema, a evolução é ampliar `CondicaoAcerto`, não entregar o veredito ao LLM.
