extends Node3D

const ARQUIVO_CONFIG := "res://config.cfg"
const URL_PADRAO := "http://127.0.0.1:8000"

var _api := ApiClient.new()
var _eventos := EventStream.new()


func _ready() -> void:
	var config := ConfigFile.new()
	config.load(ARQUIVO_CONFIG)
	var base_url: String = config.get_value("api", "base_url", URL_PADRAO)
	var partida_id: String = config.get_value("partida", "id", "")

	_montar_cena()
	add_child(_api)
	add_child(_eventos)
	_api.configurar(base_url)
	_api.falhou.connect(_ao_falhar)
	_eventos.evento_recebido.connect(_ao_receber_evento)

	var saude := await _api.obter("/saude")
	print("API: ", saude)
	if not partida_id.is_empty():
		_eventos.conectar(base_url, partida_id)


func _montar_cena() -> void:
	var camera := Camera3D.new()
	add_child(camera)
	camera.position = Vector3(0, 8, 10)
	camera.look_at(Vector3.ZERO)

	var luz := DirectionalLight3D.new()
	luz.rotation_degrees = Vector3(-50, -30, 0)
	add_child(luz)

	var chao := MeshInstance3D.new()
	var plano := PlaneMesh.new()
	plano.size = Vector2(20, 20)
	chao.mesh = plano
	add_child(chao)


func _ao_falhar(caminho: String, motivo: String) -> void:
	push_warning("Falha em %s: %s" % [caminho, motivo])


func _ao_receber_evento(evento: Dictionary) -> void:
	print("Evento: ", evento)
