# Cliente Godot

Esqueleto da fase 0 da spec 006. Não contém regra de jogo; só mostra o que a API manda.

## Como abrir

1. Instale o Godot 4 (versão estável 4.4 ou mais nova).
2. No gerenciador de projetos: Importar → escolha `godot/project.godot`.
3. Aperte F5. A cena abre uma janela com um chão e uma câmera e imprime no painel de saída o que a API respondeu.

Sem API no ar, aparece um aviso de falha de conexão. É esperado. Para ver a resposta funcionando antes de existir backend de verdade:

```
python3 tools/saude_falsa.py
```

e rode o projeto de novo.

## Quatro conceitos do Godot

- **Nó (Node)**: peça básica. Uma câmera é um nó, uma luz é um nó, um personagem é um nó.
- **Cena (.tscn)**: uma árvore de nós salva em arquivo. `scenes/main.tscn` é a cena inicial.
- **Script (.gd)**: código em GDScript (parecido com Python) preso a um nó. `scripts/main.gd` monta a câmera, a luz e o chão ao iniciar.
- **Sinal (signal)**: aviso que um nó emite e outro escuta. `EventStream` emite `evento_recebido` e `main.gd` reage a ele.

## Arquivos

| Arquivo | Papel |
| --- | --- |
| `config.cfg` | URL da API e id da partida a acompanhar |
| `scripts/api_client.gd` | Chamadas HTTP (`obter`, `enviar`) |
| `scripts/event_stream.gd` | WebSocket de eventos, com reconexão que retoma pelo último evento |
| `scripts/main.gd` | Liga tudo e monta a cena 3D mínima |

## Próximos passos (spec 006)

Fase 1: uma sala por local do mapa e uma cápsula por personagem que muda de sala quando chega um evento de movimento.
