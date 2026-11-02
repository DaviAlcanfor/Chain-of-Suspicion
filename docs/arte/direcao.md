# Direção de arte

> **Status: pendente.** As decisões abaixo ainda não foram tomadas pelo dono do projeto. Nenhuma arte, cena ou modelo deve ser produzido antes delas. Este arquivo é onde a direção final vai ser escrita.

## Decisões em aberto

| Decisão | Opções | Observação |
| --- | --- | --- |
| Dimensão | 2D, 3D ou 2.5D | 3D pede mais assets; 2D/2.5D reduz o volume de modelagem |
| Estilo | low-poly, estilizado com cores chapadas, pintado à mão | escolher pelo que dá para produzir (ver restrições) |
| Câmera | fixa por cômodo (estilo *Clue*), isométrica, terceira pessoa | afeta quanto cada local precisa ser modelado |
| Fonte dos assets | pacotes livres (Kenney, Quaternius), geração 3D por IA, modelagem própria | licença de cada asset precisa ser registrada |
| Onde guardar referências | links e miniaturas em `docs/arte/referencias.md`; arquivos grandes fora do Git (ou Git LFS) | a criar quando a direção for definida |

## O que já está fixado pelo código

- **12 personas** com aparência em enums: porte, pele, cabelo (cor e estilo), pelos faciais, peça de roupa, cor da roupa (`Paleta`), acessórios. Ver `docs/elenco.md`.
- **3 mapas** de 8 locais cada (24 locais), com a cena esperada em `res://cenas/<mapa>/<local>.tscn`. Ver `docs/mapas.md`.
- Modelo de cada persona esperado em `res://personagens/<chave>.tscn`.
- O cliente Godot não decide regra: só mostra eventos e envia comandos (constituição, princípio 7).

## Restrições para decidir bem

- Modelar à mão 12 personagens e 24 locais é muito trabalho. Como a aparência já é dado (enums), um **personagem modular** montado por código (corpo por porte, cabelo, roupa e acessórios como peças) evita 12 modelos separados.
- O assistente de código escreve GDScript, cenas `.tscn`, shaders, UI e formas simples. Ele **não esculpe nem pinta texturas**: malhas novas vêm de pacotes de assets, de ferramenta de geração 3D ou do dono do projeto.
- A paleta oficial é o enum `Paleta` (`conteudo/elenco/aparencia.py`); cor nova entra lá, com hex.

## Para destravar

1. Escolher dimensão, estilo e câmera.
2. Reunir referências (links com uma frase sobre o que cada uma ensina).
3. Reescrever este arquivo com a direção decidida e criar `docs/arte/referencias.md` e `docs/arte/pipeline.md`.
4. Só então atualizar a spec 006 (cliente Godot) e começar a fatia vertical: uma sala, duas personas, uma partida gravada.
