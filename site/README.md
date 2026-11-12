# Site da Enciclopédia da Maçonaria

Site estático (Astro + Cytoscape.js + Pagefind) que **só exibe** os dados de `data/`; nenhum
conteúdo sobre maçonaria é escrito aqui. Compila com qualquer quantidade de dados, inclusive 0
verbetes e sem linha do tempo.

## Rodar
```bash
cd site
npm ci
npm run dev                # http://localhost:4321/mapa-maconaria/
npm run build              # gera dist/ e o índice de busca (Pagefind)
python3 ../scripts/qa_site.py   # QA do dist (links, cobertura, nada do acervo, alerta ritual)
python3 ../tests/e2e_site.py    # build com dados sintéticos (tests/fixtures) + conferências
```
`SITE_BASE` (padrão `/mapa-maconaria`; `SITE_BASE=/` para a raiz) e `SITE_URL` mudam o endereço.

## O que é lido
| Página | Dados |
|---|---|
| `/` início (números, categorias, busca) | tudo |
| `/verbetes/`, `/verbetes/<id>/` | `data/verbetes/<categoria>/<id>.md` (front matter: `docs/verbetes-guia.md`, `schemas/verbete.schema.json`) |
| `/fontes/` (filtros), `/fontes/<id>/` | `data/fontes/*.json` (todos os lotes) |
| `/linha-do-tempo/` | `data/linha_do_tempo/<ID>.json` (fragmentos por sessão; `schemas/linha_do_tempo.schema.json`) |
| `/grafo/` | `relacionados` dos verbetes + `data/conexoes.json` (`schemas/conexoes.schema.json`) |
| `/glossario/` | `data/glossario.json` = `{"termos": [{"id","termo","definicao","fontes":[...],"verbete"?,"variantes"?:[...]}]}` |
| `/metodologia/`, `/buscar/` | números do catálogo; índice Pagefind |

No corpo dos verbetes: `[[id]]` ou `[[id|rótulo]]` vira link para o verbete (ou texto, se ele
ainda não existe) e todo `source_id` citado numa nota `[^n]: <source_id>, p. X` vira link para a
página da fonte (`src/lib/remark-enciclopedia.mjs`).

## Regras que o site respeita
- Nada do acervo privado (`fontes-maconaria`): o campo `acervo` das fontes não é exibido; o QA
  barra PDF/txt, caminhos do acervo e trechos de 20 palavras iguais ao texto integral.
- Conteúdo ritual: verbetes `sensivel: true` mostram aviso; o QA procura os padrões de
  `scripts/config/alerta_ritual.json` em todas as páginas.
- `noindex` em todas as páginas até o autor decidir indexação.

## Publicação
`.github/workflows/deploy-pages.yml` publica em https://aureliosaraiva.github.io/mapa-maconaria/
a cada push na `main`, depois de validadores, testes, build e QA. Requer **Pages ativado com
fonte "GitHub Actions"** (Settings → Pages), ação do dono do repositório.
