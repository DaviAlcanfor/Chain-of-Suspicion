extends Node3D
## Fatia vertical (spec 010): toca uma partida gravada. Quem anda, fala ou
## anota vem só dos eventos; este script não decide nada.

const GRAVACAO := "res://dados/partida_gravada.json"
const FONTE := preload("res://fontes/SpecialElite-Regular.ttf")
const PAPEL := Color("e6dcc3")
const TINTA := Color("1c1a1f")
const VERMELHO := Color("b3141c")

var _gravacao: Dictionary
var _pontos: Node3D
var _atores: Dictionary = {}
var _camera: Camera3D
var _quadro: Quadro
var _interface := CanvasLayer.new()
var _balao := PanelContainer.new()
var _nome := Label.new()
var _fala := Label.new()
var _relogio := Label.new()
var _dica := Label.new()
var _quem_fala: Node3D


func _ready() -> void:
	_gravacao = JSON.parse_string(FileAccess.get_file_as_string(GRAVACAO))
	var sala: Node3D = load(_gravacao["cena"]).instantiate()
	add_child(sala)
	_pontos = sala.get_node("pontos")
	_camera = get_viewport().get_camera_3d()
	for presente: Dictionary in _gravacao["presentes"]:
		_colocar(presente)
	_montar_interface()
	_quadro = Quadro.new()
	add_child(_quadro)
	_quadro.montar(_gravacao)
	_tocar_gravacao()


func _process(_delta: float) -> void:
	if _quem_fala == null:
		return
	var escala := get_viewport().get_visible_rect().size / Vector2(get_viewport().size)
	var cabeca := _camera.unproject_position(_quem_fala.global_position + Vector3.UP * 2.1) * escala
	_balao.position = cabeca - Vector2(_balao.size.x / 2.0, _balao.size.y)


func _unhandled_input(evento: InputEvent) -> void:
	if evento is InputEventKey and evento.pressed and not evento.echo and evento.keycode == KEY_TAB:
		alternar_quadro()


func alternar_quadro() -> void:
	_quadro.visible = not _quadro.visible
	_interface.visible = not _quadro.visible
	_mostrar_dica("TAB  ·  quadro", TINTA)


func _colocar(presente: Dictionary) -> void:
	var chave: String = presente["ator"]
	var ator: Personagem = load("res://personagens/%s.tscn" % chave).instantiate()
	ator.position = _ponto(presente["ponto"])
	add_child(ator)
	ator.rotation.y = presente.get("giro", 0.8)
	if presente.get("morto", false):
		ator.deitar()
	_atores[chave] = ator


func _ponto(nome: String) -> Vector3:
	return (_pontos.get_node(nome) as Marker3D).global_position


func _tocar_gravacao() -> void:
	for evento: Dictionary in _gravacao["eventos"]:
		_marcar_relogio(evento["instante"])
		await _tocar(evento)
		await get_tree().create_timer(0.35).timeout
	_mostrar_dica("fim da gravação  ·  TAB  ·  quadro", TINTA)


func _tocar(evento: Dictionary) -> void:
	var ator: Personagem = _atores[evento["ator"]]
	if evento["tipo"] == "fala":
		await _falar(ator, evento)
		return
	match evento["acao"]:
		"mover":
			await ator.andar_ate(_ponto(evento["ponto"]))
		"examinar_local", "interrogar":
			_quadro.anotar(evento["detalhe"], evento["alvo"])
			_mostrar_dica("nova anotação  ·  TAB  ·  quadro", VERMELHO)
			await get_tree().create_timer(1.0).timeout


func _falar(ator: Personagem, evento: Dictionary) -> void:
	var alvo: Personagem = _atores[evento["alvo"]]
	ator.virar_para(alvo.position)
	var texto: String = evento["detalhe"]
	_nome.text = String(ator.dados["nome"]).to_upper()
	_fala.text = texto
	_fala.visible_ratio = 0.0
	_quem_fala = ator
	_balao.reset_size()
	_balao.visible = true
	var tween := create_tween()
	tween.tween_property(_fala, "visible_ratio", 1.0, texto.length() * 0.025)
	await get_tree().create_timer(1.2 + texto.length() * 0.05).timeout
	_balao.visible = false
	_quem_fala = null


func _marcar_relogio(instante: String) -> void:
	var data := "%s/%s  %s" % [instante.substr(8, 2), instante.substr(5, 2), instante.substr(11, 5)]
	_relogio.text = "%s\n%s\n%s" % [String(_gravacao["local"]).to_upper(), _gravacao["mapa"], data]


func _mostrar_dica(texto: String, cor: Color) -> void:
	_dica.text = texto
	_dica.add_theme_color_override("font_color", cor)


func _montar_interface() -> void:
	add_child(_interface)
	_interface.add_child(_etiqueta(_relogio, Vector2(32, 28), 20))
	_interface.add_child(_etiqueta(_dica, Vector2(32, 830), 18))
	_mostrar_dica("TAB  ·  quadro", TINTA)
	var coluna := VBoxContainer.new()
	_estilizar(_nome, 15, VERMELHO)
	_estilizar(_fala, 18, TINTA)
	_fala.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_fala.custom_minimum_size.x = 340
	coluna.add_child(_nome)
	coluna.add_child(_fala)
	_balao.add_theme_stylebox_override("panel", _papel())
	_balao.add_child(coluna)
	_balao.visible = false
	_interface.add_child(_balao)


func _etiqueta(rotulo: Label, pos: Vector2, tamanho: int) -> PanelContainer:
	var painel := PanelContainer.new()
	painel.position = pos
	painel.add_theme_stylebox_override("panel", _papel())
	_estilizar(rotulo, tamanho, TINTA)
	painel.add_child(rotulo)
	return painel


func _estilizar(rotulo: Label, tamanho: int, cor: Color) -> void:
	rotulo.add_theme_font_override("font", FONTE)
	rotulo.add_theme_font_size_override("font_size", tamanho)
	rotulo.add_theme_color_override("font_color", cor)


func _papel() -> StyleBoxFlat:
	var estilo := StyleBoxFlat.new()
	estilo.bg_color = PAPEL
	estilo.set_content_margin_all(12)
	estilo.shadow_color = Color(0, 0, 0, 0.55)
	estilo.shadow_size = 6
	estilo.shadow_offset = Vector2(2, 3)
	return estilo
