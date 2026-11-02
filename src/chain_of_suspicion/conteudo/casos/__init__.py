from ..caso_pronto import CasoPronto, ChaveCaso
from . import (
    a_ultima_danca,
    nevasca_na_pousada,
    o_testamento,
    sangue_no_conves,
    veneno_na_biblioteca,
)

CATALOGO: dict[ChaveCaso, CasoPronto] = {
    caso.chave: caso
    for caso in (
        veneno_na_biblioteca.construir(),
        o_testamento.construir(),
        a_ultima_danca.construir(),
        sangue_no_conves.construir(),
        nevasca_na_pousada.construir(),
    )
}
