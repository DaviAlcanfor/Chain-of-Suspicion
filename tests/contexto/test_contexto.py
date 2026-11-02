import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CATALOGO = RAIZ / "docs" / "CATALOGO.md"
LIMITE_DE_LINHAS = 60
IGNORADOS = {".venv", ".git", ".claude", ".godot", "node_modules", "__pycache__"}


def _citados() -> list[Path]:
    links = re.findall(r"\]\(([^)]*AGENTS\.md)\)", CATALOGO.read_text(encoding="utf-8"))
    return [(CATALOGO.parent / link).resolve() for link in links]


def _existentes() -> set[Path]:
    return {
        p.resolve()
        for p in RAIZ.rglob("AGENTS.md")
        if not IGNORADOS & set(p.relative_to(RAIZ).parts)
    }


def test_todo_agents_md_existente_esta_no_catalogo_e_vice_versa() -> None:
    assert set(_citados()) == _existentes()


def test_cada_agents_md_tem_claude_md_irmao_que_o_importa() -> None:
    for agents in _citados():
        claude = agents.parent / "CLAUDE.md"
        assert claude.exists(), f"falta {claude.relative_to(RAIZ)}"
        assert claude.read_text(encoding="utf-8").strip() == "@AGENTS.md"


def test_cada_agents_md_cabe_no_limite_de_linhas() -> None:
    for agents in _citados():
        linhas = len(agents.read_text(encoding="utf-8").splitlines())
        assert linhas <= LIMITE_DE_LINHAS, f"{agents.relative_to(RAIZ)} tem {linhas} linhas"


def test_agents_md_da_raiz_manda_ler_o_catalogo() -> None:
    texto = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
    assert "docs/CATALOGO.md" in texto


def test_pastas_de_codigo_do_pacote_tem_contexto() -> None:
    pacote = RAIZ / "src" / "chain_of_suspicion"
    pastas = {p for p in pacote.iterdir() if p.is_dir() and p.name != "__pycache__"}
    sem_contexto = [p.name for p in pastas if not (p / "AGENTS.md").exists()]
    assert not sem_contexto, f"pastas sem AGENTS.md: {sem_contexto}"
