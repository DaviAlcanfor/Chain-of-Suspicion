# AGENTS.md — `conteudo/`

O conteúdo jogável: elenco, mapas e casos. É dado, não lógica. Depende de `dominio/` e `config/` só para tipos.

## Estrutura

| Caminho | O que tem |
| --- | --- |
| `elenco/aparencia.py` | enums de aparência (`TomDePele`, `CorDeCabelo`, `EstiloDeCabelo`, `PecaDeRoupa`, `Acessorio`, `Paleta`), `HEX_DA_COR`, `Aparencia` |
| `elenco/personas.py` | `ChavePersona`, `Traco`, `Persona` (personalidade, voz, manias) |
| `elenco/catalogo.py` | `ELENCO`: as 12 personas |
| `mapas.py` | `MapaPronto`: 3 mapas de 8 locais; `id_do_local` é `uuid5` |
| `caso_pronto.py` | `CasoPronto` = `Caso` + apresentação pública + solução + escalação + entrada do detetive |
| `casos/construtor.py` | `Ids` (uuid5), `hora`, `periodo`, `ator`, `estadia` |
| `casos/<caso>.py` | um módulo por caso; `casos/__init__.py` monta `CATALOGO` |
| `documentacao.py` | gera `docs/elenco.md`, `docs/mapas.md`, `docs/casos/*` |

## Regras desta pasta

- Papel (assassino, detetive...) é do **caso**; a persona é a mesma em todos. A `funcao` da escalação adapta a profissão ao cenário.
- Aparência é enum: não crie string solta de cor, cabelo ou roupa. Cor nova => item em `Paleta` + hex em `HEX_DA_COR`.
- Texto livre só onde o LLM lê: `personalidade`, `jeito_de_falar`, `manias`, `apresentacao`.
- `apresentacao` é pública: nunca cite segredo, culpado ou método escondido.
- Toda agenda começa em `crime.instante - 40 min` (`GameSettings.minutos_antes_do_crime`); senão o personagem não entra no mundo.
- Ids por `uuid5` (determinísticos): mesma chave, mesmo id, em qualquer máquina.
- Caso novo: módulo em `casos/`, entrada em `ChaveCaso` e em `CATALOGO`, depois `python tools/gerar_docs.py`.
- O `Caso` valida sozinho: rode o módulo e leia o erro (álibi falso exige fato que o desminta, pista alcançável, etc.).

## Testes

`tests/conteudo/` (inclui o teste que compara `docs/` com os dados).
