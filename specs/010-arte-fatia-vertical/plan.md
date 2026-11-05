# 010 — Plano

## Abordagem

Tudo é gerado por GDScript a partir de formas simples (caixa, cilindro, esfera), sem malhas externas. Isso cumpre a restrição de `docs/arte/direcao.md`: o assistente não esculpe, e os enums de aparência já descrevem cada personagem.

| Peça | Arquivo |
| --- | --- |
| Formas e materiais | `godot/scripts/arte/kit.gd` |
| Personagem modular | `godot/scripts/arte/personagem.gd` + `godot/personagens/*.tscn` |
| Sala | `godot/scripts/arte/biblioteca.gd` + `godot/cenas/mansao/biblioteca.tscn` |
| Traço de tinta | `godot/shaders/tinta.gdshader` |
| Quadro | `godot/scripts/quadro.gd` + `godot/shaders/cortica.gdshader` |
| Reprodutor da gravação | `godot/scripts/fatia.gd` + `godot/scenes/fatia.tscn` |
| Dados | `godot/dados/elenco.json` (gerado) e `partida_gravada.json` (à mão) |

`tools/gerar_docs.py` passa a escrever também o `elenco.json`; a função fica em `conteudo/documentacao.py`, ao lado do que já gera `docs/`.

## Dependências novas

Nenhuma de Python. Duas fontes livres em `godot/fontes/` (Special Elite e Permanent Marker, ambas Apache 2.0), porque o clima de dossiê depende de letra datilografada e de caneta.

## Testes

Godot não roda no CI, então o que dá para proteger fica em Python: `elenco.json` igual aos dados, cena de cada persona existente, e todo valor de aparência usado no elenco citado em `personagem.gd`. O visual é conferido por captura de tela.
