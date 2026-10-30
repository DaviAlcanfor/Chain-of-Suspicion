class_name ApiClient
extends Node

signal falhou(caminho: String, motivo: String)

const CABECALHOS := ["Content-Type: application/json"]

var _base_url := ""


func configurar(base_url: String) -> void:
	_base_url = base_url


func obter(caminho: String) -> Dictionary:
	return await _requisitar(caminho, HTTPClient.METHOD_GET, "")


func enviar(caminho: String, corpo: Dictionary) -> Dictionary:
	return await _requisitar(caminho, HTTPClient.METHOD_POST, JSON.stringify(corpo))


func _requisitar(caminho: String, metodo: HTTPClient.Method, corpo: String) -> Dictionary:
	var requisicao := HTTPRequest.new()
	add_child(requisicao)
	var erro := requisicao.request(_base_url + caminho, CABECALHOS, metodo, corpo)
	if erro != OK:
		requisicao.queue_free()
		falhou.emit(caminho, error_string(erro))
		return {}
	var resultado: Array = await requisicao.request_completed
	requisicao.queue_free()
	return _interpretar(caminho, resultado)


func _interpretar(caminho: String, resultado: Array) -> Dictionary:
	var status: int = resultado[1]
	if resultado[0] != HTTPRequest.RESULT_SUCCESS or status < 200 or status >= 300:
		falhou.emit(caminho, "status %d" % status)
		return {}
	var corpo: PackedByteArray = resultado[3]
	var json: Variant = JSON.parse_string(corpo.get_string_from_utf8())
	return json if json is Dictionary else {}
