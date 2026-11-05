// Cortiça procedural: manchas de ruído sobre marrom, escurecendo nas bordas.
shader_type canvas_item;

uniform vec3 clara = vec3(0.60, 0.43, 0.26);
uniform vec3 escura = vec3(0.30, 0.19, 0.10);
uniform float escala = 460.0;

float acaso(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float ruido(vec2 p) {
	vec2 i = floor(p);
	vec2 f = smoothstep(0.0, 1.0, fract(p));
	float baixo = mix(acaso(i), acaso(i + vec2(1.0, 0.0)), f.x);
	float alto = mix(acaso(i + vec2(0.0, 1.0)), acaso(i + vec2(1.0, 1.0)), f.x);
	return mix(baixo, alto, f.y);
}

void fragment() {
	vec2 p = UV * vec2(16.0 / 9.0, 1.0) * escala;
	float grao = ruido(p) * 0.6 + ruido(p * 0.37) * 0.4;
	vec3 cor = mix(escura, clara, smoothstep(0.2, 0.8, grao));
	float borda = length(UV - 0.5) * 1.414;
	COLOR = vec4(cor * (1.0 - 0.6 * smoothstep(0.45, 1.0, borda)), 1.0);
}
