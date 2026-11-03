#!/usr/bin/env python3
"""Valida data/linha_do_tempo.json (se existir) contra schemas/linha_do_tempo.schema.json.

- esquema (erro); ids únicos (erro); `data_fim` >= `data` (erro);
- `fontes` existem no catálogo data/fontes/*.json (erro); `verbete` existe (aviso; erro com --estrito);
- vocabulários da taxonomia em temas/ritos/potencias/periodos (aviso);
- lista de alerta de conteúdo ritual (erro/aviso) e citação entre aspas de 15+ palavras (erro);
- eventos fora de ordem cronológica no arquivo (aviso: o site ordena sozinho).

Uso: python3 scripts/validar_linha_do_tempo.py [--estrito] [--raiz DIR]
Sem o arquivo, passa (nada a validar). Sai com código 1 se houver erro.
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
    lt = projeto.linha_do_tempo(raiz)
    if lt is None:
        print("data/linha_do_tempo.json não existe: nada a validar. OK")
        return 0
    try:
        import jsonschema
        esq = json.loads((Path(raiz) / "schemas" / "linha_do_tempo.schema.json").read_text(encoding="utf-8"))
        for e in jsonschema.Draft202012Validator(esq).iter_errors(lt):
            erros.append(f"{'/'.join(map(str, e.path)) or '(raiz)'} {e.message}")
    except ImportError:
        avisos.append("jsonschema não instalado: checagem de esquema mínima")
    cat = projeto.fontes_por_id(raiz)
    verb = {v["fm"].get("id") for v in projeto.verbetes(raiz) if v["fm"]}
    V = projeto.vocab(raiz)
    alerta = Alerta()
    evs = lt.get("eventos", []) if isinstance(lt, dict) else []
    for i, c in Counter(e.get("id") for e in evs).items():
        if c > 1:
            erros.append(f"id de evento duplicado ({c}x): {i}")
    anterior = None
    for e in evs:
        rot = f"evento {e.get('id', '?')}"
        try:
            k, kf = chave_data(e.get("data")), chave_data(e.get("data_fim"))
        except (ValueError, TypeError):
            erros.append(f"{rot}: data inválida")
            continue
        if kf and k and kf < k:
            erros.append(f"{rot}: data_fim anterior a data")
        if anterior and k and k < anterior:
            avisos.append(f"{rot}: fora de ordem cronológica no arquivo")
        anterior = k or anterior
        for s in e.get("fontes", []):
            if s not in cat:
                erros.append(f"{rot}: fonte '{s}' não existe no catálogo")
        if e.get("verbete") and e["verbete"] not in verb:
            ref_erro.append(f"{rot}: verbete '{e['verbete']}' não existe (ainda)")
        for campo in ("temas", "ritos", "potencias", "periodos"):
            for c in e.get(campo) or []:
                if not projeto.codigo_conhecido(c, V):
                    avisos.append(f"{rot}: {campo} '{c}' fora da taxonomia")
        texto = " ".join(str(e.get(x) or "") for x in ("titulo", "resumo", "divergencia"))
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
    print(json.dumps({"eventos": len(evs), "erros": len(erros), "avisos": len(avisos)}, ensure_ascii=False))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
