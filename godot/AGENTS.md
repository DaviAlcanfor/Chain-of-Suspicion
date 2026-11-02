# AGENTS.md — `godot/`

Cliente 3D (Godot 4). **Burro por princípio**: mostra eventos e envia comandos pela API; não decide regra (constituição, princípio 7).

## Estrutura

| Caminho | O que tem |
| --- | --- |
| `project.godot`, `config.cfg` | projeto e configuração (URL da API) |
| `scenes/main.tscn` | cena inicial |
| `scripts/api_client.gd`, `event_stream.gd`, `main.gd` | cliente HTTP, WebSocket de eventos e cena principal |
| `README.md` | como abrir o projeto e conceitos básicos do Godot |

## Contratos que o cliente consome

- HTTP: `/saude`, `/partidas`, `/partidas/{id}`, `/partidas/{id}/estado`, `/acoes`, `/pausar`, `/retomar`.
- WebSocket: `/partidas/{id}/eventos?ultimo_evento=N` (reconexão retoma de `N`).
- Aparência: `docs/elenco.md` (enums de cabelo, pele, roupa, paleta, acessórios) e `Persona.modelo_godot` (`res://personagens/<chave>.tscn`).
- Cenas: `docs/mapas.md` (`res://cenas/<mapa>/<local>.tscn`).

## Regras desta pasta

- Nenhuma regra de jogo em GDScript. Dúvida de "pode ou não" => pergunte à API.
- Tudo o que o jogador vê vem de evento ou de `/estado`; nunca invente estado local.
- Nomes de cena e modelo seguem as chaves de `docs/`; renomear exige mudar `conteudo/` e regenerar docs.
- Ainda não há arte nem cenas finais: os caminhos são reservados.
- Explique conceitos do Godot devagar (o dono é de dados): nó, cena, sinal, script.
