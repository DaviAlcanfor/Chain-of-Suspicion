// Pós-produção da tela inteira: linhas de tinta onde a profundidade ou a
// direção da superfície mudam, e um escurecimento nas bordas.
shader_type spatial;
render_mode unshaded, depth_test_disabled, depth_draw_never, cull_disabled, fog_disabled, shadows_disabled;

uniform sampler2D tela : hint_screen_texture, filter_nearest;
uniform sampler2D profundidade : hint_depth_texture, filter_nearest;
uniform sampler2D normais : hint_normal_roughness_texture, filter_nearest;
uniform vec3 tinta = vec3(0.012, 0.01, 0.018);
uniform float espessura = 1.0;
uniform float limite_normal = 0.75;
uniform float limite_distancia = 0.14;
uniform float alcance = 100.0;
uniform float vinheta = 0.55;

void vertex() {
	POSITION = vec4(VERTEX.xy, 1.0, 1.0);
}

void fragment() {
	vec2 passo = espessura / VIEWPORT_SIZE;
	vec2 vizinhos[4] = { vec2(passo.x, 0.0), vec2(-passo.x, 0.0), vec2(0.0, passo.y), vec2(0.0, -passo.y) };
	float centro = texture(profundidade, SCREEN_UV).r;
	vec3 normal = texture(normais, SCREEN_UV).rgb;
	float dist = 0.0;
	float vira = 0.0;
	for (int i = 0; i < 4; i++) {
		vec2 uv = SCREEN_UV + vizinhos[i];
		dist = max(dist, abs(texture(profundidade, uv).r - centro) * alcance);
		vira = max(vira, distance(texture(normais, uv).rgb, normal));
	}
	float linha = max(smoothstep(limite_distancia, limite_distancia * 1.6, dist), smoothstep(limite_normal, limite_normal * 1.4, vira) * step(0.00001, centro));
	vec3 cor = mix(texture(tela, SCREEN_UV).rgb, tinta, linha * 0.92);
	float borda = length(SCREEN_UV - 0.5) * 1.414;
	ALBEDO = cor * (1.0 - vinheta * smoothstep(0.55, 1.0, borda));
}
