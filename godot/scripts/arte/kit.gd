class_name Kit
extends RefCounted
## Formas simples, materiais foscos e o "palco" comum a toda sala:
## câmera isométrica, ambiente noturno, chuva ao fundo e traço de tinta.

const FUNDO := Color("080b16")

static var _materiais: Dictionary = {}


static func material(cor: Color) -> StandardMaterial3D:
	if not _materiais.has(cor):
		var m := StandardMaterial3D.new()
		m.albedo_color = cor
		m.roughness = 0.9
		m.metallic_specular = 0.1
		_materiais[cor] = m
	return _materiais[cor]


static func emissivo(cor: Color, energia: float) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = cor
	m.emission_enabled = true
	m.emission = cor
	m.emission_energy_multiplier = energia
	return m


static func peca(pai: Node3D, malha: Mesh, cor: Color, pos: Vector3) -> MeshInstance3D:
	var parte := MeshInstance3D.new()
	parte.mesh = malha
	parte.material_override = material(cor)
	parte.position = pos
	pai.add_child(parte)
	return parte


static func caixa(pai: Node3D, tamanho: Vector3, cor: Color, pos: Vector3) -> MeshInstance3D:
	var malha := BoxMesh.new()
	malha.size = tamanho
	return peca(pai, malha, cor, pos)


static func esfera(pai: Node3D, raio: float, cor: Color, pos: Vector3) -> MeshInstance3D:
	var malha := SphereMesh.new()
	malha.radius = raio
	malha.height = raio * 2.0
	malha.radial_segments = 16
	malha.rings = 10
	return peca(pai, malha, cor, pos)


## Tronco de cone: `raios.x` em cima, `raios.y` embaixo.
static func cilindro(pai: Node3D, raios: Vector2, altura: float, cor: Color, pos: Vector3) -> MeshInstance3D:
	var malha := CylinderMesh.new()
	malha.top_radius = raios.x
	malha.bottom_radius = raios.y
	malha.height = altura
	malha.radial_segments = 16
	return peca(pai, malha, cor, pos)


static func capsula(pai: Node3D, raio: float, altura: float, cor: Color, pos: Vector3) -> MeshInstance3D:
	var malha := CapsuleMesh.new()
	malha.radius = raio
	malha.height = maxf(altura, raio * 2.0)
	malha.radial_segments = 12
	malha.rings = 4
	return peca(pai, malha, cor, pos)


static func anel(pai: Node3D, raio: float, cor: Color, pos: Vector3) -> MeshInstance3D:
	var malha := TorusMesh.new()
	malha.inner_radius = raio * 0.82
	malha.outer_radius = raio
	malha.rings = 20
	malha.ring_segments = 6
	return peca(pai, malha, cor, pos)


static func luz(pai: Node3D, cor: Color, pos: Vector3, energia_alcance: Vector2) -> OmniLight3D:
	var l := OmniLight3D.new()
	l.light_color = cor
	l.position = pos
	l.light_energy = energia_alcance.x
	l.omni_range = energia_alcance.y
	l.omni_attenuation = 1.1
	l.shadow_enabled = true
	pai.add_child(l)
	return l


static func palco(sala: Node3D) -> void:
	sala.add_child(_camera())
	sala.add_child(_ambiente())
	sala.add_child(_chuva())
	sala.add_child(_traco_de_tinta())


static func _camera() -> Camera3D:
	var camera := Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 11.8
	camera.far = 100.0
	camera.position = Vector3(20, 21.3, 20)
	camera.rotation_degrees = Vector3(-35.264, 45, 0)
	return camera


static func _ambiente() -> WorldEnvironment:
	var ambiente := Environment.new()
	ambiente.background_mode = Environment.BG_COLOR
	ambiente.background_color = FUNDO
	ambiente.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	ambiente.ambient_light_color = Color("3d4a78")
	ambiente.ambient_light_energy = 0.55
	ambiente.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	ambiente.ssao_enabled = true
	ambiente.ssao_radius = 0.8
	ambiente.ssao_intensity = 2.5
	ambiente.glow_enabled = true
	ambiente.glow_intensity = 0.5
	ambiente.glow_bloom = 0.04
	var mundo := WorldEnvironment.new()
	mundo.environment = ambiente
	return mundo


## A chuva cai atrás e abaixo da sala; ela nunca passa pela frente do corte.
static func _chuva() -> CPUParticles3D:
	var pingo := BoxMesh.new()
	pingo.size = Vector3(0.018, 0.34, 0.018)
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.albedo_color = Color(0.55, 0.65, 0.9, 0.3)
	m.render_priority = 110 # depois do traço de tinta, que apagaria o transparente
	pingo.material = m
	var chuva := CPUParticles3D.new()
	chuva.mesh = pingo
	chuva.amount = 500
	chuva.lifetime = 1.2
	chuva.preprocess = 1.2
	chuva.position = Vector3(-14, -11, -14)
	chuva.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
	chuva.emission_box_extents = Vector3(10, 10, 10)
	chuva.direction = Vector3.DOWN
	chuva.spread = 0.0
	chuva.gravity = Vector3.ZERO
	chuva.initial_velocity_min = 13.0
	chuva.initial_velocity_max = 16.0
	return chuva


static func _traco_de_tinta() -> MeshInstance3D:
	var quadro := QuadMesh.new()
	quadro.size = Vector2(2, 2)
	var m := ShaderMaterial.new()
	m.shader = load("res://shaders/tinta.gdshader")
	m.render_priority = 100
	var tela := MeshInstance3D.new()
	tela.mesh = quadro
	tela.material_override = m
	tela.extra_cull_margin = 16384.0
	tela.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return tela
