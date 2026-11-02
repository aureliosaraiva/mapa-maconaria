#!/usr/bin/env bash
# Sincroniza o acervo de cópias integrais (repositório PRIVADO aureliosaraiva/fontes-maconaria).
#   scripts/acervo_sync.sh pull   início da sessão: clona ou atualiza em $ACERVO_DIR
#   scripts/acervo_sync.sh push   fim da sessão: commit + push dos arquivos novos
# ACERVO_DIR padrão: ../fontes-maconaria (irmão deste repositório).
# ACERVO_BRANCH padrão: o tronco do projeto (ver CLAUDE.md, "Branch de trabalho").
# Nada do acervo entra no repositório público mapa-maconaria.
# Em sessão na nuvem, anexe antes: add_repo(owner=aureliosaraiva, repo=fontes-maconaria, access=push).
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${ACERVO_DIR:-$RAIZ/../fontes-maconaria}"
URL="${ACERVO_URL:-https://github.com/aureliosaraiva/fontes-maconaria.git}"
BR="${ACERVO_BRANCH:-claude/mapa-maconaria-research-l6ubzj}"
modo="${1:-pull}"
case "$modo" in
  pull)
    if [ -d "$DIR/.git" ]; then
      git -C "$DIR" fetch origin "$BR" && git -C "$DIR" checkout -q -B "$BR" "origin/$BR" 2>/dev/null || git -C "$DIR" pull --rebase origin "$BR"
    else
      git clone --depth 1 --branch "$BR" "$URL" "$DIR"
    fi
    echo "acervo em $(cd "$DIR" && pwd): $(find "$DIR/txt" -type f 2>/dev/null | wc -l) textos"
    ;;
  push)
    [ -d "$DIR/.git" ] || { echo "sem clone em $DIR (rode: $0 pull)"; exit 1; }
    git -C "$DIR" add -A
    if git -C "$DIR" diff --cached --quiet; then echo "acervo sem mudanças"; exit 0; fi
    n=$(git -C "$DIR" diff --cached --name-only | wc -l)
    git -C "$DIR" commit -q -m "acervo: ${n} arquivo(s) novos/atualizados (${SESSAO:-sessao} $(date +%F))"
    for t in 2 4 8 16 32; do
      git -C "$DIR" pull --rebase origin "$BR" && git -C "$DIR" push -u origin "HEAD:$BR" && exit 0
      sleep "$t"
    done
    echo "push do acervo falhou"; exit 1
    ;;
  *) echo "uso: $0 pull|push"; exit 2 ;;
esac
