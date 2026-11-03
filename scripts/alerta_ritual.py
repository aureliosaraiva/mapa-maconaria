"""Lista de alerta de conteúdo ritual reservado (CLAUDE.md regra 5).

Carrega scripts/config/alerta_ritual.json (padrões públicos) e, se existirem, termos
literais privados de scripts/config/alerta_ritual.local.json ou do arquivo indicado por
ALERTA_RITUAL_EXTRA (JSON {"termos": [...]} ou texto com um termo por linha).
"""
import json
import os
import re
import unicodedata
from pathlib import Path

DIR = Path(__file__).resolve().parent / "config"


def sem_acento(t):
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()


def _termos_extras():
    termos = []
    candidatos = [DIR / "alerta_ritual.local.json"]
    if os.environ.get("ALERTA_RITUAL_EXTRA"):
        candidatos.append(Path(os.environ["ALERTA_RITUAL_EXTRA"]).expanduser())
    for p in candidatos:
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        try:
            termos += json.loads(txt).get("termos", [])
        except ValueError:
            termos += [l.strip() for l in txt.splitlines() if l.strip() and not l.startswith("#")]
    return termos


class Alerta:
    def __init__(self, arquivo=DIR / "alerta_ritual.json"):
        cfg = json.loads(Path(arquivo).read_text(encoding="utf-8"))
        self.erro = [re.compile(p, re.I) for p in cfg.get("erro", [])]
        self.aviso = [re.compile(p, re.I) for p in cfg.get("aviso", [])]
        extras = _termos_extras()
        self.n_extras = len(extras)
        self.termos = [re.compile(r"\b" + re.escape(sem_acento(t)) + r"\b", re.I) for t in extras]

    def verificar(self, texto):
        """(erros, avisos): listas de trechos encontrados. Termos privados aparecem mascarados."""
        t = sem_acento(texto)
        erros, avisos = [], []
        for r in self.erro:
            for m in r.finditer(t):
                erros.append(m.group(0)[:80])
        for r in self.termos:
            for m in r.finditer(t):
                erros.append(f"termo da lista privada ({m.group(0)[:2]}…)")
        for r in self.aviso:
            for m in r.finditer(t):
                avisos.append(m.group(0))
        return erros, avisos
