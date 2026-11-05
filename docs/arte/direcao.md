# Direção de arte

> **Status: decidida em 2026-11-05**, a partir de `referencias.md`. Como produzir: `pipeline.md`. Prova do estilo: `godot/scenes/fatia.tscn` (spec 010), com imagens em `capturas/`.

## Em uma frase

Uma casa de bonecas noir vista de cima: cada sala é um corte iluminado flutuando na noite escura, cheio de objetos para olhar, e a investigação acontece num quadro de cortiça com fio vermelho.

## Decisões

| Decisão | Escolha | Por quê |
| --- | --- | --- |
| Dimensão | 3D com aparência de 2.5D | mantém a ADR 0002 e dá luz e sombra de graça |
| Câmera | ortográfica e isométrica, fixa | mostra a sala inteira, então o jogador vê quem está com quem |
| Corte | só as duas paredes do fundo; piso com laje aparente | as paredes da frente não atrapalham a visão |
| Estilo do mundo | cores chapadas e foscas, traço de tinta na pós-produção | esconde a simplicidade das formas e une tudo |
| Estilo da interface | dossiê: cortiça, polaroide, papel datilografado, caneta | onde o jogador pensa, a arte vira raciocínio |
| Fonte dos assets | formas geradas por código; fontes livres | 12 personagens saem dos enums, sem malha externa |

## Regras de cor e luz

- **Fundo:** azul-noite quase preto (`#080B16`). A sala é a única coisa acesa.
- **Luz:** abajures quentes contra janela fria. Cada sala tem uma fonte quente dominante e os cantos ficam escuros.
- **Vermelho é informação.** Fio, alfinete e carimbo usam `#B3141C`. Evite vermelho vivo na mobília, ou ele perde o sentido no quadro.
- **Roupas:** só `Paleta` (`conteudo/elenco/aparencia.py`). A cor da roupa é o que distingue uma pessoa de longe.

## Regras de forma

- A silhueta vem primeiro: chapéu, casaco e cabelo precisam ser lidos a 140 px de altura.
- Personagens têm cabeça um pouco grande, para a expressão aparecer na foto do quadro.
- Sala boa tem bagunça: papéis, livros empilhados, objetos no chão. Bagunça é onde a pista se esconde.

## Limites conhecidos

- Salas não servem para primeira pessoa (fase 3 da spec 006). Decidir antes de chegar lá.
- O traço de tinta depende do renderizador Forward+, que não exporta para web.
- Rostos são simples e não têm animação de fala. O balão é que mostra quem fala.
