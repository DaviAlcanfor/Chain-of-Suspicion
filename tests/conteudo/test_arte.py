from pathlib import Path

from chain_of_suspicion.conteudo.documentacao import elenco_em_json
from chain_of_suspicion.conteudo.elenco import ELENCO

GODOT = Path(__file__).resolve().parents[2] / "godot"


def test_elenco_do_godot_nao_diverge_dos_dados() -> None:
    gravado = (GODOT / "dados" / "elenco.json").read_text(encoding="utf-8")
    assert gravado.replace("\r\n", "\n") == elenco_em_json(), "rode `just docs`"


def test_toda_persona_tem_cena_que_aponta_para_a_propria_chave() -> None:
    for persona in ELENCO.values():
        cena = GODOT / persona.modelo_godot.removeprefix("res://")
        assert f'chave = "{persona.chave.value}"' in cena.read_text(encoding="utf-8")


def test_toda_aparencia_usada_no_elenco_tem_peca_no_personagem() -> None:
    script = (GODOT / "scripts" / "arte" / "personagem.gd").read_text(encoding="utf-8")
    for persona in ELENCO.values():
        a = persona.aparencia
        valores = [
            a.porte,
            a.pele,
            a.cabelo_cor,
            a.cabelo_estilo,
            a.pelos_faciais,
            a.roupa,
            *a.acessorios,
        ]
        faltando = [v.value for v in valores if f'"{v.value}"' not in script]
        assert not faltando, f"{persona.chave.value}: sem peça para {faltando}"
