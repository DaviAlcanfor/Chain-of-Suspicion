from pathlib import Path

from chain_of_suspicion.conteudo.documentacao import escrever

PASTA_DOCS = Path(__file__).resolve().parent.parent / "docs"

if __name__ == "__main__":
    for arquivo in escrever(PASTA_DOCS):
        print(arquivo.relative_to(PASTA_DOCS.parent))
