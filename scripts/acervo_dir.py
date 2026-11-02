"""Localiza o acervo de texto integral das fontes (uso interno de pesquisa).

Ordem: variável de ambiente `ACERVO_DIR`; senão o clone do repositório PRIVADO
`aureliosaraiva/fontes-maconaria` em `../fontes-maconaria` (irmão deste repositório), se
existir; senão `acervo/` local deste repositório (ignorado pelo git, que é público).
"""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXTERNO = RAIZ.parent / "fontes-maconaria"
LOCAL = RAIZ / "acervo"


def acervo_padrao():
    env = os.environ.get("ACERVO_DIR")
    if env:
        return Path(env).expanduser().resolve()
    if EXTERNO.is_dir():
        return EXTERNO.resolve()
    return LOCAL.resolve()
