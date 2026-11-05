from pathlib import Path

from chain_of_suspicion.conteudo.documentacao import elenco_em_json, escrever

RAIZ = Path(__file__).resolve().parent.parent
PASTA_DOCS = RAIZ / "docs"
ELENCO_GODOT = RAIZ / "godot" / "dados" / "elenco.json"

if __name__ == "__main__":
    for arquivo in escrever(PASTA_DOCS):
        print(arquivo.relative_to(RAIZ))
    ELENCO_GODOT.write_text(elenco_em_json(), encoding="utf-8", newline="\n")
    print(ELENCO_GODOT.relative_to(RAIZ))
