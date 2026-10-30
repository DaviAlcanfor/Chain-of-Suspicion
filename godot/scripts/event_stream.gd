class_name EventStream
extends Node

signal evento_recebido(evento: Dictionary)
signal conexao_perdida

const ESPERA_RECONEXAO := 2.0

var _socket := WebSocketPeer.new()
var _url := ""
var _ultimo_evento := 0
var _reconectando := false


func _ready() -> void:
	set_process(false)


func conectar(base_url: String, partida_id: String) -> void:
	var base_ws := base_url.replace("http", "ws")
	_url = "%s/partidas/%s/eventos" % [base_ws, partida_id]
	_abrir()
	set_process(true)


func _process(_delta: float) -> void:
	_socket.poll()
	match _socket.get_ready_state():
		WebSocketPeer.STATE_OPEN:
			_ler_pacotes()
		WebSocketPeer.STATE_CLOSED:
			_reconectar()


func _abrir() -> void:
	_socket = WebSocketPeer.new()
	var destino := "%s?ultimo_evento=%d" % [_url, _ultimo_evento]
	if _socket.connect_to_url(destino) != OK:
		_reconectar()


func _ler_pacotes() -> void:
	while _socket.get_available_packet_count() > 0:
		_processar(_socket.get_packet().get_string_from_utf8())


func _processar(texto: String) -> void:
	var evento: Variant = JSON.parse_string(texto)
	if not evento is Dictionary:
		return
	_ultimo_evento = int(evento.get("sequencia", _ultimo_evento))
	evento_recebido.emit(evento)


func _reconectar() -> void:
	if _reconectando:
		return
	_reconectando = true
	conexao_perdida.emit()
	await get_tree().create_timer(ESPERA_RECONEXAO).timeout
	_reconectando = false
	_abrir()
