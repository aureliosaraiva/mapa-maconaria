"""Leitura comum dos dados do projeto (catálogo, verbetes, linha do tempo, conexões).

Usado por validar_verbetes.py, validar_linha_do_tempo.py, anticopia.py e qa_site.py.
Todas as funções aceitam `raiz` (padrão: raiz deste repositório) para que os testes
rodem contra dados sintéticos (tests/fixtures/) numa cópia temporária.
"""
import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

CATEGORIAS = ["ritos", "graus", "potencias", "documentos", "principios", "simbolos", "eventos",
              "brasil", "personalidades", "lugares", "ordens-anexas", "antimaconaria", "conceitos"]

FM = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)
NOTA_DEF = re.compile(r"^\[\^([^\]\s]+)\]:\s*(.+?)\s*$", re.M)
NOTA_REF = re.compile(r"\[\^([^\]\s]+)\](?!:)")
WIKILINK = re.compile(r"\[\[([a-z0-9]+(?:-[a-z0-9]+)*)(?:\|[^\]]*)?\]\]")
ID_FONTE = re.compile(r"\b[a-z0-9]+(?:-[a-z0-9]+)*-(?:1[0-9]{3}|20[0-9]{2}|sd)-[a-z0-9]+(?:-[a-z0-9]+)*\b")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def ler_json(p, padrao=None):
    p = Path(p)
    if not p.exists():
        return padrao
    return json.loads(p.read_text(encoding="utf-8"))


def fontes(raiz=RAIZ):
    """Lista de (lote_arquivo, fonte) de todos os lotes data/fontes/*.json (JSON inválido é ignorado)."""
    out = []
    for p in sorted((Path(raiz) / "data" / "fontes").glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for f in d.get("fontes", []) or []:
            out.append((p.name, f))
    return out


def fontes_por_id(raiz=RAIZ):
    return {f.get("id"): f for _, f in fontes(raiz)}


def vocab(raiz=RAIZ):
    """Códigos `entre crases` de docs/taxonomia.md (aproximação, usada só para avisos)."""
    p = Path(raiz) / "docs" / "taxonomia.md"
    if not p.exists():
        p = RAIZ / "docs" / "taxonomia.md"
    return set(re.findall(r"`([a-z0-9_]+)`", p.read_text(encoding="utf-8")))


def codigo_conhecido(c, V):
    return c in V or bool(re.match(r"^(gl|go)_[a-z]{2,}$", c))


def separar_front_matter(texto):
    """(yaml_str | None, corpo)."""
    m = FM.match(texto)
    if not m:
        return None, texto
    return m.group(1), texto[m.end():]


def _datas_iso(x):
    """YAML lê 1822-06-17 como date: volta para texto ISO (o esquema aceita ano ou 'AAAA-MM-DD')."""
    import datetime
    if isinstance(x, (datetime.date, datetime.datetime)):
        return x.isoformat()[:10]
    if isinstance(x, dict):
        return {k: _datas_iso(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_datas_iso(v) for v in x]
    return x


def verbetes(raiz=RAIZ):
    """Lista de dicts {caminho, categoria_pasta, fm (dict|None), erro_fm, corpo}."""
    import yaml
    out = []
    base = Path(raiz) / "data" / "verbetes"
    for p in sorted(base.rglob("*.md")):
        rel = p.relative_to(base)
        if p.name.lower() in ("readme.md", "leiame.md"):
            continue
        txt = p.read_text(encoding="utf-8")
        y, corpo = separar_front_matter(txt)
        fm, erro = None, None
        if y is None:
            erro = "sem front matter YAML (--- ... ---)"
        else:
            try:
                fm = _datas_iso(yaml.safe_load(y))
                if not isinstance(fm, dict):
                    erro, fm = "front matter não é um mapa YAML", None
            except Exception as e:
                erro = f"YAML inválido: {e}"
        out.append({"caminho": p, "rel": str(rel), "categoria_pasta": rel.parts[0] if len(rel.parts) > 1 else "",
                    "fm": fm, "erro_fm": erro, "corpo": corpo})
    return out


def notas(corpo):
    """{rotulo: texto} das definições de nota [^n]: ..."""
    return {m.group(1): m.group(2) for m in NOTA_DEF.finditer(corpo)}


def corpo_sem_notas(corpo):
    return NOTA_DEF.sub("", corpo)


def fontes_citadas_em(texto, ids_conhecidos=None):
    """source_ids citados num texto de nota: tokens com cara de id; se `ids_conhecidos`
    for dado, só os que existem nele, mais os com cara de id que não existem (para erro)."""
    achados = []
    for tok in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+", texto):
        if (ids_conhecidos and tok in ids_conhecidos) or ID_FONTE.fullmatch(tok):
            if tok not in achados:
                achados.append(tok)
    return achados


def arquivos_linha_do_tempo(raiz=RAIZ):
    """Fragmentos data/linha_do_tempo/*.json (um por sessão) + legado data/linha_do_tempo.json."""
    base = Path(raiz) / "data"
    arqs = sorted((base / "linha_do_tempo").glob("*.json")) if (base / "linha_do_tempo").is_dir() else []
    if (base / "linha_do_tempo.json").is_file():
        arqs.append(base / "linha_do_tempo.json")
    return arqs


def id_evento(arquivo, i, e):
    return e.get("id") or f"{norm(Path(arquivo).stem).replace(' ', '-')}-{i + 1}"


def linha_do_tempo(raiz=RAIZ):
    """{"eventos": [...]} juntando todos os fragmentos; cada evento ganha `id` (se faltar) e
    `_arquivo`. None se não houver nenhum fragmento. Fragmento com JSON inválido é ignorado
    aqui (o validador acusa)."""
    arqs = arquivos_linha_do_tempo(raiz)
    if not arqs:
        return None
    evs = []
    for p in arqs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for i, e in enumerate(d.get("eventos", []) if isinstance(d, dict) else []):
            if isinstance(e, dict):
                evs.append({**e, "id": id_evento(p, i, e), "_arquivo": p.name})
    return {"eventos": evs}


def conexoes(raiz=RAIZ):
    return ler_json(Path(raiz) / "data" / "conexoes.json")
