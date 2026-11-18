# Estado do projeto

> Arquivo de passagem entre sessões. Toda sessão começa lendo este arquivo. **Só a orquestradora reescreve**; trabalhadoras atualizam só a própria linha no `ORQUESTRACAO.md`.

**Última atualização:** 2026-11-18 — encadeamento funcionando: V05, V01, V02 e R01 concluídas e dispararam A01, V03 e V04 (retomadas hoje após limite de uso). **119 verbetes** (potências 31, documentos 29, brasil 22, ritos 12, graus 8, ordens anexas 7, eventos 6, antimaçonaria 3, conceitos 1). Fila: V06, A02, V07, A03, V08.

## Onde estamos
**Onda 1 — coleta ampla + infraestrutura: concluída** (relatórios em `docs/sessoes/C01–C08.md`, `I01.md`). **Onda 3 — verbetes: em andamento.** Ver [`ORQUESTRACAO.md`](ORQUESTRACAO.md).

| Indicador | Valor | Como conferir |
|---|---:|---|
| Fontes no catálogo | 1120 (8 lotes; en 358, es 332, pt 189, fr 109, de 56, it 45, ru 8, nl 6...) | `python3 scripts/validar_fontes.py` |
| Cópias no acervo | 999 textos (+ datasets Wikidata em `outros/`) | `find ../fontes-maconaria/txt -type f \| wc -l` |
| Verbetes | 119 | `find data/verbetes -name '*.md' \| wc -l` |

## Ação do autor pendente
- **Ativar o GitHub Pages** do `mapa-maconaria`: Settings → Pages → Source: GitHub Actions (o workflow de deploy já existe).
- Obras para baixar/comprar: `COLETA.md` do acervo (seções por sessão).
- Site gob.org.br aparentemente invadido (spam para robôs desde 03/11) — avisar o GOB, se tiver contato.

## Decisões tomadas
- Mesmo método do `mapadosorixas`: fonte por afirmação, paráfrase, divergências lado a lado, acervo privado (`fontes-maconaria`) separado do repositório público.
- Commit e push sempre direto na `main` dos dois repositórios (decisão do autor, 2026-11-02).
- Catálogo fragmentado por lote (`data/fontes/<lote>.json`) para paralelismo.
- Rituais: acervo guarda o publicado; site não reproduz palavras/sinais/toques/juramentos (CLAUDE.md regra 5).
- Sem pirataria (CLAUDE.md regra 8).

## Próximas tarefas (orquestradora)
1. Acompanhar a onda 1; ao concluir, consolidar números aqui.
2. Definir onda 2 (aprofundamento: teses, periódicos, hemerotecas, idiomas sub-representados) com base nas lacunas dos relatórios.
3. Definir onda 3 (verbetes por família) e onda 4 (integração/QA).
