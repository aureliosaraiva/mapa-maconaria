#!/usr/bin/env python3
"""Valida os verbetes da enciclopédia (data/verbetes/<categoria>/<id>.md) e data/conexoes.json.

Verbetes:
- front matter YAML presente e válido contra schemas/verbete.schema.json (erro);
- `id` = nome do arquivo e `categoria` = pasta (erro); ids únicos (erro);
- `fontes`: todo source_id existe no catálogo data/fontes/*.json (erro); fonte só `pista` (aviso);
- notas `[^n]: <source_id>, p. X`: toda nota chamada no texto é definida e vice-versa (erro);
  cada nota cita ao menos um source_id do catálogo (erro) e ele está em `fontes` (aviso);
  verbete com fontes mas sem nenhuma nota (aviso: fonte por afirmação);
- `relacionados` e links `[[id]]` apontam para verbetes existentes (aviso; erro com --estrito);
- vocabulários de docs/taxonomia.md em temas/ritos/potencias/periodos (aviso);
- lista de alerta de conteúdo ritual (scripts/config/alerta_ritual.json): padrão 'erro' -> erro;
  menções -> aviso; `sensivel: true` -> aviso (pede revisão humana antes de publicar);
- citação entre aspas com 15+ palavras (erro; regra 2: paráfrase) — o anti-cópia completo é
  scripts/anticopia.py.

Conexões (data/conexoes.json, opcional): esquema, origem/destino existentes (aviso; erro com
--estrito), fontes no catálogo (erro).

Uso: python3 scripts/validar_verbetes.py [--estrito] [--raiz DIR] [--json]
Sai com código 1 se houver erro. Com 0 verbetes, passa.
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
LIMITE_CITACAO = 15


def validador(raiz, nome):
    try:
        import jsonschema
    except ImportError:
        return None
    esquema = json.loads((projeto.RAIZ / "schemas" / nome).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(esquema)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    raiz = Path(args[args.index("--raiz") + 1]) if "--raiz" in args else projeto.RAIZ
    estrito = "--estrito" in args
    erros, avisos = [], []
    ref_erro = erros if estrito else avisos

    cat = projeto.fontes_por_id(raiz)
    V = projeto.vocab(raiz)
    alerta = Alerta()
    val = validador(raiz, "verbete.schema.json")
    if val is None:
        avisos.append("jsonschema não instalado: checagem de esquema mínima (pip install jsonschema)")
    vs = projeto.verbetes(raiz)
    ids = Counter(v["fm"].get("id") for v in vs if v["fm"])
    for i, c in ids.items():
        if c > 1:
            erros.append(f"id de verbete duplicado ({c}x): {i}")
    existentes = set(ids)
    stats = Counter()

    for v in vs:
        rot = v["rel"]
        fm = v["fm"]
        if v["erro_fm"]:
            erros.append(f"{rot}: {v['erro_fm']}")
            continue
        if val:
            for e in val.iter_errors(fm):
                erros.append(f"{rot}: {'/'.join(map(str, e.path)) or '(raiz)'} {e.message}")
        else:
            for k in ("id", "titulo", "categoria", "resumo", "temas", "fontes", "status"):
                if k not in fm:
                    erros.append(f"{rot}: falta {k}")
        vid = fm.get("id")
        if vid != v["caminho"].stem:
            erros.append(f"{rot}: id '{vid}' diferente do nome do arquivo '{v['caminho'].stem}'")
        if fm.get("categoria") != v["categoria_pasta"]:
            erros.append(f"{rot}: categoria '{fm.get('categoria')}' diferente da pasta '{v['categoria_pasta']}'")
        stats[fm.get("categoria")] += 1
        stats["status:" + str(fm.get("status"))] += 1

        fontes = fm.get("fontes") or []
        for s in fontes:
            if s not in cat:
                erros.append(f"{rot}: fonte '{s}' não existe no catálogo (data/fontes/)")
            elif cat[s].get("status_verificacao") == "pista":
                avisos.append(f"{rot}: fonte '{s}' ainda é só 'pista' no catálogo (conferir antes de revisar)")

        corpo = v["corpo"]
        defs = projeto.notas(corpo)
        refs = set(projeto.NOTA_REF.findall(projeto.corpo_sem_notas(corpo)))
        for r in sorted(refs - set(defs)):
            erros.append(f"{rot}: nota [^{r}] chamada no texto mas não definida")
        for r in sorted(set(defs) - refs):
            erros.append(f"{rot}: nota [^{r}] definida mas não chamada no texto")
        for r, txt in defs.items():
            citados = projeto.fontes_citadas_em(txt, cat)
            if not citados:
                erros.append(f"{rot}: nota [^{r}] não cita nenhum source_id do catálogo: “{txt[:80]}”")
            for s in citados:
                if s not in cat:
                    erros.append(f"{rot}: nota [^{r}] cita '{s}', que não existe no catálogo")
                elif s not in fontes:
                    avisos.append(f"{rot}: nota [^{r}] cita '{s}', que não está em `fontes` do front matter")
        if fontes and not defs and projeto.corpo_sem_notas(corpo).strip():
            avisos.append(f"{rot}: corpo sem notas [^n] (fonte por afirmação: CLAUDE.md regra 1)")

        for rel in fm.get("relacionados") or []:
            if isinstance(rel, dict) and rel.get("id") not in existentes:
                ref_erro.append(f"{rot}: relacionado '{rel.get('id')}' não existe (ainda) como verbete")
            if isinstance(rel, dict) and rel.get("id") == vid:
                erros.append(f"{rot}: relacionado aponta para o próprio verbete")
        for w in projeto.WIKILINK.findall(corpo):
            if w not in existentes:
                ref_erro.append(f"{rot}: link [[{w}]] para verbete inexistente (o site mostra como texto)")

        for campo in ("temas", "ritos", "potencias", "periodos"):
            for c in fm.get(campo) or []:
                if isinstance(c, str) and not projeto.codigo_conhecido(c, V):
                    avisos.append(f"{rot}: {campo} '{c}' fora da taxonomia")

        texto = f"{fm.get('titulo', '')}\n{fm.get('resumo', '')}\n{projeto.corpo_sem_notas(corpo)}"
        e_r, a_r = alerta.verificar(texto)
        for t in e_r:
            erros.append(f"{rot}: possível reprodução de conteúdo ritual reservado (regra 5): “{t}”")
        if a_r:
            avisos.append(f"{rot}: {len(a_r)} menção(ões) a palavras/sinais/toques/juramentos ({', '.join(sorted(set(a_r))[:5])}) — conferir que nada é reproduzido")
        if fm.get("sensivel"):
            avisos.append(f"{rot}: marcado sensivel: true — exige revisão humana antes de publicar (regra 5)")
        for m in ASPAS.finditer(texto):
            k = len(re.findall(r"\w+", m.group(1)))
            if k >= LIMITE_CITACAO:
                erros.append(f"{rot}: citação entre aspas com {k} palavras (limite {LIMITE_CITACAO - 1}; regra 2)")

    # conexões
    cx = projeto.conexoes(raiz)
    n_cx = 0
    if cx is not None:
        valc = validador(raiz, "conexoes.schema.json")
        if valc:
            for e in valc.iter_errors(cx):
                erros.append(f"conexoes.json: {'/'.join(map(str, e.path)) or '(raiz)'} {e.message}")
        vistos = set()
        for i, c in enumerate(cx.get("conexoes", []) if isinstance(cx, dict) else []):
            n_cx += 1
            rot = f"conexoes.json[{i}]"
            for lado in ("origem", "destino"):
                if c.get(lado) not in existentes:
                    ref_erro.append(f"{rot}: {lado} '{c.get(lado)}' não existe (ainda) como verbete")
            for s in c.get("fontes", []):
                if s not in cat:
                    erros.append(f"{rot}: fonte '{s}' não existe no catálogo")
            k = (c.get("origem"), c.get("destino"), c.get("rel"))
            if k in vistos:
                avisos.append(f"{rot}: conexão repetida {k}")
            vistos.add(k)
            e_r, _ = alerta.verificar(c.get("nota") or "")
            for t in e_r:
                erros.append(f"{rot}: possível reprodução de conteúdo ritual reservado: “{t}”")

    resumo = {"verbetes": len(vs), "conexoes": n_cx, "por_categoria": {k: n for k, n in stats.items() if not k.startswith("status:")},
              "por_status": {k[7:]: n for k, n in stats.items() if k.startswith("status:")},
              "erros": len(erros), "avisos": len(avisos), "termos_privados_carregados": alerta.n_extras}
    if "--json" in args:
        print(json.dumps(resumo, ensure_ascii=False, indent=1))
    else:
        for a in avisos[:300]:
            print("aviso:", a)
        if len(avisos) > 300:
            print(f"... e mais {len(avisos) - 300} avisos")
        for e in erros:
            print("ERRO:", e)
        print(json.dumps(resumo, ensure_ascii=False))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
