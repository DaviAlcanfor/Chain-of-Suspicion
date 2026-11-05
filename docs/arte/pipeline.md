# Como produzir a arte

Não há modelo 3D nem textura pintada. Tudo é montado por GDScript com formas simples, e isso é um limite escolhido: troca detalhe por volume e consistência.

## Personagem

1. A aparência é dado: mude em `conteudo/elenco/catalogo.py`.
2. Rode `just docs`. Ele regenera `docs/` e `godot/dados/elenco.json`.
3. `godot/scripts/arte/personagem.gd` lê o JSON e monta o corpo. Valor novo de enum precisa de peça nesse script; um teste avisa se faltar.

## Sala nova

1. Crie `godot/scripts/arte/<local>.gd` usando as funções de `kit.gd`, com `biblioteca.gd` como modelo.
2. Crie a cena `godot/cenas/<mapa>/<local>.tscn` com esse script no nó raiz. O caminho vem de `docs/mapas.md`.
3. Marque os lugares onde as pessoas ficam como nós `Marker3D`, filhos de um nó chamado `pontos`. As pessoas andam em linha reta entre eles, então escolha pontos sem móvel no caminho.

A biblioteca levou cerca de 300 linhas. Móveis repetidos devem ir para `kit.gd` quando a segunda sala precisar deles.

## Conferir

Abra a cena no editor do Godot e aperte F6. Ajuste luz e cor olhando o resultado, porque número nenhum substitui isso.

## Licenças de terceiros

| Asset | Origem | Licença |
| --- | --- | --- |
| Special Elite (`godot/fontes/`) | Google Fonts, Astigmatic | Apache 2.0 |
| Permanent Marker (`godot/fontes/`) | Google Fonts, Font Diner | Apache 2.0 |

Asset novo de terceiros entra nesta tabela no mesmo commit.
