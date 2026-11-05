class_name Quadro
extends CanvasLayer
## Quadro de investigação: cortiça, polaroides e fio vermelho. Só mostra o
## que a gravação tornou público ou o que os eventos revelaram.

const MAQUINA := preload("res://fontes/SpecialElite-Regular.ttf")
const CANETA := preload("res://fontes/PermanentMarker-Regular.ttf")
const VERMELHO := Color("b3141c")
const CREME := Color("e6dcc3")
const AMARELO := Color("e0cf8a")
const FOTO := Vector2(190, 240)
const LUGAR_VITIMA := Vector2(705, 300)
const LUGARES_SUSPEITOS: Array[Vector2] = [
	Vector2(130, 130), Vector2(1280, 130), Vector2(130, 540), Vector2(1280, 540),
]
const LUGARES_NOTAS: Array[Vector2] = [
	Vector2(450, 210), Vector2(965, 200), Vector2(960, 580), Vector2(700, 640),
]

var _cartoes := Control.new()
var _fios := Node2D.new()
var _papeis := Control.new()
var _alfinetes := Control.new()
var _ponto_de: Dictionary = {}
var _rng := RandomNumberGenerator.new()
var _notas := 0


func _ready() -> void:
	layer = 10
	visible = false
	_rng.seed = 11
	var cortica := ColorRect.new()
	cortica.set_anchors_preset(Control.PRESET_FULL_RECT)
	var material := ShaderMaterial.new()
	material.shader = load("res://shaders/cortica.gdshader")
	cortica.material = material
	add_child(cortica)
	add_child(_cartoes)
	add_child(_fios)
	add_child(_papeis)
	add_child(_alfinetes)


func montar(gravacao: Dictionary) -> void:
	_titulo()
	_recorte(gravacao["manchete"], gravacao["resumo"])
	var vitima: String = gravacao["vitima"]
	_polaroide(vitima, LUGAR_VITIMA)
	_carimbar(LUGAR_VITIMA)
	var suspeitos: Array = gravacao["suspeitos"]
	for i in suspeitos.size():
		var chave: String = suspeitos[i]
		_polaroide(chave, LUGARES_SUSPEITOS[i])
		_fio(_ponto_de[chave], _ponto_de[vitima])


## ponytail: há 4 lugares para nota; a 5ª em diante reaproveita os lugares.
func anotar(texto: String, alvo: String) -> void:
	var pos := LUGARES_NOTAS[_notas % LUGARES_NOTAS.size()]
	_notas += 1
	var nota := _papel(AMARELO, pos, Vector2(190, 110))
	nota.reparent(_papeis)
	nota.add_child(_rotulo(texto, MAQUINA, {"tamanho": 17, "cor": Color("1c1a1f"), "largura": 166}))
	var ponto := pos + Vector2(95, 8)
	_alfinete(ponto)
	_fio(ponto, _ponto_de[alvo])


func _titulo() -> void:
	var papel := _papel(CREME, Vector2(520, 40), Vector2(560, 120))
	var rotulo := _rotulo("QUEM FOI?", CANETA, {"tamanho": 68, "cor": VERMELHO, "largura": 536})
	rotulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	papel.add_child(rotulo)
	_alfinete(Vector2(800, 50))


func _recorte(manchete: String, resumo: String) -> void:
	var papel := _papel(Color("cfc8b4"), Vector2(400, 570), Vector2(270, 250))
	var coluna := VBoxContainer.new()
	coluna.add_child(_rotulo(manchete, MAQUINA, {"tamanho": 20, "cor": Color.BLACK, "largura": 246}))
	coluna.add_child(_rotulo(resumo, MAQUINA, {"tamanho": 14, "cor": Color("3a3833"), "largura": 246}))
	papel.add_child(coluna)
	papel.reparent(_papeis)
	_alfinete(Vector2(640, 586))


func _polaroide(chave: String, pos: Vector2) -> void:
	var cartao := _papel(Color("efeae0"), pos, FOTO)
	var coluna := VBoxContainer.new()
	var pessoa: Personagem = load("res://personagens/%s.tscn" % chave).instantiate()
	var foto := _fotografar(pessoa)
	coluna.add_child(foto)
	cartao.add_child(coluna)
	var nome := _rotulo(String(pessoa.dados["nome"]), CANETA, {"tamanho": 24, "cor": Color("1c1a1f"), "largura": 166})
	nome.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	coluna.add_child(nome)
	var ponto := pos + Vector2(FOTO.x / 2.0, 8)
	_ponto_de[chave] = ponto
	_alfinete(ponto)


func _fotografar(pessoa: Personagem) -> TextureRect:
	var estudio := SubViewport.new()
	estudio.size = Vector2i(332, 332)
	estudio.own_world_3d = true
	estudio.render_target_update_mode = SubViewport.UPDATE_ONCE
	add_child(estudio)
	var cenario := Node3D.new()
	estudio.add_child(cenario)
	cenario.add_child(pessoa)
	var topo := float(pessoa.dados["altura_cm"]) / 175.0 * 1.45
	for i in 6:
		Kit.caixa(cenario, Vector3(3, 0.012, 0.01), Color("55524c"), Vector3(0, topo - 0.5 + i * 0.2, -0.6))
	Kit.caixa(cenario, Vector3(4, 4, 0.05), Color("b8b2a3"), Vector3(0, topo, -0.65))
	var luz := DirectionalLight3D.new()
	luz.rotation_degrees = Vector3(-30, 35, 0)
	luz.light_energy = 1.4
	luz.shadow_enabled = true
	cenario.add_child(luz)
	var camera := Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 0.95
	camera.position = Vector3(0, topo, 2.5)
	camera.environment = _ambiente_da_foto()
	cenario.add_child(camera)
	var foto := TextureRect.new()
	foto.texture = estudio.get_texture()
	foto.custom_minimum_size = Vector2(166, 166)
	foto.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	var preto_e_branco := ShaderMaterial.new()
	preto_e_branco.shader = load("res://shaders/foto.gdshader")
	foto.material = preto_e_branco
	return foto


func _ambiente_da_foto() -> Environment:
	var ambiente := Environment.new()
	ambiente.background_mode = Environment.BG_COLOR
	ambiente.background_color = Color("b8b2a3")
	ambiente.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	ambiente.ambient_light_color = Color("9a9a9a")
	ambiente.ambient_light_energy = 0.7
	return ambiente


func _carimbar(pos: Vector2) -> void:
	var inicio := pos + Vector2(14, 16)
	var fim := inicio + Vector2(162, 162)
	_risco([inicio, fim])
	_risco([Vector2(fim.x, inicio.y), Vector2(inicio.x, fim.y)])
	var carimbo := _rotulo("MORTO", CANETA, {"tamanho": 36, "cor": VERMELHO, "largura": 170})
	carimbo.position = pos + Vector2(28, 118)
	carimbo.rotation = -0.3
	_alfinetes.add_child(carimbo)


func _risco(pontos: Array[Vector2]) -> void:
	var linha := Line2D.new()
	linha.points = PackedVector2Array(pontos)
	linha.width = 7.0
	linha.default_color = VERMELHO
	_fios.add_child(linha)


## Fio barrigudo: uma curva simples com sombra deslocada embaixo.
func _fio(de: Vector2, para: Vector2) -> void:
	var meio := (de + para) / 2.0 + Vector2(0, 26)
	var pontos := PackedVector2Array()
	for i in 13:
		var t := i / 12.0
		pontos.append(de.lerp(meio, t).lerp(meio.lerp(para, t), t))
	for camada: Array in [[Color(0, 0, 0, 0.35), Vector2(3, 5)], [VERMELHO, Vector2.ZERO]]:
		var linha := Line2D.new()
		linha.points = pontos
		linha.width = 3.0
		linha.default_color = camada[0]
		linha.position = camada[1]
		_fios.add_child(linha)


func _alfinete(pos: Vector2) -> void:
	var cabeca := Panel.new()
	var estilo := StyleBoxFlat.new()
	estilo.bg_color = VERMELHO
	estilo.set_corner_radius_all(9)
	estilo.shadow_color = Color(0, 0, 0, 0.6)
	estilo.shadow_size = 3
	estilo.shadow_offset = Vector2(2, 3)
	cabeca.add_theme_stylebox_override("panel", estilo)
	cabeca.size = Vector2(18, 18)
	cabeca.position = pos - cabeca.size / 2.0
	_alfinetes.add_child(cabeca)


func _papel(cor: Color, pos: Vector2, tamanho: Vector2) -> PanelContainer:
	var papel := PanelContainer.new()
	var estilo := StyleBoxFlat.new()
	estilo.bg_color = cor
	estilo.set_content_margin_all(12)
	estilo.shadow_color = Color(0, 0, 0, 0.5)
	estilo.shadow_size = 7
	estilo.shadow_offset = Vector2(3, 5)
	papel.add_theme_stylebox_override("panel", estilo)
	papel.position = pos
	papel.custom_minimum_size = tamanho
	papel.pivot_offset = tamanho / 2.0
	papel.rotation = _rng.randf_range(-0.025, 0.025)
	_cartoes.add_child(papel)
	return papel


func _rotulo(texto: String, fonte: Font, jeito: Dictionary) -> Label:
	var rotulo := Label.new()
	rotulo.text = texto
	rotulo.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	rotulo.custom_minimum_size.x = jeito["largura"]
	rotulo.add_theme_font_override("font", fonte)
	rotulo.add_theme_font_size_override("font_size", jeito["tamanho"])
	rotulo.add_theme_color_override("font_color", jeito["cor"])
	return rotulo
