# Plano — 001 Domínio do caso

## Módulos e interfaces

| Módulo | Responsabilidade | Interface pública |
| --- | --- | --- |
| `base` | Base pydantic com `extra="forbid"` | `ModeloBase` |
| `ids` | Ids tipados e geração por seed | `GeradorIds` |
| `enums` | Vocabulário fechado do domínio | `Papel`, `TipoAcao`, ... |
| `mapa` | Grafo de locais e tempos | `Mapa.tempo_minimo`, `Mapa.vizinhos` |
| `caso` | Verdade do caso e validações | `Caso`, `Personagem`, `Presenca` |
| `mundo` | Estado de runtime | `Mundo.no_instante`, `Mundo.colocar` |
| `acoes` | Permissões e aplicação de ações | `validar_acao`, `aplicar_acao` |
| `regras` | Pressão, visão, juiz | `aplicar_pressao`, `visao_do_personagem`, `Juiz` |

## Decisões e alternativas

| Decisão | Alternativa descartada | Motivo |
| --- | --- | --- |
| Validar no construtor do `Caso` | Validar só no gerador | Impossível criar caso inválido, nem à mão |
| Juiz em código, `Juiz` como `Protocol` | Jev como juiz único | Reprodutível e barato; Jev fica para justificativas em texto livre |
| Dijkstra no `Mapa` | Distância fixa | Tempo real de deslocamento valida agenda e álibi |
| Ids por `GeradorIds(seed)` | `uuid4()` solto | Replay determinístico |

## Dependências novas

`pydantic`.

## Estratégia de teste

Tudo é teste unitário sem rede. `tests/caso_exemplo.py` é o caso de referência; `variar(**mudancas)` cria variações inválidas para provar cada recusa.
