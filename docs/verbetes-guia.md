# Guia de verbetes

Arquivo: `data/verbetes/<categoria>/<id>.md`. `id` = slug sem acento (ex.: `rito-escoces-antigo-e-aceito`, `grande-oriente-do-brasil`, `questao-religiosa`). Um verbete por arquivo; a sessão dona da categoria é a única que edita aqueles arquivos.

## Front matter (YAML)

```yaml
---
id: questao-religiosa
titulo: Questão Religiosa (1872–1875)
categoria: brasil            # ritos|graus|potencias|documentos|principios|simbolos|eventos|brasil|personalidades|lugares|ordens-anexas|antimaconaria|conceitos
nomes_alternativos: ["Questão Epíscopo-Maçônica"]
resumo: >-                   # 1–3 frases, paráfrase
  Conflito entre bispos católicos e o governo imperial...
datas: {inicio: 1872, fim: 1875}           # eventos/documentos/potências (fundação/extinção); pessoas: nascimento/morte
paises: [br]
periodos: [p1871_1918]
ritos: []
potencias: [gob]
temas: [religiao, politica]
relacionados:                # alimentam o grafo; tipo de relação livre mas curto
  - {id: grande-oriente-do-brasil, rel: envolve}
  - {id: humanum-genus, rel: contexto}
fontes: [barata-1999-luzes, vieira-1980-bispo]     # source_ids usados (todos devem existir no catálogo)
status: rascunho            # rascunho|revisado
sensivel: false             # true se tocar em conteúdo ritual reservado (ver CLAUDE.md regra 5)
---
```

## Corpo
1. **Abertura** (1 parágrafo): o que é, quando, onde, para quem.
2. Seções conforme a categoria:
   - *rito*: origem e história; estrutura de graus (tabela); potências que o praticam (por país); características rituais e simbólicas (nível publicado); variantes; no Brasil.
   - *grau*: rito(s), posição, lenda/tema, simbolismo, variações entre ritos/potências.
   - *potência*: fundação, sede, jurisdição, ritos, membros (com data e fonte), reconhecimentos/regularidade, cisões, grão-mestres notáveis.
   - *evento*: antecedentes, fatos, atores, consequências, historiografia.
   - *documento*: datação, autoria, conteúdo (paráfrase), edições, onde está, importância.
   - *pessoa*: evidência documental da filiação (loja, data), atuação maçônica, mitos associados.
3. **Divergências** (quando houver): versões lado a lado com quem afirma o quê.
4. **Notas** `[^1]: source_id, p. X.` e **Ver também** (links `[[id]]`).

Regras: paráfrase; nada de palavras de passe/sinais/toques/juramentos por extenso; lendas marcadas como lendas; números com data e fonte.
