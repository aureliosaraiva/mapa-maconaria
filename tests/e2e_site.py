#!/usr/bin/env python3
"""Ponta a ponta do site com dados sintéticos: copia site/ para uma pasta temporária com
tests/fixtures/data no lugar de data/, faz o build (Astro + Pagefind) e confere:
- scripts/qa_site.py passa (links, âncoras, cobertura, acervo, alerta ritual, noindex);
- página de verbete com nota ligada à fonte, [[link]] para verbete existente e texto para o
  inexistente, aviso de verbete sensível, "Ver também" vindo de `relacionados`;
- linha do tempo lê os fragmentos (ids '<arquivo>-<n>', precisão década/século, nota);
- grafo com dados; página da fonte lista os verbetes que a citam;
- QA acusa um trecho de 20 palavras do "acervo" que aparece no site.
Precisa de site/node_modules (npm ci em site/). Uso: python3 tests/e2e_site.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FIX = RAIZ / "tests" / "fixtures"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="e2e-maconaria-"))
    try:
        shutil.copytree(RAIZ / "site", tmp / "site", ignore=shutil.ignore_patterns("node_modules", "dist", ".astro"))
        (tmp / "site" / "node_modules").symlink_to(RAIZ / "site" / "node_modules")
        shutil.copytree(FIX / "data", tmp / "data")
        env = {**os.environ, "SITE_BASE": "/mapa-maconaria", "ASTRO_TELEMETRY_DISABLED": "1"}
        r = subprocess.run(["npm", "run", "build"], cwd=tmp / "site", env=env, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-3000:], r.stderr[-3000:])
            return 1
        dist = tmp / "site" / "dist"
        falhas = []
        env_qa = {**env, "ANTICOPIA_REFS": str(FIX / "acervo" / "txt")}
        qa = subprocess.run([sys.executable, str(RAIZ / "scripts" / "qa_site.py"), "--raiz", str(tmp), "--dist", str(dist)],
                            env=env_qa, capture_output=True, text=True)
        print(qa.stdout.strip())
        if qa.returncode:
            falhas.append("qa_site.py falhou com as fixtures")

        def ler(rel):
            p = dist / rel
            return p.read_text(encoding="utf-8") if p.exists() else ""

        def confere(rel, *trechos, ausente=()):
            t = ler(rel)
            if not t:
                falhas.append(f"{rel} não gerado")
                return
            for s in trechos:
                if s not in t:
                    falhas.append(f"{rel}: falta {s!r}")
            for s in ausente:
                if s in t:
                    falhas.append(f"{rel}: não devia ter {s!r}")

        confere("verbetes/rito-exemplo/index.html", "/mapa-maconaria/fontes/exemplo-2001-alfa/", 'href="/mapa-maconaria/verbetes/potencia-exemplo/"',
                "verbete que ainda não existe", "Estrutura de graus", "Ver também", ausente=("[[", "verbetes/verbete-inexistente"))
        confere("verbetes/evento-exemplo/index.html", "conteúdo ritual", "Na linha do tempo")
        confere("verbetes/index.html", 'id="cat-ritos"', 'id="cat-potencias"')
        confere("linha-do-tempo/index.html", 'id="ev-t02-1"', 'id="ev-ev-gama"', "década de 1720", "século XVIII", "formato mínimo", "Divergência")
        confere("grafo/index.html", 'id="dados-grafo"', "envolvida em")
        confere("fontes/exemplo-2001-alfa/index.html", "Citada nos verbetes", "Potência Exemplo", "Citada na linha do tempo")
        confere("index.html", ">3</strong> verbetes")
        confere("glossario/index.html", "Termo Exemplo", "termo-acacia-exemplo", "/mapa-maconaria/verbetes/rito-exemplo")
        if not (dist / "pagefind" / "pagefind-ui.js").exists():
            falhas.append("índice do Pagefind não gerado")

        # QA deve acusar texto do "acervo" no site
        falso = tmp / "acervo_falso"
        falso.mkdir()
        (falso / "exemplo-2001-alfa.txt").write_text(
            "Não existe uma maçonaria única. Potências regulares e liberais divergem sobre a obrigatoriedade da crença no "
            "Grande Arquiteto do Universo, sobre a presença de mulheres e sobre quais landmarks valem.", encoding="utf-8")
        qa2 = subprocess.run([sys.executable, str(RAIZ / "scripts" / "qa_site.py"), "--raiz", str(tmp), "--dist", str(dist)],
                             env={**env, "ANTICOPIA_REFS": str(falso)}, capture_output=True, text=True)
        if qa2.returncode == 0 or "texto integral" not in qa2.stdout:
            falhas.append("qa_site.py não acusou trecho do acervo publicado no site")
        # QA deve acusar PDF publicado
        (dist / "x.pdf").write_bytes(b"%PDF-1.4")
        qa3 = subprocess.run([sys.executable, str(RAIZ / "scripts" / "qa_site.py"), "--raiz", str(tmp), "--dist", str(dist)],
                             env=env, capture_output=True, text=True)
        if qa3.returncode == 0 or "PDF publicado" not in qa3.stdout:
            falhas.append("qa_site.py não acusou PDF no dist")

        for f in falhas:
            print("FALHA:", f)
        print("e2e do site:", "OK" if not falhas else f"{len(falhas)} falha(s)")
        return 1 if falhas else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
