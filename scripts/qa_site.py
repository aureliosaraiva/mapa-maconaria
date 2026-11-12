#!/usr/bin/env python3
"""QA do site gerado (site/dist), depois do `npm run build`. Sem rede, só biblioteca padrão.

1. Acervo privado fora do site: nenhum arquivo do dist com "acervo" ou "fontes-maconaria" no
   caminho, nenhum PDF, nenhum .txt (exceto robots.txt), nenhum arquivo com nome de source_id
   (<id>.pdf/.txt/.html fora de /fontes/<id>/); nenhuma página menciona caminhos do acervo
   (txt/<id>.txt, pdf/<id>.pdf, fontes-maconaria); e, se houver textos do acervo
   ($ANTICOPIA_REFS ou txt/ de $ACERVO_DIR / ../fontes-maconaria), nenhuma sequência de 20
   palavras de um deles aparece no texto do site (descontadas as que estão no próprio catálogo:
   títulos, autores, resumos — que o anti-cópia confere à parte).
2. Cobertura: uma página por verbete (/verbetes/<id>/) e por fonte (/fontes/<id>/); páginas
   fixas (início, verbetes, fontes, linha do tempo, grafo, metodologia, buscar); cada evento da
   linha do tempo com âncora #ev-<id>.
3. Links internos (href/src) apontam para arquivos existentes e âncoras (#id) existentes.
4. Conteúdo ritual reservado: nenhum padrão 'erro' de scripts/config/alerta_ritual.json (nem
   termo da lista privada) no texto visível de nenhuma página.
5. `noindex` em todas as páginas (até o autor decidir indexação) e rodapé com licença MIT e
   aviso de direitos.

Uso: python3 scripts/qa_site.py [--dist site/dist] [--raiz DIR]
SITE_BASE (padrão /mapa-maconaria; SITE_BASE=/ para a raiz) igual ao do build.
Sai com código 1 se houver erro.
"""
import hashlib
import html
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import projeto  # noqa: E402
from alerta_ritual import Alerta  # noqa: E402

N_ACERVO = 20


class Pagina(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.texto, self.metas = [], set(), [], []
        self._pula = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for k in ("href", "src"):
            if a.get(k) and tag in ("a", "link", "script", "img", "source", "iframe"):
                self.links.append(a[k])
        if tag == "meta":
            self.metas.append(a)
        if tag in ("script", "style", "template"):
            self._pula += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template") and self._pula:
            self._pula -= 1

    def handle_data(self, d):
        if not self._pula:
            self.texto.append(d)


def palavras(t):
    return re.findall(r"\w+", t.lower())


def h(g):
    return hashlib.blake2b(g.encode(), digest_size=8).digest()


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    raiz = Path(args[args.index("--raiz") + 1]) if "--raiz" in args else projeto.RAIZ
    dist = Path(args[args.index("--dist") + 1]) if "--dist" in args else projeto.RAIZ / "site" / "dist"
    base = (os.environ.get("SITE_BASE", "/mapa-maconaria") or "/").rstrip("/") + "/"
    erros, avisos = [], []
    if not (dist / "index.html").exists():
        print(f"ERRO: {dist}/index.html não existe (rode npm run build em site/)")
        return 1

    fontes = projeto.fontes_por_id(raiz)
    verbetes = [v["fm"] for v in projeto.verbetes(raiz) if v["fm"]]
    lt = projeto.linha_do_tempo(raiz) or {"eventos": []}

    # 1. arquivos
    arquivos = [p for p in dist.rglob("*") if p.is_file()]
    for p in arquivos:
        rel = p.relative_to(dist).as_posix()
        if "acervo" in rel.lower() or "fontes-maconaria" in rel.lower():
            erros.append(f"arquivo com 'acervo' no caminho: {rel}")
        if p.suffix.lower() == ".pdf":
            erros.append(f"PDF publicado: {rel}")
        if p.suffix.lower() == ".txt" and p.name != "robots.txt":
            erros.append(f"arquivo .txt publicado: {rel}")
        if p.stem in fontes and p.suffix.lower() in (".pdf", ".txt", ".html", ".htm") and not rel.startswith("fontes/"):
            erros.append(f"arquivo com nome de source_id (cópia do acervo?): {rel}")

    paginas = {}
    for p in dist.rglob("*.html"):
        pg = Pagina()
        pg.feed(p.read_text(encoding="utf-8", errors="ignore"))
        paginas[p] = pg
    CAMINHO_ACERVO = re.compile(r"fontes-maconaria|\b(?:txt|pdf|html)/[a-z0-9]+(?:-[a-z0-9]+)+\.(?:txt|pdf|html)\b")
    for p, pg in paginas.items():
        m = CAMINHO_ACERVO.search(" ".join(pg.texto) + " " + " ".join(pg.links))
        if m and "github.com/aureliosaraiva/fontes-maconaria" not in m.group(0):
            erros.append(f"{p.relative_to(dist)}: menciona caminho do acervo privado: {m.group(0)}")

    # 1b. trechos longos do acervo no texto do site
    from anticopia import pasta_refs
    refs = pasta_refs(raiz)
    n_refs = 0
    if refs:
        site_g = {}
        for p, pg in paginas.items():
            pal = palavras(" ".join(pg.texto))
            for i in range(len(pal) - N_ACERVO + 1):
                site_g.setdefault(h(" ".join(pal[i:i + N_ACERVO])), p)
        cat_txt = palavras(" ".join(" ".join([f.get("titulo", ""), f.get("titulo_traduzido", "") or "", " ".join(f.get("autores", [])), f.get("resumo", "") or "", f.get("observacoes", "") or ""]) for f in fontes.values()))
        cat_g = {h(" ".join(cat_txt[i:i + N_ACERVO])) for i in range(len(cat_txt) - N_ACERVO + 1)}
        achados = {}
        for t in sorted(Path(refs).expanduser().rglob("*.txt")):
            n_refs += 1
            pal = palavras(t.read_text(encoding="utf-8", errors="ignore"))
            for i in range(len(pal) - N_ACERVO + 1):
                g = " ".join(pal[i:i + N_ACERVO])
                k = h(g)
                if k in site_g and k not in cat_g:
                    achados.setdefault((t.stem, site_g[k]), g)
        for (fonte, p), g in achados.items():
            erros.append(f"{p.relative_to(dist)}: trecho de {N_ACERVO} palavras igual ao texto integral de {fonte}: “{g}”")

    # 2. cobertura
    def existe(rel):
        return (dist / rel / "index.html").exists() or (dist / f"{rel}.html").exists()
    for fixa in ("verbetes", "fontes", "linha-do-tempo", "grafo", "metodologia", "buscar"):
        if not existe(fixa):
            erros.append(f"página fixa ausente: /{fixa}/")
    for v in verbetes:
        if not existe(f"verbetes/{v.get('id')}"):
            erros.append(f"verbete sem página: {v.get('id')}")
    for fid in fontes:
        if not existe(f"fontes/{fid}"):
            erros.append(f"fonte sem página: {fid}")
    pl = dist / "linha-do-tempo" / "index.html"
    if pl in paginas:
        for e in lt.get("eventos", []):
            if f"ev-{e.get('id')}" not in paginas[pl].ids:
                erros.append(f"evento sem âncora na linha do tempo: {e.get('id')}")

    # 3. links internos
    def alvo(p, href):
        u = urlsplit(href)
        if u.scheme or u.netloc or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
            return None, None
        caminho = unquote(u.path)
        if not caminho:
            return p, u.fragment
        if caminho.startswith("/"):
            if not caminho.startswith(base):
                return "fora", None
            rel = caminho[len(base):]
        else:
            rel = (p.parent / caminho).resolve().relative_to(dist.resolve()).as_posix()
        d = dist / rel
        for c in (d, d / "index.html", Path(str(d) + ".html")):
            if c.is_file():
                return c, u.fragment
        return "quebrado", None
    for p, pg in paginas.items():
        for href in pg.links:
            dest, frag = alvo(p, href)
            if dest is None:
                continue
            if dest in ("fora", "quebrado"):
                erros.append(f"{p.relative_to(dist)}: link interno {dest}: {href}")
            elif frag and dest in paginas and frag not in paginas[dest].ids:
                erros.append(f"{p.relative_to(dist)}: âncora inexistente: {href}")

    # 4. conteúdo ritual reservado
    alerta = Alerta()
    for p, pg in paginas.items():
        e_r, _ = alerta.verificar(html.unescape(" ".join(pg.texto)))
        for t in e_r:
            erros.append(f"{p.relative_to(dist)}: possível conteúdo ritual reservado: “{t}”")

    # 5. noindex e rodapé
    for p, pg in paginas.items():
        if not any(m.get("name") == "robots" and "noindex" in (m.get("content") or "") for m in pg.metas):
            erros.append(f"{p.relative_to(dist)}: sem meta robots noindex")
        txt = " ".join(pg.texto)
        if "licença MIT" not in txt or "direitos sobre as obras" not in txt:
            erros.append(f"{p.relative_to(dist)}: rodapé sem licença MIT/aviso de direitos")

    print(f"QA do site: {len(paginas)} páginas, {len(arquivos)} arquivos, {len(verbetes)} verbetes, {len(fontes)} fontes, "
          f"{len(lt.get('eventos', []))} eventos; acervo para comparação: " + (f"{n_refs} texto(s) em {refs}" if refs else "nenhum"))
    for a in avisos:
        print(" aviso:", a)
    for e in erros[:200]:
        print(" ERRO:", e)
    if len(erros) > 200:
        print(f" ... e mais {len(erros) - 200} erros")
    if erros:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
