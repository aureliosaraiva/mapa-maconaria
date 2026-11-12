# Estado do projeto

> Arquivo de passagem entre sessões. Toda sessão começa lendo este arquivo. **Só a orquestradora reescreve**; trabalhadoras atualizam só a própria linha no `ORQUESTRACAO.md`.

**Última atualização:** 2026-11-12 — onda 1: 6 de 9 concluídas; C06, C08 e I01 retomadas (paradas desde 03/11 por limite de uso). Ondas 2 e 3 definidas no quadro. Orquestração passou a rodar em ciclos automáticos (`docs/ORQUESTRADOR.md`), via tarefa agendada a cada 2 h (id `trig_01GCxpR6cpf9U6edRjwvWgzu`, minuto 19 das horas pares UTC).

## Onde estamos
**Onda 1 — coleta ampla + infraestrutura: em andamento.** Ver [`ORQUESTRACAO.md`](ORQUESTRACAO.md).

| Indicador | Valor | Como conferir |
|---|---:|---|
| Fontes no catálogo | 1020 (8 lotes; en 318, es 308, pt 186, fr 100...) | `python3 scripts/validar_fontes.py` |
| Cópias no acervo | 917 textos | `find ../fontes-maconaria/txt -type f \| wc -l` |
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
