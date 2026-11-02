#!/usr/bin/env python3
"""Valida o catálogo de fontes fragmentado em data/fontes/<lote>.json.

- Esquema (schemas/fonte.schema.json) via jsonschema, se instalado; senão checagem mínima.
- ids únicos entre TODOS os lotes (erro), títulos+ano parecidos em lotes diferentes (aviso).
- Vocabulários de docs/taxonomia.md: código desconhecido -> aviso.
- Estatísticas por lote, idioma, tema, status.

Uso:
  python3 scripts/validar_fontes.py              # valida e mostra números
  python3 scripts/validar_fontes.py --buscar anderson   # procura em id/título/autores de todos os lotes
  python3 scripts/validar_fontes.py --json       # números em JSON (para ESTADO.md)
Sai com código 1 se houver erro.
"""
import json, re, sys, unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "data" / "fontes"
ESQUEMA = json.loads((RAIZ / "schemas" / "fonte.schema.json").read_text())
OBRIG = ESQUEMA["required"]
PROPS = ESQUEMA["properties"]


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def vocab():
    """Extrai códigos `entre crases` de docs/taxonomia.md (aproximação suficiente para aviso)."""
    t = (RAIZ / "docs" / "taxonomia.md").read_text()
    return set(re.findall(r"`([a-z0-9_]+)`", t))


def carregar():
    lotes = {}
    for p in sorted(DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text())
        except Exception as e:
            print(f"ERRO {p.name}: JSON inválido: {e}")
            lotes[p.name] = None
            continue
        lotes[p.name] = d
    return lotes


def main():
    args = sys.argv[1:]
    lotes = carregar()
    todas = [(n, f) for n, d in lotes.items() if d for f in d.get("fontes", [])]
    if "--buscar" in args:
        termo = norm(args[args.index("--buscar") + 1])
        for n, f in todas:
            alvo = norm(" ".join([f.get("id", ""), f.get("titulo", ""), " ".join(f.get("autores", []))]))
            if termo in alvo:
                print(f"{n}: {f.get('id')} | {f.get('titulo')} ({f.get('ano')})")
        return 0
    erros, avisos = [], []
    if any(d is None for d in lotes.values()):
        erros.append("lote com JSON inválido")
    try:
        import jsonschema
        val = jsonschema.Draft202012Validator(ESQUEMA)
    except Exception:
        val = None
    V = vocab()
    ids = Counter(f.get("id") for _, f in todas)
    for i, c in ids.items():
        if c > 1:
            erros.append(f"id duplicado ({c}x): {i}")
    chave = {}
    for n, f in todas:
        fid = f.get("id", "?")
        if val:
            for e in val.iter_errors(f):
                erros.append(f"{n}:{fid}: {'/'.join(map(str, e.path))} {e.message}")
        else:
            for k in OBRIG:
                if k not in f:
                    erros.append(f"{n}:{fid}: falta {k}")
            for k in f:
                if k not in PROPS:
                    erros.append(f"{n}:{fid}: campo desconhecido {k}")
        for campo in ("temas", "ritos", "potencias", "periodos"):
            for c in f.get(campo, []) or []:
                if c not in V and not re.match(r"^(gl|go)_[a-z]{2,}$", c):
                    avisos.append(f"{n}:{fid}: {campo} '{c}' fora da taxonomia")
        if f.get("status_verificacao") in ("copiado", "fichado", "revisado") and not f.get("acervo"):
            avisos.append(f"{n}:{fid}: status {f['status_verificacao']} sem campo 'acervo'")
        k = (norm(f.get("titulo", ""))[:60], f.get("ano"))
        if k in chave and chave[k][0] != n:
            avisos.append(f"possível duplicata: {fid} ({n}) ~ {chave[k][1]} ({chave[k][0]})")
        chave.setdefault(k, (n, fid))
    stats = {
        "fontes": len(todas),
        "lotes": {n: len(d.get("fontes", [])) for n, d in lotes.items() if d},
        "idiomas": dict(Counter(f.get("idioma") for _, f in todas).most_common()),
        "status": dict(Counter(f.get("status_verificacao") for _, f in todas).most_common()),
        "acesso": dict(Counter(f.get("acesso") for _, f in todas).most_common()),
        "temas": dict(Counter(t for _, f in todas for t in f.get("temas", [])).most_common()),
        "erros": len(erros), "avisos": len(avisos),
    }
    if "--json" in args:
        print(json.dumps(stats, ensure_ascii=False, indent=1))
    else:
        for a in avisos[:200]:
            print("aviso:", a)
        for e in erros:
            print("ERRO:", e)
        print(json.dumps(stats, ensure_ascii=False))
        if not val:
            print("(jsonschema não instalado: checagem mínima; pip install jsonschema)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
