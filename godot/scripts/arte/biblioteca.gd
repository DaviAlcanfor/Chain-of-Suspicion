extends Node3D
## Biblioteca da Mansão Villaça: estantes até o teto, lareira apagada e
## poltronas de couro. As paredes x = -5 e z = -4 são as do fundo do corte.

const LARGURA := 10.0
const FUNDO_Z := 8.0
const ALTURA := 3.3

const TABUA := Color("5a3a22")
const MADEIRA := Color("3b2415")
const MADEIRA_CLARA := Color("6d4526")
const PAPEL_DE_PAREDE := Color("3e4a3a")
const CORTE := Color("b9ad96")
const COURO := Color("5b2e17")
const PEDRA := Color("6b655c")
const LATAO := Color("b48a3a")
const PAPEL := Color("d8cfb8")
const CAPAS: Array[Color] = [
	Color("5b1f22"), Color("23364f"), Color("2f4a38"), Color("6b4a1f"),
	Color("3a2a3f"), Color("7a6a4a"), Color("1e2026"), Color("54402f"),
]

var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	_rng.seed = 7
	Kit.palco(self)
	_montar_casca()
	_montar_estantes()
	_montar_lareira()
	_montar_janela()
	_montar_porta()
	_montar_tapete()
	_montar_poltronas()
	_montar_escrivaninha()
	_montar_bagunca()
	_montar_luzes()
	_marcar_pontos()


func _montar_casca() -> void:
	Kit.caixa(self, Vector3(LARGURA + 0.5, 0.6, FUNDO_Z + 0.5), Color("17151a"), Vector3(0, -0.34, 0))
	var tabuas := 27
	for i in tabuas:
		var z := -FUNDO_Z / 2.0 + (i + 0.5) * FUNDO_Z / tabuas
		var cor := TABUA.darkened(_rng.randf_range(0.0, 0.22))
		Kit.caixa(self, Vector3(LARGURA, 0.06, FUNDO_Z / tabuas - 0.008), cor, Vector3(0, -0.03, z))
	_parede(Vector3(0.2, ALTURA, FUNDO_Z + 0.2), Vector3(-LARGURA / 2.0 - 0.1, ALTURA / 2.0, 0))
	_parede(Vector3(LARGURA + 0.4, ALTURA, 0.2), Vector3(0, ALTURA / 2.0, -FUNDO_Z / 2.0 - 0.1))
	Kit.caixa(self, Vector3(0.06, 1.0, FUNDO_Z), MADEIRA, Vector3(-LARGURA / 2.0 + 0.03, 0.5, 0))
	Kit.caixa(self, Vector3(LARGURA, 1.0, 0.06), MADEIRA, Vector3(0, 0.5, -FUNDO_Z / 2.0 + 0.03))


func _parede(tamanho: Vector3, pos: Vector3) -> void:
	Kit.caixa(self, tamanho, PAPEL_DE_PAREDE, pos)
	Kit.caixa(self, Vector3(tamanho.x, 0.02, tamanho.z), CORTE, Vector3(pos.x, ALTURA + 0.01, pos.z))


func _montar_estantes() -> void:
	_estante(Vector3(-4.7, 0, -3.72), Vector2(5.2, 0))
	_estante(Vector3(-4.72, 0, -2.42), Vector2(2.1, PI / 2.0))
	_estante(Vector3(-4.72, 0, 2.65), Vector2(2.6, PI / 2.0))


## `forma.x` é a largura e `forma.y` o giro em torno de Y.
func _estante(pos: Vector3, forma: Vector2) -> void:
	var movel := Node3D.new()
	movel.position = pos
	movel.rotation.y = forma.y
	add_child(movel)
	var largura := forma.x
	var meio := largura / 2.0 if forma.y == 0.0 else 0.0
	var prateleiras := 7
	var vao := (ALTURA - 0.1) / prateleiras
	Kit.caixa(movel, Vector3(largura, ALTURA, 0.04), MADEIRA.darkened(0.4), Vector3(meio, ALTURA / 2.0, -0.2))
	for lado: float in [-0.5, 0.5]:
		Kit.caixa(movel, Vector3(0.08, ALTURA, 0.44), MADEIRA, Vector3(meio + lado * largura, ALTURA / 2.0, 0))
	for i in prateleiras + 1:
		Kit.caixa(movel, Vector3(largura, 0.05, 0.44), MADEIRA, Vector3(meio, i * vao + 0.03, 0))
		if i < prateleiras:
			_livros(movel, Vector3(meio - largura / 2.0 + 0.08, i * vao + 0.055, 0), largura - 0.16)


func _livros(movel: Node3D, inicio: Vector3, largura: float) -> void:
	var x := 0.0
	while x < largura - 0.12:
		var espessura := _rng.randf_range(0.05, 0.12)
		if _rng.randf() < 0.08:
			x += _rng.randf_range(0.15, 0.4)
			continue
		var altura := _rng.randf_range(0.25, 0.38)
		var cor: Color = CAPAS[_rng.randi() % CAPAS.size()]
		var livro := Kit.caixa(movel, Vector3(espessura, altura, 0.3), cor, inicio + Vector3(x + espessura / 2.0, altura / 2.0, 0.02))
		if _rng.randf() < 0.05:
			livro.rotation.z = -0.25
		x += espessura + 0.004


func _montar_lareira() -> void:
	var z := 0.0
	var x := -4.72
	Kit.caixa(self, Vector3(0.5, 1.5, 0.45), PEDRA, Vector3(x, 0.75, z - 0.95))
	Kit.caixa(self, Vector3(0.5, 1.5, 0.45), PEDRA, Vector3(x, 0.75, z + 0.95))
	Kit.caixa(self, Vector3(0.5, 0.4, 2.35), PEDRA, Vector3(x, 1.3, z))
	Kit.caixa(self, Vector3(0.1, 1.1, 1.5), Color("0e0d10"), Vector3(x - 0.15, 0.55, z))
	Kit.caixa(self, Vector3(0.7, 0.1, 2.6), MADEIRA_CLARA, Vector3(x + 0.1, 1.55, z))
	Kit.caixa(self, Vector3(0.95, 0.06, 2.6), PEDRA.darkened(0.25), Vector3(x + 0.2, 0.03, z))
	for i in 3:
		var tora := Kit.cilindro(self, Vector2(0.07, 0.07), 0.9, Color("241912"), Vector3(x + 0.05, 0.1 + 0.11 * float(i == 2), z - 0.1 + i * 0.12))
		tora.rotation.x = PI / 2.0
	Kit.caixa(self, Vector3(0.14, 0.34, 0.26), MADEIRA, Vector3(x + 0.05, 1.77, z))
	Kit.cilindro(self, Vector2(0.07, 0.07), 0.02, PAPEL, Vector3(x + 0.13, 1.8, z)).rotation.z = PI / 2.0
	Kit.cilindro(self, Vector2(0.04, 0.05), 0.24, LATAO, Vector3(x + 0.05, 1.72, z - 0.9))
	Kit.cilindro(self, Vector2(0.04, 0.05), 0.24, LATAO, Vector3(x + 0.05, 1.72, z + 0.9))
	_quadro_na_parede(Vector3(-4.97, 2.5, z), Vector2(1.5, 1.0))


func _quadro_na_parede(pos: Vector3, tamanho: Vector2) -> void:
	Kit.caixa(self, Vector3(0.05, tamanho.y, tamanho.x), LATAO.darkened(0.3), pos)
	Kit.caixa(self, Vector3(0.02, tamanho.y - 0.16, tamanho.x - 0.16), Color("2a2f36"), pos + Vector3(0.03, 0, 0))
	Kit.esfera(self, 0.16, Color("c9b08c"), pos + Vector3(0.0, 0.06, 0)).scale.x = 0.25
	Kit.cilindro(self, Vector2(0.1, 0.28), 0.35, Color("20181c"), pos + Vector3(0.0, -0.22, 0)).scale.x = 0.2


func _montar_janela() -> void:
	var x := 2.5
	var z := -3.98
	Kit.caixa(self, Vector3(1.6, 2.2, 0.04), Kit.FUNDO, Vector3(x, 1.75, z))
	var vidro := Kit.caixa(self, Vector3(1.4, 2.0, 0.02), Color.WHITE, Vector3(x, 1.75, z + 0.03))
	vidro.material_override = Kit.emissivo(Color("3a5f9a"), 0.45)
	for dx: float in [-0.75, 0.0, 0.75]:
		Kit.caixa(self, Vector3(0.07, 2.2, 0.06), MADEIRA, Vector3(x + dx, 1.75, z + 0.05))
	for y: float in [0.65, 1.75, 2.85]:
		Kit.caixa(self, Vector3(1.57, 0.07, 0.06), MADEIRA, Vector3(x, y, z + 0.05))
	Kit.caixa(self, Vector3(2.5, 0.08, 0.1), LATAO, Vector3(x, 2.98, z + 0.14))
	for lado: float in [-1.0, 1.0]:
		for i in 4:
			var dobra := Kit.cilindro(self, Vector2(0.07, 0.09), 2.8, Color("4c1a22"), Vector3(x + lado * (0.95 + i * 0.1), 1.56, z + 0.14))
			dobra.scale.z = 0.7


func _montar_porta() -> void:
	var x := 4.3
	var z := -3.96
	Kit.caixa(self, Vector3(1.2, 2.4, 0.06), MADEIRA, Vector3(x, 1.2, z))
	Kit.caixa(self, Vector3(1.02, 2.3, 0.04), MADEIRA_CLARA.darkened(0.25), Vector3(x, 1.15, z + 0.03))
	for y: float in [0.65, 1.7]:
		Kit.caixa(self, Vector3(0.76, 0.85, 0.02), MADEIRA_CLARA.darkened(0.45), Vector3(x, y, z + 0.06))
	Kit.esfera(self, 0.05, LATAO, Vector3(x - 0.38, 1.1, z + 0.1))


func _montar_tapete() -> void:
	var centro := Vector3(-0.8, 0.012, 0.6)
	Kit.caixa(self, Vector3(5.6, 0.02, 4.8), Color("15352c"), centro)
	Kit.caixa(self, Vector3(5.2, 0.024, 4.4), Color("a68340"), centro)
	Kit.caixa(self, Vector3(5.0, 0.028, 4.2), Color("1f4a3d"), centro)
	Kit.caixa(self, Vector3(3.6, 0.032, 2.8), Color("183a30"), centro)


func _montar_poltronas() -> void:
	_poltrona(Vector3(-2.7, 0, -1.6), -0.9)
	_poltrona(Vector3(-2.7, 0, 1.55), -2.23)
	var mesa := Vector3(-3.3, 0, 0)
	Kit.cilindro(self, Vector2(0.03, 0.04), 0.65, MADEIRA, mesa + Vector3(0, 0.33, 0))
	Kit.cilindro(self, Vector2(0.2, 0.2), 0.03, MADEIRA_CLARA, mesa + Vector3(0, 0.65, 0))
	Kit.cilindro(self, Vector2(0.15, 0.15), 0.03, MADEIRA, mesa + Vector3(0, 0.02, 0))
	_abajur(Vector3(-4.05, 0, 2.5))


func _poltrona(pos: Vector3, giro: float) -> void:
	var movel := Node3D.new()
	movel.position = pos
	movel.rotation.y = giro
	add_child(movel)
	Kit.caixa(movel, Vector3(0.9, 0.38, 0.8), COURO, Vector3(0, 0.27, 0))
	Kit.caixa(movel, Vector3(0.72, 0.1, 0.66), COURO.lightened(0.1), Vector3(0, 0.5, 0.05))
	Kit.caixa(movel, Vector3(0.9, 0.85, 0.18), COURO, Vector3(0, 0.62, -0.36))
	for lado: float in [-1.0, 1.0]:
		Kit.caixa(movel, Vector3(0.16, 0.55, 0.8), COURO.darkened(0.12), Vector3(lado * 0.42, 0.45, 0))
		Kit.caixa(movel, Vector3(0.06, 0.08, 0.06), Color("120c08"), Vector3(lado * 0.38, 0.04, 0.32))
		Kit.caixa(movel, Vector3(0.06, 0.08, 0.06), Color("120c08"), Vector3(lado * 0.38, 0.04, -0.32))


func _abajur(pos: Vector3) -> void:
	Kit.cilindro(self, Vector2(0.15, 0.18), 0.03, LATAO.darkened(0.3), pos + Vector3(0, 0.02, 0))
	Kit.cilindro(self, Vector2(0.018, 0.018), 1.55, LATAO.darkened(0.3), pos + Vector3(0, 0.8, 0))
	var cupula := Kit.cilindro(self, Vector2(0.15, 0.27), 0.3, Color.WHITE, pos + Vector3(0, 1.6, 0))
	cupula.material_override = Kit.emissivo(Color("ffb35a"), 1.6)


func _montar_escrivaninha() -> void:
	var movel := Node3D.new()
	movel.position = Vector3(3.2, 0, 2.2)
	movel.rotation.y = -0.5
	add_child(movel)
	Kit.caixa(movel, Vector3(1.9, 0.08, 1.0), MADEIRA_CLARA, Vector3(0, 0.76, 0))
	for lado: float in [-1.0, 1.0]:
		Kit.caixa(movel, Vector3(0.5, 0.72, 0.9), MADEIRA, Vector3(lado * 0.68, 0.36, 0))
		Kit.esfera(movel, 0.022, LATAO, Vector3(lado * 0.68, 0.5, 0.46))
	Kit.caixa(movel, Vector3(0.75, 0.01, 0.5), Color("1f4a3d"), Vector3(0, 0.805, 0.05))
	for i in 5:
		var folha := Kit.caixa(movel, Vector3(0.22, 0.012, 0.3), PAPEL, Vector3(-0.45 + _rng.randf() * 0.2, 0.81 + i * 0.012, 0.15 - _rng.randf() * 0.2))
		folha.rotation.y = _rng.randf_range(-0.4, 0.4)
	Kit.cilindro(movel, Vector2(0.06, 0.08), 0.03, LATAO, Vector3(0.6, 0.815, -0.2))
	Kit.cilindro(movel, Vector2(0.012, 0.012), 0.3, LATAO, Vector3(0.6, 0.97, -0.2))
	var cupula := Kit.caixa(movel, Vector3(0.36, 0.09, 0.14), Color.WHITE, Vector3(0.6, 1.14, -0.15))
	cupula.material_override = Kit.emissivo(Color("3fae76"), 1.8)
	Kit.caixa(movel, Vector3(0.5, 0.42, 0.5), COURO.darkened(0.35), Vector3(0, 0.48, -0.85))
	Kit.caixa(movel, Vector3(0.5, 0.7, 0.08), COURO.darkened(0.35), Vector3(0, 0.95, -1.08))
	Kit.cilindro(movel, Vector2(0.04, 0.07), 0.42, COURO.darkened(0.6), Vector3(0, 0.2, -0.85))


func _montar_bagunca() -> void:
	_globo(Vector3(4.15, 0, -2.6))
	_escada(Vector3(-0.4, 0, -3.25))
	_pilha(Vector3(0.9, 0, -2.95), 6)
	_pilha(Vector3(-1.9, 0, -3.1), 4)
	_pilha(Vector3(1.55, 0, 3.0), 5)
	_folhas(Vector3(0.2, 0, 2.4), 7)
	_folhas(Vector3(2.0, 0, 0.3), 4)
	_vaso(Vector3(4.45, 0, -0.75))
	var mesa := Vector3(-3.3, 0.665, 0)
	var taca := Kit.cilindro(self, Vector2(0.04, 0.012), 0.08, Color("aeb9c2"), mesa + Vector3(0.04, 0.08, 0.03))
	taca.material_override = Kit.emissivo(Color("9fb0bb"), 0.3)
	Kit.cilindro(self, Vector2(0.006, 0.006), 0.07, Color("aeb9c2"), mesa + Vector3(0.04, 0.03, 0.03))
	Kit.caixa(self, Vector3(0.1, 0.03, 0.14), CAPAS[0], mesa + Vector3(-0.08, 0.02, -0.04))


func _globo(pos: Vector3) -> void:
	Kit.cilindro(self, Vector2(0.02, 0.2), 0.5, MADEIRA, pos + Vector3(0, 0.25, 0))
	Kit.esfera(self, 0.3, Color("6d7f5e"), pos + Vector3(0, 0.82, 0))
	Kit.anel(self, 0.36, LATAO, pos + Vector3(0, 0.82, 0)).rotation.x = PI / 2.0


func _escada(pos: Vector3) -> void:
	for lado: float in [-0.25, 0.25]:
		var trave := Kit.caixa(self, Vector3(0.05, 3.0, 0.05), MADEIRA_CLARA, pos + Vector3(lado, 1.45, 0))
		trave.rotation.x = 0.18
	for i in 9:
		var y := 0.3 + i * 0.3
		Kit.caixa(self, Vector3(0.5, 0.035, 0.08), MADEIRA_CLARA, pos + Vector3(0, y, 0.27 - y * 0.18))


func _pilha(pos: Vector3, quantos: int) -> void:
	for i in quantos:
		var livro := Kit.caixa(self, Vector3(0.36, 0.06, 0.26), CAPAS[_rng.randi() % CAPAS.size()], pos + Vector3(0, 0.03 + i * 0.062, 0))
		livro.rotation.y = _rng.randf_range(-0.5, 0.5)


func _folhas(pos: Vector3, quantas: int) -> void:
	for i in quantas:
		var deslocamento := Vector3(_rng.randf_range(-0.6, 0.6), 0.036, _rng.randf_range(-0.5, 0.5))
		var folha := Kit.caixa(self, Vector3(0.22, 0.004, 0.3), PAPEL, pos + deslocamento)
		folha.rotation.y = _rng.randf_range(-PI, PI)


func _vaso(pos: Vector3) -> void:
	Kit.cilindro(self, Vector2(0.22, 0.15), 0.4, Color("4a2f24"), pos + Vector3(0, 0.2, 0))
	for i in 7:
		var angulo := i * TAU / 7.0
		var folha := Kit.capsula(self, 0.05, 0.75, Color("223f2b"), pos + Vector3(cos(angulo) * 0.17, 0.72, sin(angulo) * 0.17))
		folha.rotation = Vector3(sin(angulo) * 0.45, 0, -cos(angulo) * 0.45)


func _montar_luzes() -> void:
	Kit.luz(self, Color("ffb066"), Vector3(-3.85, 1.95, 2.25), Vector2(3.4, 8.0))
	Kit.luz(self, Color("9fe0a8"), Vector3(3.3, 1.5, 1.7), Vector2(1.5, 3.8))
	Kit.luz(self, Color("6d90d8"), Vector3(2.5, 2.0, -2.8), Vector2(1.8, 6.0))
	var ceu := DirectionalLight3D.new()
	ceu.light_color = Color("7c8fc4")
	ceu.light_energy = 0.32
	ceu.rotation_degrees = Vector3(-62, 25, 0)
	ceu.shadow_enabled = true
	add_child(ceu)


func _marcar_pontos() -> void:
	var pontos := Node3D.new()
	pontos.name = "pontos"
	add_child(pontos)
	var lugares := {
		"porta": Vector3(4.3, 0, -3.1),
		"janela": Vector3(2.5, 0, -2.6),
		"lareira": Vector3(-3.55, 0, -1.1),
		"corpo": Vector3(-0.9, 0, 0.5),
		"junto_ao_corpo": Vector3(0.2, 0, 1.6),
		"mesa": Vector3(-2.6, 0, 0.6),
		"centro": Vector3(0.8, 0, -0.6),
		"escrivaninha": Vector3(1.9, 0, 0.7),
	}
	for nome: String in lugares:
		var ponto := Marker3D.new()
		ponto.name = nome
		ponto.position = lugares[nome]
		pontos.add_child(ponto)
