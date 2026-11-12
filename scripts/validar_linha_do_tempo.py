#!/usr/bin/env python3
"""Valida a linha do tempo fragmentada: data/linha_do_tempo/<ID>.json (um por sessão) e o
legado data/linha_do_tempo.json, se existir. Esquema: schemas/linha_do_tempo.schema.json.

- cada fragmento: JSON válido e conforme o esquema (erro);
- ids únicos entre todos os fragmentos (erro; evento sem `id` recebe '<arquivo>-<n>');
- `data` no formato ano / AAAA-MM / AAAA-MM-DD; `data_fim` >= `data` (erro);
  `precisao` coerente com a data (aviso: 'dia' sem dia, 'mes' sem mês);
- `fontes` existem no catálogo data/fontes/*.json (erro); `verbete` existe (aviso; erro com --estrito);
- vocabulários da taxonomia em temas/ritos/potencias/periodos (aviso);
- lista de alerta de conteúdo ritual (erro/aviso) e citação entre aspas de 15+ palavras (erro);
- mesmo título e data em fragmentos diferentes (aviso: possível duplicata entre sessões).

Uso: python3 scripts/validar_linha_do_tempo.py [--estrito] [--raiz DIR]
Sem fragmentos, passa. Sai com código 1 se houver erro.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import projeto  # noqa: E402
from alerta_ritual import Alerta  # noqa: E402

ASPAS = re.compile(r"[\"“”«»]([^\"“”«»\n]{3,})[\"“”«»]")


def chave_data(d):
    """Data (int ou 'AAAA[-MM[-DD]]') -> tupla ordenável."""
    if d is None:
        return None
    if isinstance(d, int):
        return (d, 0, 0)
    s = str(d)
    neg = s.startswith("-")
    partes = [int(x) for x in s.lstrip("-").split("-")]
    partes[0] = -partes[0] if neg else partes[0]
    return tuple(partes + [0] * (3 - len(partes)))


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    raiz = Path(args[args.index("--raiz") + 1]) if "--raiz" in args else projeto.RAIZ
    estrito = "--estrito" in args
    erros, avisos = [], []
    ref_erro = erros if estrito else avisos
    arqs = projeto.arquivos_linha_do_tempo(raiz)
    if not arqs:
        print("nenhum fragmento em data/linha_do_tempo/: nada a validar. OK")
        return 0
    try:
        import jsonschema
        esq = json.loads((projeto.RAIZ / "schemas" / "linha_do_tempo.schema.json").read_text(encoding="utf-8"))
        val = jsonschema.Draft202012Validator(esq)
    except ImportError:
        val = None
        avisos.append("jsonschema não instalado: checagem de esquema mínima (pip install jsonschema)")
    for p in arqs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            erros.append(f"{p.name}: JSON inválido: {e}")
            continue
        if val:
            for e in val.iter_errors(d):
                erros.append(f"{p.name}: {'/'.join(map(str, e.path)) or '(raiz)'} {e.message}")
        elif not isinstance(d, dict) or not isinstance(d.get("eventos"), list):
            erros.append(f"{p.name}: esperado {{\"eventos\": [...]}}")
    lt = projeto.linha_do_tempo(raiz) or {"eventos": []}
    cat = projeto.fontes_por_id(raiz)
    verb = {v["fm"].get("id") for v in projeto.verbetes(raiz) if v["fm"]}
    V = projeto.vocab(raiz)
    alerta = Alerta()
    evs = lt["eventos"]
    for i, c in Counter(e["id"] for e in evs).items():
        if c > 1:
            erros.append(f"id de evento duplicado ({c}x): {i}")
    vistos = {}
    for e in evs:
        rot = f"{e['_arquivo']}:{e['id']}"
        try:
            k, kf = chave_data(e.get("data")), chave_data(e.get("data_fim"))
        except (ValueError, TypeError):
            erros.append(f"{rot}: data inválida: {e.get('data')!r}")
            continue
        if kf and k and kf < k:
            erros.append(f"{rot}: data_fim anterior a data")
        prec = e.get("precisao")
        if k and prec == "dia" and not k[2]:
            avisos.append(f"{rot}: precisao 'dia' mas a data não tem dia")
        if k and prec == "mes" and not k[1]:
            avisos.append(f"{rot}: precisao 'mes' mas a data não tem mês")
        for s in e.get("fontes", []) or []:
            if s not in cat:
                erros.append(f"{rot}: fonte '{s}' não existe no catálogo")
        if e.get("verbete") and e["verbete"] not in verb:
            ref_erro.append(f"{rot}: verbete '{e['verbete']}' não existe (ainda)")
        for campo in ("temas", "ritos", "potencias", "periodos"):
            for c in e.get(campo) or []:
                if isinstance(c, str) and not projeto.codigo_conhecido(c, V):
                    avisos.append(f"{rot}: {campo} '{c}' fora da taxonomia")
        chave = (projeto.norm(str(e.get("titulo", ""))), k)
        if chave in vistos and vistos[chave] != e["_arquivo"]:
            avisos.append(f"{rot}: mesmo título e data que um evento de {vistos[chave]} (duplicata entre sessões?)")
        vistos.setdefault(chave, e["_arquivo"])
        texto = " ".join(str(e.get(x) or "") for x in ("titulo", "resumo", "nota", "divergencia"))
        e_r, a_r = alerta.verificar(texto)
        for t in e_r:
            erros.append(f"{rot}: possível reprodução de conteúdo ritual reservado: “{t}”")
        if a_r:
            avisos.append(f"{rot}: menção a {', '.join(sorted(set(a_r)))} — conferir")
        for m in ASPAS.finditer(texto):
            if len(re.findall(r"\w+", m.group(1))) >= 15:
                erros.append(f"{rot}: citação entre aspas longa (regra 2)")
    for a in avisos:
        print("aviso:", a)
    for x in erros:
        print("ERRO:", x)
    print(json.dumps({"fragmentos": len(arqs), "eventos": len(evs), "erros": len(erros), "avisos": len(avisos)}, ensure_ascii=False))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
