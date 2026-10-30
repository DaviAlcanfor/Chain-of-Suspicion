# 0002 — Godot como cliente 3D

- Status: aceita

## Contexto

Quero um mundo 3D em que os personagens se movam e, no futuro, um humano ande. Alternativa considerada: Three.js no navegador.

## Decisão

Godot 4, com GDScript. O cliente conversa com o backend por HTTP (`HTTPRequest`) e WebSocket (`WebSocketPeer`), ambos nativos.

## Consequências

- Motor de jogo completo (cena, física, câmera, iluminação) sem montar do zero.
- Curva de aprendizado nova; mitigada pela fase 0 pequena da spec 006.
- Three.js continuaria possível como segundo cliente, já que a API é o contrato.
- Exportar para web é possível, mas não é requisito.
