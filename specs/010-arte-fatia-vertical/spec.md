# 010 — Arte: direção e fatia vertical

- Status: implementada (2026-11-05; aprovada pelo dono com as referências em `docs/arte/referencias.md`)
- Depende de: 006, 009

## Problema

A direção de arte estava pendente e o cliente Godot só mostrava um chão. Sem uma fatia jogável não dá para saber se o estilo escolhido funciona nem se dá para produzi-lo.

## Objetivos

- Fechar as decisões de `docs/arte/direcao.md`.
- Provar o estilo em uma sala, com personagens de verdade, tocando uma partida gravada.

## Fora de escopo

- As outras 23 salas.
- Ligar a fatia à API ao vivo (ver riscos).
- Período do dia na luz (R5 da spec 006) e som.

## Requisitos

- R1. Personagens são montados por código a partir de `godot/dados/elenco.json`, gerado de `conteudo/elenco/`.
- R2. Cada uma das 12 personas tem sua cena em `res://personagens/<chave>.tscn`.
- R3. A sala `res://cenas/mansao/biblioteca.tscn` mostra o que `docs/mapas.md` descreve, em corte isométrico.
- R4. A fatia toca `godot/dados/partida_gravada.json`: quem anda, fala ou encontra algo vem só de evento.
- R5. O quadro de investigação abre com Tab e só mostra o que os eventos já revelaram.
- R6. Toda fonte ou asset de terceiros tem a licença registrada em `docs/arte/pipeline.md`.

## Critérios de aceite

- [x] Rodar o projeto mostra a biblioteca, os personagens andando e os balões de fala.
- [x] O quadro abre com fotos das personas, pistas e fio vermelho (conferido por script; a tecla Tab em si não foi apertada).
- [x] `just checar` falha se `elenco.json` divergir dos dados ou se faltar cena de persona.

## Riscos e perguntas em aberto

- **A API não diz qual persona é cada personagem.** O evento traz `ator_id` (UUID) e nenhuma rota expõe a persona. A gravação usa a chave da persona no campo `ator`; a fase ao vivo vai precisar expor esse vínculo na API.
- A gravação é um roteiro escrito à mão no formato dos eventos, não a saída de uma partida real.
- Só o elenco de pé, a biblioteca e o quadro foram vistos. Oito personas nunca apareceram numa sala, sob a luz e o traço de tinta.
- Quem anda segue em linha reta e pode atravessar móveis. Personagem pequeno na tela ainda tem rosto duro, com pouco contraste.
- A fase 3 da spec 006 prevê primeira pessoa. Salas feitas para a câmera isométrica não têm detalhe nem teto para isso; decidir antes da fase 3.
- O traço de tinta usa o renderizador Forward+, que não existe na exportação para web.
