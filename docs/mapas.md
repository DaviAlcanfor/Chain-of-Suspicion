# Mapas

> Gerado por `tools/gerar_docs.py`. Não edite à mão: mude `conteudo/mapas.py`.

Cada local tem uma chave estável, que o servidor usa como id determinístico e o Godot usa para carregar a cena. Os tempos são de deslocamento entre locais vizinhos.

## Mansão Villaça (`mansao`)

Casarão de dois andares numa colina afastada da cidade, com madeira escura, tapetes pesados e corredores que rangem. A noite cai cedo e o único caminho até a estrada está bloqueado pela chuva.

Entrada do detetive: `hall`

| Chave | Nome | Descrição | Cena do Godot |
| --- | --- | --- | --- |
| `hall` | Hall | Saguão amplo com escadaria de madeira e relógio de pêndulo. | `res://cenas/mansao/hall.tscn` |
| `biblioteca` | Biblioteca | Estantes até o teto, lareira apagada e poltronas de couro. | `res://cenas/mansao/biblioteca.tscn` |
| `escritorio` | Escritório | Mesa de mogno, cofre embutido e papéis empilhados. | `res://cenas/mansao/escritorio.tscn` |
| `sala_de_jantar` | Sala de Jantar | Mesa para doze, candelabros e louça de gala. | `res://cenas/mansao/sala_de_jantar.tscn` |
| `cozinha` | Cozinha | Fogão a lenha, bancada de mármore e despensa abarrotada. | `res://cenas/mansao/cozinha.tscn` |
| `jardim` | Jardim | Canteiros, estufa de ervas e um banco sob a figueira. | `res://cenas/mansao/jardim.tscn` |
| `quarto` | Quarto de Hóspedes | Cama de dossel, penteadeira e janela para o jardim. | `res://cenas/mansao/quarto.tscn` |
| `adega` | Adega | Porão frio de pedra com garrafas empoeiradas. | `res://cenas/mansao/adega.tscn` |

| Passagem | Tempo |
| --- | --- |
| hall ↔ biblioteca | 1 min |
| hall ↔ escritorio | 2 min |
| hall ↔ sala_de_jantar | 1 min |
| sala_de_jantar ↔ cozinha | 1 min |
| cozinha ↔ jardim | 2 min |
| hall ↔ quarto | 2 min |
| cozinha ↔ adega | 2 min |

## Cruzeiro Estrela do Sul (`navio`)

Pequeno navio de cruzeiro em travessia noturna, com salão de baile, bar e cabines luxuosas. Em alto-mar não há para onde fugir nem como pedir ajuda.

Entrada do detetive: `conves`

| Chave | Nome | Descrição | Cena do Godot |
| --- | --- | --- | --- |
| `conves` | Convés | Pista aberta ao vento, com espreguiçadeiras e vista para o mar escuro. | `res://cenas/navio/conves.tscn` |
| `salao` | Salão de Baile | Pista de dança, palco para a banda e lustres de cristal. | `res://cenas/navio/salao.tscn` |
| `bar` | Bar | Balcão de madeira polida, banquetas e luz baixa. | `res://cenas/navio/bar.tscn` |
| `corredor` | Corredor das Cabines | Corredor estreito com carpete vermelho e portas numeradas. | `res://cenas/navio/corredor.tscn` |
| `cabine_vip` | Cabine VIP | Suíte com sacada fechada, cofre e cama de casal. | `res://cenas/navio/cabine_vip.tscn` |
| `ponte` | Ponte de Comando | Painel de navegação, leme e cartas náuticas. | `res://cenas/navio/ponte.tscn` |
| `casa_de_maquinas` | Casa de Máquinas | Barulho constante, vapor e cheiro de óleo. | `res://cenas/navio/casa_de_maquinas.tscn` |
| `enfermaria` | Enfermaria | Maca, armário de remédios e luz branca. | `res://cenas/navio/enfermaria.tscn` |

| Passagem | Tempo |
| --- | --- |
| conves ↔ salao | 1 min |
| salao ↔ bar | 1 min |
| salao ↔ corredor | 1 min |
| corredor ↔ cabine_vip | 1 min |
| conves ↔ ponte | 2 min |
| conves ↔ casa_de_maquinas | 3 min |
| corredor ↔ enfermaria | 2 min |

## Pousada Serra Branca (`pousada`)

Pousada de madeira no alto da serra, isolada por uma nevasca que derrubou a linha telefônica. Lareira acesa, cheiro de lenha e poucos hóspedes.

Entrada do detetive: `recepcao`

| Chave | Nome | Descrição | Cena do Godot |
| --- | --- | --- | --- |
| `recepcao` | Recepção | Balcão de madeira, quadro de chaves e sino de latão. | `res://cenas/pousada/recepcao.tscn` |
| `lareira` | Salão da Lareira | Poltronas gastas, tapete de lã e lareira crepitando. | `res://cenas/pousada/lareira.tscn` |
| `refeitorio` | Refeitório | Mesas compridas, bules fumegantes e janelas embaçadas. | `res://cenas/pousada/refeitorio.tscn` |
| `cozinha` | Cozinha | Panelas de cobre, facas na parede e despensa fria. | `res://cenas/pousada/cozinha.tscn` |
| `corredor` | Corredor dos Quartos | Piso de tábuas que rangem e portas com plaquinhas. | `res://cenas/pousada/corredor.tscn` |
| `quarto_12` | Quarto 12 | Aposento do dono, com escrivaninha, cofre pequeno e fotos antigas. | `res://cenas/pousada/quarto_12.tscn` |
| `galpao` | Galpão de Lenha | Barracão externo com lenha empilhada, machado e ferramentas. | `res://cenas/pousada/galpao.tscn` |
| `sotao` | Sótão | Baús, caixas de documentos e uma janela redonda. | `res://cenas/pousada/sotao.tscn` |

| Passagem | Tempo |
| --- | --- |
| recepcao ↔ lareira | 1 min |
| lareira ↔ refeitorio | 1 min |
| refeitorio ↔ cozinha | 1 min |
| recepcao ↔ corredor | 1 min |
| corredor ↔ quarto_12 | 1 min |
| cozinha ↔ galpao | 2 min |
| corredor ↔ sotao | 2 min |
