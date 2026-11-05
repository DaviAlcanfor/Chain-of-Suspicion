// Polaroide: preto e branco com contraste alto e um leve tom de papel velho.
shader_type canvas_item;

void fragment() {
	float luz = dot(texture(TEXTURE, UV).rgb, vec3(0.3, 0.59, 0.11));
	luz = smoothstep(0.08, 0.85, luz);
	COLOR = vec4(luz * vec3(1.0, 0.96, 0.88), 1.0);
}
