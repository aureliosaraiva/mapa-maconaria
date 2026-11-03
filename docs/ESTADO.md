# Estado do projeto

> Arquivo de passagem entre sessões. Toda sessão começa lendo este arquivo. **Só a orquestradora reescreve**; trabalhadoras atualizam só a própria linha no `ORQUESTRACAO.md`.

**Última atualização:** 2026-11-03 08:10 UTC — onda 1: C01, C02, C05 concluídas; C03, C04, C07 em andamento; C06, C08, I01 na fila (execução em lotes de 3 por limite de uso).

## Onde estamos
**Onda 1 — coleta ampla + infraestrutura: em andamento.** Ver [`ORQUESTRACAO.md`](ORQUESTRACAO.md).

| Indicador | Valor | Como conferir |
|---|---:|---|
| Fontes no catálogo | 583 (6 lotes; en 256, pt 158, fr 73, de 34, es 22, it 20, ru 7, la 5...) | `python3 scripts/validar_fontes.py` |
| Cópias no acervo | 506 textos | `find ../fontes-maconaria/txt -type f \| wc -l` |
| Verbetes | 0 | `find data/verbetes -name '*.md' \| wc -l` |

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
