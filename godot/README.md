# Cliente Godot

Não contém regra de jogo; só mostra o que recebe. Hoje há duas cenas: a fatia de arte (spec 010) e o esqueleto ligado à API (spec 006).

## Como abrir

1. Instale o Godot 4 (versão estável 4.4 ou mais nova).
2. No gerenciador de projetos: Importar → escolha `godot/project.godot`.
3. Aperte F5. Abre a biblioteca e toca a partida gravada. **Tab** abre o quadro de investigação.

Para testar a conexão com a API, abra `scenes/main.tscn` e aperte F6 (F6 roda só a cena aberta). Ela imprime no painel de saída o que a API respondeu.

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
| `scripts/main.gd` | Liga a API à cena 3D mínima |
| `scripts/fatia.gd` | Toca `dados/partida_gravada.json` na biblioteca |
| `scripts/quadro.gd` | Quadro de cortiça, polaroides e fio vermelho |
| `scripts/arte/` | Formas, personagens e salas, todos montados por código |

## Próximos passos

Ligar a fatia à API ao vivo, o que exige a API dizer qual persona é cada personagem (spec 010, riscos), e fazer as outras salas (`docs/arte/pipeline.md`).
