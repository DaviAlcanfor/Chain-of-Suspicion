class_name Personagem
extends Node3D
## Boneco modular: lê a aparência em dados/elenco.json e monta o corpo com
## formas simples. A frente é +Z e os pés ficam em y = 0.

const ARQUIVO_ELENCO := "res://dados/elenco.json"
const VELOCIDADE := 1.5

const LARGURA := {"magro": 0.86, "medio": 1.0, "robusto": 1.28, "atletico": 1.12}
const PELE := {
	"claro": Color("e8c2a0"),
	"medio_claro": Color("d6a57f"),
	"medio": Color("b98258"),
	"medio_escuro": Color("8d5a3a"),
	"escuro": Color("5c3a26"),
}
const CABELO := {
	"preto": Color("15131a"),
	"castanho": Color("41281a"),
	"castanho_claro": Color("7a5532"),
	"loiro_platinado": Color("e8dcb0"),
	"ruivo": Color("a8461e"),
	"grisalho": Color("8b8c90"),
	"branco": Color("d9d8d3"),
}
const BRANCO := Color("e4dfd2")
const PRETO := Color("17151a")
const JEANS := Color("34466b")
const COURO := Color("3a2415")
const OURO := Color("c79a3b")
const PRATA := Color("a9acb2")

static var _elenco: Dictionary = {}

@export var chave: String = ""

var dados: Dictionary = {}
var _corpo := Node3D.new()
var _perna_e := Node3D.new()
var _perna_d := Node3D.new()
var _braco_e := Node3D.new()
var _braco_d := Node3D.new()
var _largura := 1.0
var _pele := Color.WHITE
var _andando := false
var _fase := 0.0


func _ready() -> void:
	if _elenco.is_empty():
		_elenco = JSON.parse_string(FileAccess.get_file_as_string(ARQUIVO_ELENCO))
	dados = _elenco[chave]
	_largura = LARGURA[dados["porte"]]
	_pele = PELE[dados["pele"]]
	_fase = float(hash(chave) % 100)
	_corpo.scale = Vector3.ONE * float(dados["altura_cm"]) / 175.0
	add_child(_corpo)
	_montar_cabeca()
	_montar_cabelo()
	_montar_pelos()
	_vestir()
	_equipar()


func _process(delta: float) -> void:
	_fase += delta
	var balanco := sin(_fase * 8.5) * 0.6 if _andando else 0.0
	_perna_e.rotation.x = balanco
	_perna_d.rotation.x = -balanco
	_braco_e.rotation.x = -balanco * 0.7
	_braco_d.rotation.x = balanco * 0.7
	_corpo.position.y = absf(sin(_fase * 8.5)) * 0.03 if _andando else sin(_fase * 1.6) * 0.004


func andar_ate(destino: Vector3) -> void:
	virar_para(destino)
	_andando = true
	var tween := create_tween()
	tween.tween_property(self, "position", destino, position.distance_to(destino) / VELOCIDADE)
	await tween.finished
	_andando = false


func virar_para(alvo: Vector3) -> void:
	var direcao := alvo - position
	if not direcao.is_zero_approx():
		rotation.y = atan2(direcao.x, direcao.z)


func deitar() -> void:
	set_process(false)
	rotation = Vector3(-PI / 2.0, rotation.y, 0)
	position.y = 0.14
	_braco_e.rotation.z = -1.0
	_perna_d.rotation.z = 0.25


func _montar_cabeca() -> void:
	Kit.cilindro(_corpo, Vector2(0.055, 0.065), 0.12, _pele, Vector3(0, 1.42, 0))
	Kit.esfera(_corpo, 0.15, _pele, Vector3(0, 1.58, 0))
	for lado: float in [-1.0, 1.0]:
		Kit.esfera(_corpo, 0.021, PRETO, Vector3(lado * 0.058, 1.6, 0.135))
		Kit.caixa(_corpo, Vector3(0.065, 0.014, 0.02), CABELO[dados["cabelo_cor"]].darkened(0.2), Vector3(lado * 0.058, 1.645, 0.135))
	Kit.esfera(_corpo, 0.02, _pele.darkened(0.1), Vector3(0, 1.56, 0.15))
	var boca: Color = Color("a3131f") if "batom_vermelho" in dados["acessorios"] else _pele.darkened(0.45)
	Kit.caixa(_corpo, Vector3(0.06, 0.014, 0.02), boca, Vector3(0, 1.505, 0.135))


func _montar_cabelo() -> void:
	var cor: Color = CABELO[dados["cabelo_cor"]]
	match dados["cabelo_estilo"]:
		"curto":
			_touca(cor)
		"penteado_para_tras":
			_touca(cor)
			Kit.esfera(_corpo, 0.14, cor, Vector3(0, 1.6, -0.075))
		"repartido_de_lado":
			_touca(cor)
			Kit.caixa(_corpo, Vector3(0.2, 0.05, 0.1), cor, Vector3(0.05, 1.715, 0.085)).rotation.z = -0.3
		"ralo":
			Kit.esfera(_corpo, 0.14, cor, Vector3(0, 1.57, -0.05))
			for lado: float in [-1.0, 1.0]:
				Kit.esfera(_corpo, 0.05, cor, Vector3(lado * 0.135, 1.6, -0.015))
		"volumoso":
			Kit.esfera(_corpo, 0.19, cor, Vector3(0, 1.67, -0.06))
		"coque":
			_touca(cor)
			Kit.esfera(_corpo, 0.07, cor, Vector3(0, 1.81, -0.06))
		"rabo_de_cavalo":
			_touca(cor)
			Kit.capsula(_corpo, 0.04, 0.38, cor, Vector3(0, 1.5, -0.18))
		"ondulado_nos_ombros":
			_mechas(cor, 0.3)
		"ondulado_comprido":
			_mechas(cor, 0.42)
		"ondas_de_festa":
			_mechas(cor, 0.52)
			Kit.esfera(_corpo, 0.08, cor, Vector3(0.1, 1.73, 0.03))


func _touca(cor: Color) -> void:
	Kit.esfera(_corpo, 0.156, cor, Vector3(0, 1.63, -0.03))


func _mechas(cor: Color, comprimento: float) -> void:
	_touca(cor)
	Kit.capsula(_corpo, 0.125, comprimento + 0.08, cor, Vector3(0, 1.62 - comprimento / 2.0, -0.075))
	for lado: float in [-1.0, 1.0]:
		Kit.capsula(_corpo, 0.052, comprimento, cor, Vector3(lado * 0.135, 1.64 - comprimento / 2.0, 0.0))


func _montar_pelos() -> void:
	var cor: Color = CABELO[dados["cabelo_cor"]]
	match dados["pelos_faciais"]:
		"nenhum":
			pass
		"bigode":
			Kit.caixa(_corpo, Vector3(0.12, 0.028, 0.03), cor, Vector3(0, 1.53, 0.14))
		"bigode_caido":
			Kit.caixa(_corpo, Vector3(0.12, 0.024, 0.03), cor, Vector3(0, 1.532, 0.14))
			for lado: float in [-1.0, 1.0]:
				Kit.caixa(_corpo, Vector3(0.022, 0.07, 0.025), cor, Vector3(lado * 0.055, 1.495, 0.13))
		"barba_rente":
			Kit.esfera(_corpo, 0.135, cor.lerp(_pele, 0.35), Vector3(0, 1.525, 0.022))
			Kit.caixa(_corpo, Vector3(0.06, 0.014, 0.02), _pele.darkened(0.45), Vector3(0, 1.505, 0.155))
		"barba_aparada":
			Kit.esfera(_corpo, 0.138, cor, Vector3(0, 1.515, 0.022))
			Kit.caixa(_corpo, Vector3(0.06, 0.014, 0.02), _pele.lightened(0.15), Vector3(0, 1.51, 0.16))


func _vestir() -> void:
	var cor := Color(dados["hex_da_roupa"])
	var calca_escura := cor.darkened(0.3)
	match dados["roupa"]:
		"tailleur":
			_corte({"tronco": cor, "pernas": _pele, "saia": 0.42, "saia_cor": cor, "gola": BRANCO})
		"terno":
			_corte({"tronco": cor, "pernas": cor, "gola": BRANCO, "gravata": cor.darkened(0.55)})
		"avental_sobre_vestido":
			_corte({"tronco": cor, "pernas": _pele, "saia": 0.62, "saia_cor": cor})
			Kit.caixa(_corpo, Vector3(0.24 * _largura, 0.9, 0.02), BRANCO, Vector3(0, 0.86, 0.15 * _largura + 0.03))
		"camisa_de_linho_e_jeans":
			_corte({"tronco": cor, "pernas": JEANS, "gola": cor.lightened(0.3)})
		"sobretudo_e_gravata":
			_corte({"tronco": cor, "pernas": PRETO, "saia": 0.68, "saia_cor": cor, "gola": BRANCO, "gravata": Color("5a1a20")})
		"colete_de_tweed":
			_corte({"tronco": cor, "bracos": BRANCO, "pernas": calca_escura, "gola": BRANCO, "gravata": PRETO})
		"blazer_e_camisa":
			_corte({"tronco": cor, "pernas": cor, "gola": BRANCO})
		"paleto_e_gravata_borboleta":
			_corte({"tronco": cor, "pernas": calca_escura, "gola": BRANCO})
			for lado: float in [-1.0, 1.0]:
				Kit.caixa(_corpo, Vector3(0.05, 0.04, 0.02), PRETO, Vector3(lado * 0.03, 1.31, 0.14 * _largura + 0.03))
		"jaqueta_de_couro":
			_corte({"tronco": cor, "pernas": JEANS.darkened(0.25), "gola": PRETO})
		"macacao_de_brim":
			_corte({"tronco": BRANCO.darkened(0.15), "pernas": cor})
			Kit.caixa(_corpo, Vector3(0.24 * _largura, 0.3, 0.03), cor, Vector3(0, 1.02, 0.14 * _largura))
			for lado: float in [-1.0, 1.0]:
				Kit.caixa(_corpo, Vector3(0.03, 0.3, 0.3 * _largura), cor, Vector3(lado * 0.09, 1.25, 0))
		"vestido_de_noite":
			_corte({"tronco": cor, "bracos": _pele, "pernas": _pele, "saia": 0.8, "saia_cor": cor})
		"uniforme_de_comandante":
			_corte({"tronco": cor, "pernas": cor, "gola": BRANCO, "gravata": PRETO})
			for lado: float in [-1.0, 1.0]:
				Kit.caixa(_corpo, Vector3(0.1, 0.02, 0.1), OURO, Vector3(lado * 0.21 * _largura, 1.39, 0))
			for y: float in [1.1, 1.0, 0.9]:
				Kit.esfera(_corpo, 0.012, OURO, Vector3(0.03, y, 0.15 * _largura))


func _corte(corte: Dictionary) -> void:
	var tronco: Color = corte["tronco"]
	var bracos: Color = corte.get("bracos", tronco)
	var pernas: Color = corte["pernas"]
	Kit.cilindro(_corpo, Vector2(0.21, 0.155) * _largura, 0.56, tronco, Vector3(0, 1.1, 0)).scale.z = 0.72
	_membro(_perna_e, Vector3(-0.085 * _largura, 0.84, 0), {"cor": pernas, "raio": 0.07 * _largura, "ponta": PRETO})
	_membro(_perna_d, Vector3(0.085 * _largura, 0.84, 0), {"cor": pernas, "raio": 0.07 * _largura, "ponta": PRETO})
	_membro(_braco_e, Vector3(-0.245 * _largura, 1.32, 0), {"cor": bracos, "raio": 0.052 * _largura, "ponta": _pele, "curto": true})
	_membro(_braco_d, Vector3(0.245 * _largura, 1.32, 0), {"cor": bracos, "raio": 0.052 * _largura, "ponta": _pele, "curto": true})
	if corte.has("saia"):
		var comprimento: float = corte["saia"]
		var saia := Kit.cilindro(_corpo, Vector2(0.16, 0.16 + comprimento * 0.22) * _largura, comprimento, corte["saia_cor"], Vector3(0, 0.86 - comprimento / 2.0, 0))
		saia.scale.z = 0.8
	if corte.has("gola"):
		Kit.caixa(_corpo, Vector3(0.1, 0.16, 0.02), corte["gola"], Vector3(0, 1.28, 0.14 * _largura)).rotation.x = -0.12
	if corte.has("gravata"):
		Kit.caixa(_corpo, Vector3(0.035, 0.26, 0.02), corte["gravata"], Vector3(0, 1.2, 0.155 * _largura)).rotation.x = -0.1


func _membro(pivo: Node3D, ombro: Vector3, jeito: Dictionary) -> void:
	pivo.position = ombro
	_corpo.add_child(pivo)
	var braco: bool = jeito.has("curto")
	var comprimento := 0.62 if braco else 0.8
	Kit.capsula(pivo, jeito["raio"], comprimento, jeito["cor"], Vector3(0, -comprimento / 2.0, 0))
	if braco:
		Kit.esfera(pivo, 0.05, jeito["ponta"], Vector3(0, -comprimento, 0))
	else:
		Kit.caixa(pivo, Vector3(0.11, 0.07, 0.24), jeito["ponta"], Vector3(0, -comprimento, 0.04))


func _equipar() -> void:
	for item: String in dados["acessorios"]:
		_acessorio(item)


func _acessorio(item: String) -> void:
	var mao := Vector3(0, -0.66, 0)
	var peito := 0.155 * _largura
	match item:
		"batom_vermelho":
			pass
		"colar_de_perolas":
			Kit.anel(_corpo, 0.1, BRANCO, Vector3(0, 1.33, 0.03)).rotation.x = 0.45
		"anel_de_safira":
			Kit.esfera(_braco_d, 0.018, Color("2a56c8"), mao + Vector3(0, 0.02, 0.04))
		"oculos_de_aro_fino":
			for lado: float in [-1.0, 1.0]:
				Kit.anel(_corpo, 0.04, PRETO, Vector3(lado * 0.058, 1.6, 0.14)).rotation.x = PI / 2.0
		"pasta_de_couro":
			Kit.caixa(_braco_d, Vector3(0.09, 0.28, 0.38), COURO, mao + Vector3(0, -0.12, 0))
		"brincos_de_argola":
			for lado: float in [-1.0, 1.0]:
				Kit.anel(_corpo, 0.03, OURO, Vector3(lado * 0.15, 1.51, 0)).rotation.z = PI / 2.0
		"pulseiras_de_couro":
			Kit.anel(_braco_e, 0.058, COURO, Vector3(0, -0.52, 0))
		"caderneta":
			Kit.caixa(_braco_d, Vector3(0.1, 0.14, 0.03), Color("7d1f22"), mao + Vector3(0, 0.0, 0.07))
		"chapeu_de_feltro":
			_chapeu(Color("3a2f26"), 0.25)
		"bengala_de_ebano":
			Kit.cilindro(_braco_d, Vector2(0.014, 0.014), 0.72, PRETO, mao + Vector3(0, -0.34, 0.04))
			Kit.esfera(_braco_d, 0.028, OURO, mao + Vector3(0, 0.03, 0.04))
		"relogio_de_bolso":
			Kit.esfera(_corpo, 0.022, OURO, Vector3(0.09 * _largura, 1.05, peito))
		"distintivo":
			Kit.esfera(_corpo, 0.03, OURO, Vector3(-0.09 * _largura, 1.22, peito))
		"relogio_de_pulso":
			Kit.anel(_braco_e, 0.058, PRATA, Vector3(0, -0.52, 0))
		"maleta_medica":
			Kit.caixa(_braco_d, Vector3(0.14, 0.2, 0.32), PRETO, mao + Vector3(0, -0.1, 0))
			Kit.caixa(_braco_d, Vector3(0.02, 0.1, 0.03), OURO, mao + Vector3(0.07, -0.1, 0))
		"estetoscopio":
			Kit.anel(_corpo, 0.12, PRETO, Vector3(0, 1.3, 0.04)).rotation.x = 0.5
			Kit.esfera(_corpo, 0.025, PRATA, Vector3(0.05, 1.12, peito))
		"gravador":
			Kit.caixa(_braco_d, Vector3(0.1, 0.14, 0.05), PRETO, mao + Vector3(0, 0, 0.07))
		"mochila_de_lona":
			Kit.caixa(_corpo, Vector3(0.3 * _largura, 0.42, 0.14), Color("5d5a3c"), Vector3(0, 1.12, -0.21 * _largura))
		"molho_de_chaves":
			Kit.anel(_corpo, 0.035, PRATA, Vector3(0.17 * _largura, 0.82, 0.06)).rotation.z = PI / 2.0
		"chapeu_de_palha":
			_chapeu(Color("c9ae6a"), 0.31)
		"leque":
			Kit.cilindro(_braco_d, Vector2(0.14, 0.005), 0.012, Color("1d1a22"), mao + Vector3(0, 0.1, 0.08)).rotation.x = PI / 2.0
		"brincos_longos":
			for lado: float in [-1.0, 1.0]:
				Kit.caixa(_corpo, Vector3(0.012, 0.1, 0.012), OURO, Vector3(lado * 0.15, 1.46, 0.02))
		"bone_de_comandante":
			Kit.cilindro(_corpo, Vector2(0.18, 0.15), 0.1, BRANCO, Vector3(0, 1.75, -0.005))
			Kit.caixa(_corpo, Vector3(0.2, 0.02, 0.1), PRETO, Vector3(0, 1.7, 0.16)).rotation.x = 0.25
			Kit.caixa(_corpo, Vector3(0.05, 0.04, 0.02), OURO, Vector3(0, 1.76, 0.165))
		"binoculo":
			for lado: float in [-1.0, 1.0]:
				Kit.cilindro(_corpo, Vector2(0.03, 0.03), 0.1, PRETO, Vector3(lado * 0.04, 1.14, peito + 0.02)).rotation.x = PI / 2.0


func _chapeu(cor: Color, aba: float) -> void:
	Kit.cilindro(_corpo, Vector2(aba, aba), 0.02, cor, Vector3(0, 1.72, -0.01))
	Kit.cilindro(_corpo, Vector2(0.125, 0.155), 0.14, cor, Vector3(0, 1.8, -0.01))
	Kit.cilindro(_corpo, Vector2(0.156, 0.156), 0.03, cor.darkened(0.5), Vector3(0, 1.745, -0.01))
