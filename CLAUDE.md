# Projeto: Enciclopédia da Maçonaria (mapa-maconaria)

## Contexto
- Projeto irmão do `aureliosaraiva/mapadosorixas` (mesmo método: fontes citadas por afirmação, acervo privado de texto integral, divergências lado a lado, sessões autônomas coordenadas por uma orquestradora).
- Objetivo: reunir **todo conteúdo acessível** sobre maçonaria, em **qualquer idioma** — ritos, rituais, graus, princípios/dogmas, simbolismo, potências (obediências), documentos fundadores, eventos marcantes no Brasil e no mundo, personalidades, antimaçonaria — e apresentá-lo como **enciclopédia** com fontes.
- Dois repositórios:
  - **`aureliosaraiva/mapa-maconaria` (PÚBLICO)** — este: catálogo de fontes, fichamento, verbetes da enciclopédia, linha do tempo, grafo e site. **Nunca** contém texto integral de obra protegida.
  - **`aureliosaraiva/fontes-maconaria` (PRIVADO)** — acervo: cópia do conteúdo (PDF, HTML salvo, texto convertido) de tudo que foi coletado, para leitura, releitura e anti-cópia. Não tornar público. Ver `LEIAME.md` dele.

## Idioma de trabalho
Português do Brasil em tudo (documentação, verbetes, commits). Fontes em qualquer idioma; nomes próprios e títulos no original, com tradução quando útil.

## Regras de conteúdo (obrigatórias)
1. **Fonte por afirmação.** Todo dado factual de um verbete aponta para `source_id` do catálogo (`data/fontes/`), com página/seção quando houver.
2. **Paráfrase sempre** no repositório público. Citação literal só de obra em domínio público, curta (≤ 2 frases) e marcada entre aspas com fonte. Texto integral só no acervo privado.
3. **Pluralidade explícita.** Maçonaria não é uma só: registre divergências por **potência, rito, país e época** lado a lado (ex.: regular × liberal; GADU obrigatório × facultativo; mulheres; landmarks de Mackey × outras listas), sem eleger uma versão "correta".
4. **Etiquetagem.** Toda informação é etiquetada com rito(s), potência(s), país e período a que se refere (vocabulários em `docs/taxonomia.md`).
5. **Rituais e segredo.** Fontes de ritual são catalogadas e copiadas no acervo quando **já publicadas** (exposições históricas como Prichard 1730, Duncan 1866; rituais impressos e vendidos publicamente; monitores; edições acadêmicas). No **site**, verbetes descrevem estrutura, temas, lendas e simbolismo dos graus conforme a literatura publicada, **sem reproduzir** palavras de passe, sinais, toques e juramentos por extenso. Na dúvida, não publicar e registrar em `PENDENCIAS.md`.
6. **Neutralidade.** Nem apologia nem denúncia. Antimaçonaria e teorias conspiratórias (Taxil, *Protocolos*, Barruel, "Illuminati") são verbetes históricos, tratados criticamente com fontes acadêmicas. Afirmações de "fulano era maçom" exigem fonte documental (ata, registro de loja, biografia acadêmica); lendas ficam marcadas como lendas.
7. **Confiabilidade.** Cada fonte recebe nota A–D (A: documento primário editado/acadêmica revisada; B: historiografia maçônica séria, ex. *Ars Quatuor Coronatorum*; C: divulgação/site oficial de potência — ótimo para dados institucionais, fraco para história; D: blog/anônimo — só pista).
8. **Sem pirataria.** Coletar só o que é acessível legalmente: domínio público, acesso aberto, sites oficiais, páginas públicas. **Nunca** LibGen, Anna's Archive, Z-Library, Sci-Hub, nem contornar paywall/anti-robô. Obra só comercial/impressa → catálogo com `acesso: comercial` + `COLETA.md` do acervo.

## Registro de bloqueios
Todo bloqueio (domínio fora, 403/404, paywall, obra impressa, dúvida de sigilo, conferência que depende de pessoa) vai para `docs/pesquisa/PENDENCIAS.md` com status, o que está atrás do bloqueio e prioridade. Nunca substituir por conteúdo inventado.

## Branch de trabalho (tronco)
**Decisão do autor (2026-11-02): commit e push SEMPRE direto na `main`, nos DOIS repositórios.** Não usar outros branches, não criar PR. Push com rebase, pois várias sessões empurram ao mesmo tempo:
`git pull --rebase origin main && git push -u origin HEAD:main` (repita com espera 2/4/8/16 s se houver corrida com outra sessão).

## Fluxo de cada sessão trabalhadora
1. **Abertura:** `git pull --rebase` do tronco; ler `docs/ESTADO.md`, `docs/ORQUESTRACAO.md` (sua linha: ID, escopo, arquivos que só você edita) e `docs/taxonomia.md`. Anexar o acervo: `add_repo(owner="aureliosaraiva", repo="fontes-maconaria", access="push")` e `scripts/acervo_sync.sh pull` (clone em `../fontes-maconaria`; outro lugar: `ACERVO_DIR`).
2. **Escopo:** uma sessão = uma tarefa fechada (um lote de coleta, uma família de verbetes, uma fase de infra). **Só edite os arquivos que o `ORQUESTRACAO.md` atribui à sua sessão**; arquivos compartilhados (`docs/ESTADO.md`, `docs/ORQUESTRACAO.md`, `PENDENCIAS.md`) só com edição pequena e localizada, perto do fim, seguida de pull/rebase imediato.
3. **Commits frequentes** (a cada lote útil, ~30–60 min de trabalho): a sessão pode ser interrompida a qualquer momento; o que não foi empurrado se perde. Mensagem: `[<ID-da-sessão>] <resumo>`.
4. **Fechamento:** `python3 scripts/validar_fontes.py` (0 erros), relatório em `docs/sessoes/<ID>.md` (o que fez, números, bloqueios, sugestões de próximas tarefas), atualizar sua linha no `ORQUESTRACAO.md` (status `concluída` + link do relatório), acrescentar bloqueios ao `PENDENCIAS.md`, `scripts/acervo_sync.sh push`, commit e push. Último commit: `[orq:<ID> concluída] <resumo>`.

## Catálogo de fontes (fragmentado para paralelismo)
- Um arquivo por lote: `data/fontes/<lote>.json` = `{"lote": "...", "fontes": [ ... ]}`; cada sessão de coleta só edita o seu. Esquema: `schemas/fonte.schema.json`.
- `id` único global: `<sobrenome-ou-org>-<ano>-<palavra>` em minúsculas sem acento (ex.: `anderson-1723-constitutions`, `gob-2022-constituicao`). Antes de criar, procure duplicata em todos os lotes (`python3 scripts/validar_fontes.py --buscar <termo>`); se a fonte já existir em outro lote, não duplique — cite o `id` existente.
- `status_verificacao`: `pista` (só referência) → `conferido_web` (metadados conferidos) → `copiado` (cópia no acervo) → `fichado` (lido e extraído) → `revisado`.

## Acervo (repositório privado `fontes-maconaria`)
- Arquivos nomeados pelo `source_id`: `pdf/<id>.pdf`, `html/<id>.html` (página salva), `txt/<id>.txt` (texto convertido: `pdftotext -layout` ou extração de HTML; hifenização de fim de linha desfeita).
- Metadados por lote: `indices/<lote>.json` (lista de `{id, arquivo, url_origem, data, sha256, paginas, palavras, licenca, obs}`); `python3 scripts/gerar_indice.py` (no acervo) gera `INDICE.md`. PDF > 15 MB: guardar só o `txt` e registrar a URL (o acervo já passa de 0,5 GB; limite de tamanho do GitHub).
- Obra que exige ação humana (impressa, comprada, biblioteca) → `COLETA.md` do acervo, em ordem de prioridade.

## Verbetes (enciclopédia)
- `data/verbetes/<categoria>/<id>.md` com front matter YAML (esquema e exemplo em `docs/verbetes-guia.md`). Categorias: `ritos`, `graus`, `potencias`, `documentos`, `principios`, `simbolos`, `eventos`, `brasil`, `personalidades`, `lugares`, `ordens-anexas`, `antimaconaria`, `conceitos`.
- Corpo em prosa enciclopédica, parafraseada, com notas `[^n]` que apontam `source_id` + página. Divergências em seção própria.

## Paralelismo
Sessões simultâneas só em arquivos diferentes. O `ORQUESTRACAO.md` é a fonte de verdade de quem é dono de quê. A sessão orquestradora é a única que cria novas linhas/ondas no `ORQUESTRACAO.md` e reescreve o `ESTADO.md`.
