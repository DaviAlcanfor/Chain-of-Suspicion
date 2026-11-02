import pytest

from ajudas import settings_de_teste
from chain_of_suspicion.config.api_keys import APIKeySettings
from chain_of_suspicion.config.modelos_llm import ModeloDecisao, ModeloLLM
from chain_of_suspicion.config.perfis import PERFIL_POR_PAPEL
from chain_of_suspicion.config.precos import PRECO_DO_MODELO
from chain_of_suspicion.config.settings import Settings
from chain_of_suspicion.dominio.enums import Papel
from chain_of_suspicion.erros.codigos import ErrorCode
from chain_of_suspicion.erros.excecoes import ErroJogo


def test_ids_de_modelo_sao_os_do_gateway() -> None:
    assert ModeloLLM.GPT_6_LUNA == "openai/gpt-6-luna"
    assert ModeloLLM.CLAUDE_HAIKU == "anthropic/claude-haiku-5.5"
    assert ModeloDecisao.JEV == "typesafe-ai/jev"
    assert ModeloDecisao.D1_ULTRA == "liquid/d1-ultra"
    assert ModeloDecisao.GPT_6_LUNA_DECISIONS == "openai/gpt-6-luna-decisions"


def test_todo_papel_tem_perfil_e_todo_preco_tem_modelo() -> None:
    assert set(PERFIL_POR_PAPEL) == set(Papel)
    assert set(PRECO_DO_MODELO) <= {*ModeloLLM, *ModeloDecisao}


def test_uma_chave_so_define_se_o_gateway_esta_configurado() -> None:
    assert settings_de_teste("x").api_keys.configurada
    assert not settings_de_teste("").api_keys.configurada


def test_settings_agrupam_chaves_llm_e_jogo() -> None:
    cfg = settings_de_teste(passos_por_partida=7)
    assert isinstance(cfg, Settings)
    assert cfg.game.passos_por_partida == 7
    assert cfg.llm.modelo_decisao == ModeloDecisao.D1_ULTRA
    assert cfg.llm.url_do_gateway.startswith("https://ai-gateway.vercel.sh")


def test_chave_vem_da_variavel_de_ambiente(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "segredo")
    assert APIKeySettings(_env_file=None).ai_gateway_api_key.get_secret_value() == "segredo"  # type: ignore[call-arg]


def test_chave_nao_aparece_na_representacao() -> None:
    assert "chave-secreta" not in repr(settings_de_teste("chave-secreta"))


def test_erro_base_tem_codigo_interno() -> None:
    assert ErroJogo.codigo == ErrorCode.ERRO_INTERNO
