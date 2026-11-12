# Orquestração das sessões

> Fonte de verdade sobre **quem faz o quê e quem é dono de qual arquivo**. Só a sessão orquestradora cria ondas/linhas; cada trabalhadora atualiza **apenas a própria linha** (status e link do relatório) no fechamento.
> Orquestradora: sessão `session_011fM5cnUPbf7GuvJPgxJSh9` (claude.ai/code). Tronco: `main` nos dois repositórios (commit e push direto, decisão do autor).

## Quadro

| ID | Onda | Escopo | Arquivos de que é dona (mapa-maconaria) | Lote no acervo | Status | Relatório |
|---|---|---|---|---|---|---|
| C01 | 1 | Documentos fundadores e obras clássicas em domínio público | `data/fontes/c01-fundadores.json` | `indices/c01.json` | concluída | [C01](sessoes/C01.md) |
| C02 | 1 | Ritos, graus e rituais publicados (todos os ritos) | `data/fontes/c02-ritos.json` | `indices/c02.json` | concluída | [C02](sessoes/C02.md) |
| C03 | 1 | Potências e organizações (mundo e Brasil) | `data/fontes/c03-potencias.json` | `indices/c03.json` | concluída | [C03](sessoes/C03.md) |
| C04 | 1 | História mundial (Reino Unido, França, EUA, Europa central/norte) e historiografia | `data/fontes/c04-historia-mundo.json` | `indices/c04.json` | concluída | [relatório](sessoes/C04.md) |
| C05 | 1 | Brasil, Portugal e mundo lusófono | `data/fontes/c05-lusofono.json` | `indices/c05.json` | concluída | [relatório](sessoes/C05.md) — 138 fontes, 107 copiadas, 5 idiomas |
| C06 | 1 | América hispânica, Espanha, Itália e Caribe | `data/fontes/c06-iberoamerica.json` | `indices/c06.json` | concluída | [relatório](sessoes/C06.md) |
| C07 | 1 | Princípios, simbolismo, esoterismo, religião (inclui documentos eclesiásticos) e mulheres | `data/fontes/c07-doutrina.json` | `indices/c07.json` | concluída | [C07](sessoes/C07.md) |
| C08 | 1 | Obras de referência, Wikipédia/Wikidata multilíngue, museus, bibliotecas, periódicos e audiovisual | `data/fontes/c08-referencia.json`, `docs/pesquisa/acervos-e-periodicos.md` | `indices/c08.json` | concluída | [C08](sessoes/C08.md) |
| I01 | 1 | Infraestrutura: site Astro, validadores de verbetes, anti-cópia, CI | `site/`, `.github/`, `scripts/` (exceto `validar_fontes.py`, `acervo_*`), `schemas/verbete.schema.json`, `tests/` | — | concluída | [I01](sessoes/I01.md) |

Ondas 2–4: a definir pela orquestradora com base nos relatórios (ver `PLANO.md`).

---

## Instruções comuns às sessões de coleta (C01–C08)
1. Siga o `CLAUDE.md` (abertura, acervo, commits frequentes, fechamento).
2. **Busque em vários idiomas** (pt, en, fr, es, it, de no mínimo; mais os pertinentes ao tema). Use WebSearch (modo `extended` para temas de nicho) e WebFetch, e APIs abertas quando ajudarem: Internet Archive (`archive.org/advancedsearch.php`, `archive.org/download/<id>/`), Open Library, HathiTrust (full-text de domínio público), Wikisource, Project Gutenberg, Gallica (BnF), BN Digital, OpenAlex (`api.openalex.org`), Crossref, CORE, DOAJ, SciELO, Redalyc, Dialnet, HAL, Persée, OpenEdition, Cairn (só aberto), Google Books (só metadados), WorldCat (metadados).
3. Para cada fonte: entrada no seu lote do catálogo (`schemas/fonte.schema.json`) com `resumo` parafraseado, etiquetas da `taxonomia.md`, `confiabilidade`, `acesso`, `licenca`, `evidencias`.
4. **Cópia no acervo** (`../fontes-maconaria`): tudo que for domínio público, acesso aberto ou página oficial pública → `pdf/<id>.pdf` e/ou `html/<id>.html` + `txt/<id>.txt`, registrado em `indices/<lote>.json`; marque a fonte `status_verificacao: copiado` e preencha `acervo`. Use `curl -L --fail` com User-Agent normal; respeite robots/anti-robô (não contornar). Arquivo > 50 MB: só `txt` + URL.
5. Faça `scripts/acervo_sync.sh push` e commit/push do catálogo **a cada ~20 fontes**.
6. Relatório `docs/sessoes/<ID>.md`: números (fontes, copiadas, idiomas), principais achados (fontes-chave por subtema), **lacunas** e **sugestões de verbetes** (lista de ids/títulos), bloqueios (também no `PENDENCIAS.md`), e obras que exigem ação humana (também no `COLETA.md` do acervo — edite só a seção do seu lote, `## <ID>`).
7. Não escreva verbetes nesta onda; o foco é coleta e cópia. Fontes de outro tema achadas no caminho podem entrar no seu lote (verifique duplicata com `--buscar`).

### C01 — Documentos fundadores e clássicos em domínio público
Old Charges (Regius, Cooke, Grand Lodge No. 1, edições de Hughan e Speth/*Quatuor Coronatorum Antigrapha*), Estatutos Schaw, Edinburgh Register House MS, Graham MS, Sloane; Constituições de Anderson 1723 e 1738; Ahiman Rezon (Dermott, edições); Discurso de Ramsay; exposições: Prichard 1730, *Le Secret des Francs-Maçons* (1742), *L'Ordre des Francs-Maçons trahi* (1745), *Three Distinct Knocks*, *Jachin and Boaz*, *Hiram* (1764); Preston *Illustrations*; Hutchinson *Spirit of Masonry*; Webb *Freemason's Monitor*; Cross *Chart*; Morgan 1826; Allyn; Bernard *Light on Masonry*; Richardson *Monitor*; Duncan *Ritual*; Mackey (*Encyclopedia*, *Lexicon*, *Jurisprudence*, *Symbolism*, landmarks); Pike (*Morals and Dogma*); Oliver; Gould (*History of Freemasonry*, *Concise History*); Hughan; Findel; Ragon; Clavel; Kloss (bibliografia); Lessing *Ernst und Falk*; Fichte; Krause; textos do séc. XVIII-XIX em fr/de/es/pt/it. Fontes: Internet Archive, HathiTrust, Gallica, Google Books (DP), Wikisource, Gutenberg, sacred-texts.com (seção de maçonaria), Phoenixmasonry, Pietre-Stones. **Copiar tudo** (são DP).

### C02 — Ritos, graus e rituais publicados
Para cada rito da taxonomia: histórias do rito, rituais impressos/publicados disponíveis abertamente (rituais históricos em DP, edições críticas, rituais de potências publicados oficialmente quando públicos), estruturas de graus, monitores, rituais históricos dos altos graus (Francken MS 1771/1783, Rito de Perfeição, Constituições de 1762/1786, Clermont, Estrita Observância, RER: Código de 1778, Rituais de Lyon/Wilhelmsbad; Rito Moderno: *Régulateur du Maçon* 1801; Memphis-Misraïm: Marconis, Bédarride; Sueco; Schröder; Zinnendorf; Emulation: *Emulation Ritual* histórico; York/Webb; Rito Brasileiro (1878/1914/1968); Adonhiramita (Guillemain de Saint-Victor, *Recueil précieux* 1781); Rito Escocês Filosófico). Ordens anexas: Arco Real, Marca, Críptica, Templários, Rosa-Cruz, Shriners, Estrela do Oriente, DeMolay. Literatura acadêmica sobre ritos (Snoek, Mollier, Noël, Bernheim, Révauger, *Renaissance Traditionnelle*). Pt/fr/en/de/sv/es.

### C03 — Potências e organizações
Sites oficiais e documentos públicos (constituições, regulamentos gerais, históricos, listas de lojas/membros, relações de reconhecimento) de: GOB, CMSB e Grandes Lojas estaduais, COMAB e Grandes Orientes estaduais, Supremo Conselho do Brasil, potências mistas/femininas brasileiras; UGLE, GL Escócia, GL Irlanda; GOdF, GLNF, GLDF, GLFF, Droit Humain; GLs estaduais dos EUA, Prince Hall, Supremos Conselhos SJ/NMJ; Grande Oriente Lusitano, GLLP/GLRP; GLE, GOI, GL Argentina, Chile, México, Cuba, Uruguai, Colômbia, Peru, Venezuela; Alemanha (VGLvD), Suécia (Svenska Frimurare Orden), Países Baixos, Bélgica (GOB-be), Suíça (Alpina), Canadá, Austrália, Índia, África (Nigéria, Gana, África do Sul), Filipinas, Japão; organizações internacionais (CLIPSAS, CMI, CIMAL, Conferência de Supremos Conselhos); listas de reconhecimento (UGLE "Recognised Grand Lodges", Commission on Information for Recognition, Paul Bessel). Dados: fundação, sede, número de lojas/membros (com data), ritos. Copiar páginas institucionais (HTML) e PDFs públicos.

### C04 — História mundial e historiografia
Academia e historiografia séria: Stevenson (*Origins of Freemasonry*), Jacob, Bullock (*Revolutionary Brotherhood*), Prescott (CRFF Sheffield, artigos abertos), Kebbell, Berman, Harland-Jacobs (*Builders of Empire*), Hoffmann, Beaurepaire (*L'Europe des francs-maçons*), Halévi, Combes, Ligou, Chevallier, Porset/Révauger (*Le Monde maçonnique des Lumières*), Snoek/Bogdan (*Handbook of Freemasonry*, Brill), Önnerfors, Reinalter (Innsbruck), Hoffmann; Iluminados, Revolução Francesa, independência dos EUA, caso Morgan, Prince Hall (Wallace, Hinks/Kantrowitz), perseguições (nazismo — Melzer; Vichy; franquismo; URSS), P2, Rússia, Império Otomano, Índia/colônias. Periódicos: AQC (abertos), *Journal for Research into Freemasonry and Fraternalism*, *Heredom*, *Pietre-Stones*, *Ritual, Secrecy and Civil Society*, *Philosophical Transactions*... Centros: CRFF, Library and Museum of Freemasonry, Scottish Rite Research Society, Quatuor Coronati.

### C05 — Brasil, Portugal e mundo lusófono
Teses/dissertações (BDTD, CAPES, repositórios USP/UNICAMP/UFF/UFPE/UFRGS/UFMG/UnB/UFBA), SciELO, Hemeroteca Digital (BN), *Boletim do GOB* e periódicos maçônicos históricos, obras: Castellani (*História do Grande Oriente do Brasil*), Barata (*Luzes e Sombras*; *Maçonaria, sociabilidade e independência*), Morel (*As transformações dos espaços públicos*; Morel & Souza), Colussi (*A maçonaria gaúcha no século XIX*), Azevedo, Vieira (*O Bispo e os Maçons*), Lustosa, Ferreira, Mário Behring, Tenório d'Albuquerque, Pereira Lima; eventos (Itambé, Conjuração Baiana, 1817, Independência, Questão Religiosa, Abolição, República, cisões de 1927/1973, Estado Novo, ditadura). Portugal: Oliveira Marques (*História da Maçonaria em Portugal*, *Dicionário de Maçonaria Portuguesa*), Ventura, Dias; Grande Oriente Lusitano; Revolução de 1820; 1910; Salazar (lei 1935). Angola, Moçambique, Cabo Verde, Goa.

### C06 — América hispânica, Espanha, Itália e Caribe
REHMLAC+ (revista aberta, Univ. de Costa Rica — coletar todos os números), CEHME (Centro de Estudios Históricos de la Masonería Española, Ferrer Benimeli — simpósios), Dialnet, Redalyc, SciELO es; Espanha (Ferrer Benimeli, Morales Ruiz, Tribunal Especial para la Represión de la Masonería e o Comunismo, Archivo de Salamanca/CDMH), México (Escocesses × Yorkinos, Juárez), Argentina/Chile (Lautaro, Sarmiento), Cuba (Martí, Céspedes, Gran Logia de Cuba), Venezuela, Colômbia, Peru, Porto Rico, Haiti, Rep. Dominicana, Filipinas (Rizal). Itália (Risorgimento, Garibaldi, Mazzini?, GOI, fascismo, P2: relatório da Comissão Anselmi — documento público), Mola, Conti, Cazzaniga (*Storia d'Italia, Annali 21: La Massoneria*).

### C07 — Princípios, simbolismo, esoterismo, religião, mulheres
Landmarks (Mackey, Pound, outras listas por GL), *Basic Principles* UGLE 1929, Convento de Lausanne 1875, debate de 1877 (GOdF), Grande Arquiteto, VLS, tolerância, laicidade; simbolismo (Wirth, Guénon, Boucher, Plantagenet, Mackey, Wilmshurst, Ward, MacNulty, Hall; acadêmicos: Mollier, Snoek); esoterismo (Rosa-Cruz, Martinismo, Willermoz, Cagliostro, Golden Dawn, Theosophy × co-maçonaria); religião: documentos papais (*In eminenti*, *Providas*, *Ecclesiam a Jesu Christo*, *Quo graviora*, *Humanum genus*, *Custodi di quella fede*, *Dall'alto dell'Apostolico Seggio*, CIC 1917 c.2335, CIC 1983 c.1374, Declaração CDF 1983, nota DDF 2023), posição de igrejas protestantes (Igreja da Inglaterra 1987, Batistas do Sul 1993, Metodistas), islã (fatwa Al-Azhar 1978), judaísmo; mulheres (lojas de adoção, Maria Deraismes, Le Droit Humain, Order of Women Freemasons, GLFF, femininas no Brasil, Prince Hall/Estrela do Oriente). Copiar documentos (vatican.va etc.).

### C08 — Referência, Wikipédia/Wikidata, museus, periódicos, audiovisual
Verbetes de enciclopédias abertas (Wikipédia em pt, en, fr, es, it, de, nl, sv, pl, ru — salvar HTML e usar sobretudo as referências), Britannica, Catholic Encyclopedia 1909 (DP), Jewish Encyclopedia (DP), *Encyclopaedia Britannica* 1911 (DP); dicionários maçônicos (Mackey, Coil, Ligou, Daniel Ligou, Oliveira Marques, Ferrer Benimeli, Lennhoff-Posner *Internationales Freimaurerlexikon* 1932 — DP?); Wikidata: SPARQL de potências maçônicas, lojas, maçons notáveis com referência (exportar como dataset `data/fontes` tipo `dataset` + cópia CSV/JSON no acervo); museus e bibliotecas (Library and Museum of Freemasonry, Scottish Rite Masonic Museum & Library, House of the Temple, Musée de la Franc-maçonnerie Paris, Deutsches Freimaurermuseum, Museu do GOB/Palácio do Lavradio, Biblioteca Nacional de España — fundo maçônico, Klossiana Haia — catálogos online); periódicos (inventário em `docs/pesquisa/acervos-e-periodicos.md`: título, editor, anos, acesso, URL); audiovisual (documentários, palestras acadêmicas — só metadados).

### I01 — Infraestrutura
Baseado no `mapadosorixas` (clone de leitura: `https://github.com/aureliosaraiva/mapadosorixas`, pasta `site/` e `scripts/`): (1) site estático Astro com páginas: início com busca (Pagefind), catálogo de fontes filtrável (lê `data/fontes/*.json`), listagem e página de verbete (lê `data/verbetes/**/*.md`), linha do tempo (lê `data/linha_do_tempo.json`), grafo Cytoscape.js (lê `relacionados` dos verbetes e `data/conexoes.json`), metodologia; funcionar com 0 verbetes (dados de exemplo só em `tests/`); (2) `schemas/verbete.schema.json` + `scripts/validar_verbetes.py` (front matter, `fontes` existentes no catálogo, `relacionados` existentes, sem palavras de passe — lista de alerta configurável) e esquema/validador de `data/linha_do_tempo.json`; (3) `scripts/anticopia.py` portado (n-gramas contra `../fontes-maconaria/txt/<source_id>.txt` das fontes citadas); (4) `scripts/qa_site.py` (nenhum texto/arquivo do acervo no build); (5) workflow `.github/workflows/validar.yml` (validadores + build) — **sem** deploy por enquanto (deploy de Pages depende da decisão do autor sobre a `main`; registrar em PENDENCIAS); (6) `site/README.md`. Não editar `data/` nem docs de outras sessões.

## Ondas 2 e 3 (definidas em 2026-11-03 pela orquestradora)

Ordem de disparo (no máximo 3 sessões simultâneas, por limite de uso): **V05, V01, V02 → R01, A01, V03, V04 → V06, A02, V07 → A03, V08**. Onda 3 (verbetes) e onda 2 (aprofundamento) intercaladas, para o conteúdo da enciclopédia aparecer cedo.

| ID | Onda | Escopo | Arquivos de que é dona | Status | Relatório |
|---|---|---|---|---|---|
| R01 | 2 | **Reescrita dos resumos do catálogo** que reproduzem trechos da própria fonte (108 apontados pela I01 com `scripts/anticopia.py --com-catalogo`; 94 no c06/REHMLAC+, mais os 340 resumos automáticos da REHMLAC+): paráfrase de 2–4 frases a partir do texto no acervo | campo `resumo` em `data/fontes/*.json` (só esse campo; avisar no relatório) | pendente | — |
| A01 | 2 | Aprofundamento Brasil/lusófono: rituais brasileiros do séc. XIX (Moderno, Adonhiramita, REAA, Rito Brasileiro 1878/1914/1968), Estado Novo, cisões 1927/1973, maçonaria mista/feminina no Brasil, PALOP/Goa, lei portuguesa 1935; nova tentativa em BN Digital, SciELO, BDTD, RCAAP | `data/fontes/a01-lusofono2.json` | pendente | — |
| A02 | 2 | Lacunas mundo: nazismo, URSS, franquismo, Prince Hall (Delany 1853, Upton 1899), França 1870–1940 (Lausanne 1875, GOdF 1877, caso das fichas 1904), RER/Estrita Observância/Clermont, edições de Old Charges (QCA, Knoop-Jones-Hamer), listas alternativas de landmarks, islã/ortodoxia | `data/fontes/a02-mundo2.json` | pendente | — |
| A03 | 2 | Periódicos e literatura acadêmica: OpenAlex/Crossref (nova tentativa), JRFF, *Heredom*, AQC aberto, Pietre-Stones, REHMLAC+ completa, *Renaissance Traditionnelle*, *Chroniques d'histoire maçonnique*, teses (theses.fr, ProQuest abertos, EThOS) | `data/fontes/a03-periodicos.json` | pendente | — |
| V01 | 3 | Verbetes de **ritos, graus e ordens anexas** | `data/verbetes/ritos/`, `data/verbetes/graus/`, `data/verbetes/ordens-anexas/`, `data/linha_do_tempo/V01.json` | em andamento | — |
| V02 | 3 | Verbetes de **potências** (Brasil e mundo) + `conceitos/regularidade-e-reconhecimento` (com fichamento da série COGMNA) | `data/verbetes/potencias/`, `data/verbetes/conceitos/regularidade-e-reconhecimento.md`, `data/linha_do_tempo/V02.json` | em andamento | — |
| V03 | 3 | Verbetes de **documentos** (Old Charges, constituições, exposições, bulas e documentos eclesiásticos, landmarks, Basic Principles) | `data/verbetes/documentos/`, `data/linha_do_tempo/V03.json` | pendente | — |
| V04 | 3 | Verbetes de **eventos mundiais e antimaçonaria** | `data/verbetes/eventos/`, `data/verbetes/antimaconaria/`, `data/linha_do_tempo/V04.json` | pendente | — |
| V05 | 3 | Verbetes do **Brasil e mundo lusófono** (eventos, potências não, só história) | `data/verbetes/brasil/`, `data/linha_do_tempo/V05.json` | em andamento | — |
| V06 | 3 | Verbetes de **princípios, símbolos e conceitos** (exceto regularidade) | `data/verbetes/principios/`, `data/verbetes/simbolos/`, `data/verbetes/conceitos/` (exceto o da V02), `data/linha_do_tempo/V06.json` | pendente | — |
| V07 | 3 | Verbetes de **personalidades e lugares** (filiação com fonte documental; lendas marcadas) | `data/verbetes/personalidades/`, `data/verbetes/lugares/`, `data/linha_do_tempo/V07.json` | pendente | — |
| V08 | 3 | **Integração**: glossário, revisão cruzada de `relacionados` (links quebrados), conexões extras (`data/conexoes.json`), consolidação da linha do tempo, auditoria de sigilo (regra 5) e anti-cópia global | `data/glossario.json`, `data/conexoes.json`, `docs/sessoes/V08.md` (+ correções pontuais avisadas no relatório) | pendente | — |

### Instruções comuns às sessões de verbetes (V01–V07)
1. Siga `CLAUDE.md` e `docs/verbetes-guia.md`. Leia as sugestões de verbetes dos relatórios `docs/sessoes/C0*.md` e a taxonomia; monte primeiro a **lista de verbetes** da sua família (em `docs/sessoes/<ID>.md`, seção "Plano") e escreva por prioridade.
2. **Leia o texto no acervo** (`../fontes-maconaria/txt/<source_id>.txt`) antes de afirmar; cite página/seção. Paráfrase sempre; nada de palavras de passe, sinais, toques e juramentos (regra 5); lendas marcadas como lendas; divergências lado a lado.
3. Fonte que faltar e for aberta: pode catalogar num lote próprio `data/fontes/<id-da-sessão-minúsculo>.json` (ex.: `v01.json`) e copiar no acervo (`indices/<id>.json`).
4. Linha do tempo: cada sessão grava só o seu fragmento `data/linha_do_tempo/<ID>.json` = `{"eventos": [{"data": "1717-06-24", "precisao": "dia|mes|ano|decada|seculo", "titulo": "...", "verbete": "<id>", "paises": [...], "fontes": ["source_id"], "nota": "..."}]}` (datas incertas: `precisao` e nota).
5. Valide com `python3 scripts/validar_fontes.py` e, se já existir (sessão I01), `python3 scripts/validar_verbetes.py` e `python3 scripts/anticopia.py` — 0 erros antes de cada push. Commits a cada 3–5 verbetes.
6. Meta: 20–40 verbetes bem fontados por sessão (qualidade > quantidade). Relatório com verbetes feitos, pendentes e fontes que faltam.

## Sessões ativas (registro de IDs claude.ai/code)
> Atualizada a cada disparo/conclusão pelo ciclo de orquestração (`docs/ORQUESTRADOR.md`). Máximo de 3 `em andamento`.

| ID | Sessão | Status | Desde |
|---|---|---|---|
| C01 | `session_011fM5cigkddqRnQGmh6CcfR` | concluída | 2026-11-02 |
| C02 | `session_011fM5cj4Bj5nKuAL6cRn9PE` | concluída | 2026-11-02 |
| C03 | `session_011fM5cjAKKGbu4bttUNBBPd` | concluída | 2026-11-02 |
| C04 | `session_011fM5ckbgb8ZriFHDKUgGYG` | concluída | 2026-11-02 |
| C05 | `session_011fM5cnDpjyJhXfF3huBCJS` | concluída | 2026-11-02 |
| C06 | `session_011fM5cinwwrD4QhYxqG2J69` | concluída | 2026-11-02 (retomada 2026-11-12) |
| C07 | `session_011fM5ckBeU4EZtKrUUXX7Bx` | concluída | 2026-11-02 |
| C08 | `session_011fM5ciDEAUpHL3T5LWaVtG` | concluída | 2026-11-02 (retomada 2026-11-12) |
| I01 | `session_011fM5cj3PMZJKToLirjYtNU` | concluída | 2026-11-02 (retomada 2026-11-12) |
| V05 | `session_011fM5cjXSZuEitx2oa2VnZz` | em andamento | 2026-11-12 |
| V01 | `session_011fM5cinVfNKUkv4RYhrBZe` | em andamento | 2026-11-12 |
| V02 | `session_011fM5cisYWgkY8m5wJGBkLh` | em andamento | 2026-11-12 |

## Registro da orquestradora
- 2026-11-02 22:27 UTC — as 9 sessões da onda 1 pararam ~2 min após o início: **limite de uso de 5 h da conta** (sem perda no repositório; nada tinha sido empurrado).
- 2026-11-03 07:16 UTC — retomada **em lotes de 3 sessões simultâneas** para não estourar o limite: lote 1 = C01, C05, C02; lote 2 = C03, C04, C07; lote 3 = C06, C08, I01. Cada lote começa quando o anterior conclui (ou trava).
- 2026-11-03 19:24 UTC — C06, C08 e I01 pararam de novo pelo limite de uso; os check-ins agendados na sessão orquestradora só foram entregues em 2026-11-12 (sessão ociosa não acorda). **Correção:** ciclo de orquestração sem estado (`docs/ORQUESTRADOR.md`) executado por tarefa agendada recorrente que abre uma sessão nova a cada 2 h.
