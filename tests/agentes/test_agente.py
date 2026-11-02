from datetime import timedelta

from ajudas import VENENO, pessoa
from chain_of_suspicion.agentes.agente import AgenteEmDuasEtapas, FichaDoAgente
from chain_of_suspicion.agentes.contexto import montar_contexto
from chain_of_suspicion.agentes.turno import FalaGerada, PropostaDoAgente
from chain_of_suspicion.dominio.enums import TipoAcao
from chain_of_suspicion.dominio.ids import PersonagemId
from chain_of_suspicion.dominio.mundo import Mundo
from chain_of_suspicion.dominio.regras import VisaoPersonagem, visao_do_personagem
from chain_of_suspicion.infra.decisao.decisor import DecisorFalso
from chain_of_suspicion.infra.llm.falso import ProvedorFalso

MARTA = pessoa(VENENO, "Marta")
PAULO = pessoa(VENENO, "Paulo")
ALENCAR = pessoa(VENENO, "Inspetor Alencar")
FICHA = FichaDoAgente(sistema="SISTEMA", persona="PERSONA")


class EspiaoDeMentira(DecisorFalso):
    def __init__(self, acao: TipoAcao) -> None:
        super().__init__(acao, mentir=True)
        self.consultas = 0

    async def deve_mentir(self, estado: str) -> bool:
        self.consultas += 1
        return await super().deve_mentir(estado)


def _mundo() -> Mundo:
    caso = VENENO.caso
    mundo = Mundo.no_instante(caso, caso.crime.instante - timedelta(minutes=40))
    mundo.colocar(ALENCAR, VENENO.entrada)
    return mundo


async def _decidir(
    decisor: DecisorFalso,
    fala: ProvedorFalso,
    quem: PersonagemId,
    ajuste: dict[str, object] | None = None,
) -> PropostaDoAgente:
    mundo = _mundo()
    visao: VisaoPersonagem = visao_do_personagem(mundo.caso, quem)
    if ajuste:
        visao = visao.model_copy(update=ajuste)
    agente = AgenteEmDuasEtapas(decisor, fala, FICHA)
    return await agente.decidir(visao, montar_contexto(mundo, quem))


async def test_acao_sem_fala_nao_chama_o_llm() -> None:
    fala = ProvedorFalso()
    proposta = await _decidir(DecisorFalso(TipoAcao.MOVER), fala, MARTA)
    assert proposta.tipo == TipoAcao.MOVER
    assert proposta.alvo_local is not None
    assert proposta.fala is None
    assert fala.pedidos == []


async def test_acao_com_fala_chama_o_llm_uma_vez_com_a_decisao() -> None:
    fala = ProvedorFalso(FalaGerada(fala="Boa noite."))
    proposta = await _decidir(DecisorFalso(TipoAcao.CONVERSAR, mentir=True), fala, MARTA)
    assert proposta.tipo == TipoAcao.CONVERSAR
    assert proposta.alvo_personagem == "Paulo"
    assert proposta.fala == "Boa noite."
    assert len(fala.pedidos) == 1
    sistema, usuario = fala.pedidos[0]
    assert sistema.conteudo == "SISTEMA"
    assert "esconder a verdade" in usuario.conteudo


async def test_quem_tem_segredo_consulta_a_mentira() -> None:
    decisor = EspiaoDeMentira(TipoAcao.CONVERSAR)
    await _decidir(decisor, ProvedorFalso(FalaGerada(fala="oi")), PAULO)
    assert decisor.consultas == 1


async def test_inocente_sem_segredo_nao_consulta_a_mentira() -> None:
    decisor = EspiaoDeMentira(TipoAcao.CONVERSAR)
    sem_segredo = {"segredos": []}
    proposta = await _decidir(decisor, ProvedorFalso(FalaGerada(fala="oi")), PAULO, sem_segredo)
    assert proposta.fala == "oi"
    assert decisor.consultas == 0


async def test_acusar_nao_e_oferecido_ao_decisor() -> None:
    proposta = await _decidir(DecisorFalso(TipoAcao.ACUSAR), ProvedorFalso(), ALENCAR)
    assert proposta.tipo != TipoAcao.ACUSAR


async def test_acao_que_exige_alvo_inexistente_nao_e_oferecida() -> None:
    proposta = await _decidir(DecisorFalso(TipoAcao.CONVERSAR), ProvedorFalso(), ALENCAR)
    assert proposta.tipo != TipoAcao.CONVERSAR
