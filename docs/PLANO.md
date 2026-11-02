# Plano — Enciclopédia da Maçonaria

> Documento vivo. Base: `CLAUDE.md`. Criado em 2026-11-02 pela sessão orquestradora.

## Visão
Ser a referência aberta, organizada e com fontes citadas sobre a maçonaria em todas as suas vertentes — ritos, rituais (no nível do que é publicado), princípios, simbolismo, potências, documentos, eventos e pessoas — no Brasil e no mundo, mostrando as divergências entre potências, ritos, países e épocas em vez de apagá-las.

## Entregáveis
| Repositório | Entregável |
|---|---|
| `fontes-maconaria` (privado) | Acervo: cópia integral (PDF/HTML/TXT) de todo conteúdo acessível legalmente; índice por lote; `COLETA.md` com o que exige ação humana |
| `mapa-maconaria` (público) | Catálogo de fontes (`data/fontes/`), verbetes (`data/verbetes/`), linha do tempo (`data/linha_do_tempo.json`), grafo (`data/conexoes.json`), glossário, site estático (Astro, como no mapadosorixas) |

## Fases e ondas de sessões
A execução é feita por **sessões trabalhadoras autônomas** do Claude Code, criadas e acompanhadas pela **sessão orquestradora** (esta que escreveu o plano). O quadro vivo de sessões, escopos e donos de arquivos está em [`ORQUESTRACAO.md`](ORQUESTRACAO.md).

### Onda 1 — Coleta ampla + infraestrutura (paralela)
Oito sessões de coleta temática (C01–C08), cada uma com seu lote de catálogo e acervo, mais uma sessão de infraestrutura (I01). Meta por sessão de coleta: **≥ 80 fontes catalogadas** com metadados conferidos, **cópia no acervo de tudo que for aberto/domínio público**, em ≥ 4 idiomas, e relatório com lacunas.

### Onda 2 — Aprofundamento da coleta
Definida pela orquestradora a partir dos relatórios da onda 1: teses e dissertações (BDTD, CAPES, theses.fr, ProQuest abertos), periódicos acadêmicos e maçônicos de acesso aberto (REHMLAC+, *Ars Quatuor Coronatorum* acessível, Pietre-Stones, *Heredom*, *Renaissance Traditionnelle* aberto, Cairn/Persée/OpenEdition, SciELO), hemerotecas (BN Digital, Gallica, Chronicling America), idiomas sub-representados (de, it, nl, sv, ru, pl), lacunas.

### Onda 3 — Enciclopédia (verbetes)
Sessões por família de verbetes (ritos e graus; potências; documentos; eventos mundiais + linha do tempo; Brasil; princípios, símbolos e conceitos; personalidades; ordens anexas, antimaçonaria e lugares; glossário). Cada verbete segue `docs/verbetes-guia.md`, com fontes do catálogo e leitura do texto no acervo.

### Onda 4 — Integração e qualidade
Site completo (catálogo filtrável, verbetes, linha do tempo interativa, grafo de conexões, busca, página de metodologia e limitações), anti-cópia global contra o acervo, auditoria de fontes e de conteúdo sensível, revisão cruzada entre sessões, preparação para versões es/en.

## Critérios de pronto (MVP)
- ≥ 600 fontes catalogadas, ≥ 50 % com cópia no acervo, ≥ 6 idiomas.
- Verbetes: todos os ritos da taxonomia, graus simbólicos + estrutura de graus de cada rito, ≥ 40 potências, ≥ 30 documentos, ≥ 60 eventos (≥ 20 do Brasil), ≥ 40 símbolos/conceitos, ≥ 60 personalidades.
- Linha do tempo com ≥ 150 datas com fonte; grafo com ritos ↔ potências ↔ eventos ↔ pessoas.
- 100 % dos dados factuais com `source_id`; anti-cópia 0 erros; 0 vazamento do acervo no site.

## Riscos
- **Sigilo ritual:** regra 5 do `CLAUDE.md`; sessão de auditoria na onda 4.
- **Direitos autorais:** acervo privado; site só paráfrase; sem pirataria.
- **Confiabilidade:** literatura maçônica tem muito mito de origem — confiabilidade A–D e seção de divergências/lendas.
- **Corrida entre sessões:** donos de arquivo no `ORQUESTRACAO.md`, catálogo fragmentado, push com rebase.
- **Limites de uso:** a orquestradora dosa o número de sessões simultâneas.
