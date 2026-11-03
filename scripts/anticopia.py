#!/usr/bin/env python3
"""Detector anti-cópia (n-gramas), portado do mapadosorixas.

Regra do projeto (CLAUDE.md regra 2): no repositório público, paráfrase sempre; citação
literal só curta (≤ 2 frases), de obra em domínio público, entre aspas e com fonte.

Textos verificados (tudo o que o projeto redige e o site publica):
- verbetes data/verbetes/**/*.md: resumo + cada parágrafo do corpo, comparados com as
  fontes do front matter e com as citadas nas notas do parágrafo;
- data/linha_do_tempo.json: título, resumo e divergência de cada evento (fontes do evento);
- data/conexoes.json: nota de cada conexão;
- catálogo data/fontes/*.json: `resumo` de cada fonte, comparado com o texto da própria fonte.

Verificações:
1. Citação entre aspas com ≥ LIMITE_CITACAO palavras -> ERRO; ≥ 6 palavras -> aviso.
2. Com textos de referência (acervo privado: $ANTICOPIA_REFS, ou txt/ de $ACERVO_DIR /
   ../fontes-maconaria, ou acervo/txt local): qualquer sequência de N palavras (padrão 8)
   idêntica a um texto de referência -> ERRO. E cada texto é comparado só com as fontes que
   cita (`<source_id>.txt`): sequência de 6 a N-1 palavras igual -> aviso "redação próxima".
   Cada aviso deve ser reescrito ou justificado (nome próprio, título, lista, termo técnico).
3. Sequências formadas sobretudo por números/marcas de página não contam (são referência).

Uso: python3 scripts/anticopia.py [--n 8] [--raiz DIR] [--sem-catalogo]
     ANTICOPIA_REFS=/pasta/txt python3 scripts/anticopia.py
     ANTICOPIA_REFS= python3 scripts/anticopia.py        (sem referências)
Sai com código 1 se houver erro.
"""
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import projeto  # noqa: E402

LIMITE_CITACAO = 15
AVISO_CITACAO = 6
AVISO_FONTE = 6
HIFEN = re.compile(r"(\w)-[ \t]*\n\s*(\w)")
REF_TOKENS = {"p", "pp", "v", "vol", "n", "cf", "apud", "ed", "fl", "f", "nota", "cap", "s", "ss", "t", "art"}
ASPAS = re.compile(r"[\"“”«»]([^\"“”«»]{3,})[\"“”«»]")


def normalizar(t):
    return re.findall(r"\w+", unicodedata.normalize("NFC", t.lower()))


def ngramas(palavras, n):
    return {" ".join(palavras[i:i + n]) for i in range(len(palavras) - n + 1)}


def eh_referencia(grama):
    toks = grama.split()
    k = sum(1 for t in toks if t.isdigit() or t in REF_TOKENS or re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", t))
    return k * 2 >= len(toks)


def paragrafos(corpo):
    return [p.strip() for p in re.split(r"\n\s*\n", corpo) if p.strip()]


def textos_do_projeto(raiz, com_catalogo=True):
    """(rótulo, [source_ids], texto)."""
    cat = projeto.fontes_por_id(raiz)
    for v in projeto.verbetes(raiz):
        fm = v["fm"]
        if not fm:
            continue
        fontes = list(fm.get("fontes") or [])
        rot = v["rel"]
        if fm.get("resumo"):
            yield f"{rot}:resumo", fontes, str(fm["resumo"])
        defs = projeto.notas(v["corpo"])
        corpo = projeto.corpo_sem_notas(v["corpo"])
        for i, par in enumerate(paragrafos(corpo)):
            citadas = []
            for r in projeto.NOTA_REF.findall(par):
                citadas += [s for s in projeto.fontes_citadas_em(defs.get(r, ""), cat) if s not in citadas]
            yield f"{rot}:§{i + 1}", citadas + [f for f in fontes if f not in citadas], par
    lt = projeto.linha_do_tempo(raiz) or {}
    for e in lt.get("eventos", []) if isinstance(lt, dict) else []:
        for campo in ("titulo", "resumo", "divergencia"):
            if e.get(campo):
                yield f"linha_do_tempo/{e.get('id')}.{campo}", e.get("fontes", []), e[campo]
    cx = projeto.conexoes(raiz) or {}
    for i, c in enumerate(cx.get("conexoes", []) if isinstance(cx, dict) else []):
        if c.get("nota"):
            yield f"conexoes[{i}].nota", c.get("fontes", []), c["nota"]
    if com_catalogo:
        for lote, f in projeto.fontes(raiz):
            if f.get("resumo"):
                yield f"fontes/{lote}:{f.get('id')}.resumo", [f.get("id")], f["resumo"]


def pasta_refs(raiz):
    refs = os.environ.get("ANTICOPIA_REFS")
    if refs is not None:
        return refs or None
    from acervo_dir import acervo_padrao
    for base in (acervo_padrao(), Path(raiz) / "acervo"):
        if (base / "txt").is_dir() and any((base / "txt").glob("*.txt")):
            return str(base / "txt")
    return None


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    raiz = Path(args[args.index("--raiz") + 1]) if "--raiz" in args else projeto.RAIZ
    n = int(args[args.index("--n") + 1]) if "--n" in args else 8
    erros, avisos, proximos = [], [], []
    textos = list(textos_do_projeto(raiz, "--sem-catalogo" not in args))

    for rot, _, txt in textos:
        for m in ASPAS.finditer(txt):
            k = len(normalizar(m.group(1)))
            if k >= LIMITE_CITACAO:
                erros.append(f"{rot}: citação entre aspas com {k} palavras (limite {LIMITE_CITACAO - 1}) — parafrasear")
            elif k >= AVISO_CITACAO:
                avisos.append(f"{rot}: citação curta ({k} palavras) — conferir se é DP e necessária: “{m.group(1)}”")

    refs_dir = pasta_refs(raiz)
    n_refs = 0
    if refs_dir:
        indice = defaultdict(set)
        por_id = {}
        com_erro = set()
        for p in sorted(Path(refs_dir).expanduser().rglob("*.txt")):
            n_refs += 1
            pal = normalizar(HIFEN.sub(r"\1\2", p.read_text(encoding="utf-8", errors="ignore")))
            por_id[p.stem] = pal
            for g in ngramas(pal, n):
                indice[g].add(p.stem)
        for rot, _, txt in textos:
            iguais = sorted(g for g in ngramas(normalizar(txt), n) if g in indice and not eh_referencia(g))
            if iguais:
                obras = sorted({o for g in iguais for o in indice[g]})
                com_erro.add(rot)
                erros.append(f"{rot}: {len(iguais)} sequência(s) de {n} palavras idêntica(s) a {', '.join(obras)} — ex.: “{iguais[0]}”")
        cache = {}
        for rot, fontes, txt in textos:
            pal = normalizar(txt)
            vistos = set()
            for f in fontes or []:
                if f not in por_id:
                    continue
                if f not in cache:
                    cache[f] = ngramas(por_id[f], AVISO_FONTE)
                k = AVISO_FONTE
                pos = [i for i in range(len(pal) - k + 1)
                       if " ".join(pal[i:i + k]) in cache[f] and not eh_referencia(" ".join(pal[i:i + k]))]
                trechos, ini, fim = [], None, None
                for i in pos:
                    if ini is not None and i == fim + 1:
                        fim = i
                    else:
                        if ini is not None:
                            trechos.append((ini, fim))
                        ini = fim = i
                if ini is not None:
                    trechos.append((ini, fim))
                for a, b in trechos:
                    tam = b - a + k
                    trecho = " ".join(pal[a:b + k])
                    if (tam < n or rot not in com_erro) and trecho not in vistos:
                        vistos.add(trecho)
                        proximos.append(f"{rot}: {tam} palavras iguais a {f} — “{trecho}”")

    print(f"{len(textos)} textos verificados; n={n}; referências: "
          + (f"{n_refs} arquivo(s) em {refs_dir}" if refs_dir else
             "nenhuma (sem acervo: rode scripts/acervo_sync.sh pull ou defina ANTICOPIA_REFS)"))
    for a in avisos:
        print(" aviso:", a)
    if proximos:
        print(f"\n{len(proximos)} aviso(s) de redação próxima da fonte citada ({AVISO_FONTE}–{n - 1} palavras; reescrever ou justificar):")
        for a in proximos:
            print(" próximo:", a)
    if erros:
        print(f"\n{len(erros)} erro(s):")
        for e in erros:
            print(" -", e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
