// Leitura dos dados da raiz do repositório (data/). O site só exibe esses dados:
// nenhum conteúdo sobre maçonaria é escrito aqui. Tudo é opcional: o site compila
// com 0 verbetes, sem linha do tempo e sem conexões.
const lotesMod = import.meta.glob('../../../data/fontes/*.json', { eager: true });
const verbetesMod = import.meta.glob('../../../data/verbetes/**/*.md', { eager: true });
const linhaMod = import.meta.glob(['../../../data/linha_do_tempo/*.json', '../../../data/linha_do_tempo.json'], { eager: true });
const conexoesMod = import.meta.glob('../../../data/conexoes.json', { eager: true });
const glossarioMod = import.meta.glob('../../../data/glossario.json', { eager: true });

const valor = (m) => (m && m.default !== undefined ? m.default : m);

export const url = (p = '') => {
  const b = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/';
  return b + String(p).replace(/^\//, '');
};

// ---------------------------------------------------------------- fontes
export const lotes = Object.entries(lotesMod)
  .map(([caminho, m]) => ({ arquivo: caminho.split('/').pop(), ...valor(m) }))
  .filter((l) => Array.isArray(l.fontes));
const vistos = new Set();
export const fontes = lotes
  .flatMap((l) => l.fontes.map((f) => ({ ...f, lote: f.lote || l.lote || l.arquivo.replace(/\.json$/, '') })))
  .filter((f) => f && f.id && !vistos.has(f.id) && vistos.add(f.id))
  .sort((a, b) => autorCurto(a).localeCompare(autorCurto(b), 'pt-BR') || (a.ano ?? 0) - (b.ano ?? 0));
export const fontePorId = Object.fromEntries(fontes.map((f) => [f.id, f]));

export function autorCurto(f) {
  if (!f) return '?';
  const a = (f.autores || [])[0] || 'Anônimo';
  // "Nome Sobrenome" -> "Sobrenome"; organizações (com sigla ou muitas palavras) ficam inteiras
  const partes = a.trim().split(/\s+/);
  const nome = partes.length > 1 && partes.length <= 5 && !/[A-Z]{2,}/.test(a) && !/\b(de la|of|des|du)\b/i.test(a) ? partes[partes.length - 1] : a;
  return (f.autores || []).length > 2 ? `${nome} et al.` : (f.autores || []).length === 2 ? `${nome} e ${ultimo(f.autores[1])}` : nome;
}
function ultimo(a) { const p = a.trim().split(/\s+/); return p.length > 1 && !/[A-Z]{2,}/.test(a) ? p[p.length - 1] : a; }
export const anoFonte = (f) => (f?.ano ?? 's.d.');
export const citacaoCurta = (f) => `${autorCurto(f)} (${anoFonte(f)})`;

// ---------------------------------------------------------------- verbetes
export const verbetes = Object.entries(verbetesMod)
  .filter(([c]) => !/\/(readme|leiame)\.md$/i.test(c))
  .map(([caminho, m]) => {
    const fm = m.frontmatter || {};
    const id = fm.id || caminho.split('/').pop().replace(/\.md$/, '');
    return { ...fm, id, titulo: fm.titulo || id, categoria: fm.categoria || caminho.split('/').slice(-2, -1)[0], Content: m.Content, caminho };
  })
  .sort((a, b) => a.titulo.localeCompare(b.titulo, 'pt-BR'));
export const verbetePorId = Object.fromEntries(verbetes.map((v) => [v.id, v]));

// ---------------------------------------------------------------- linha do tempo
// Fragmentos por sessão (data/linha_do_tempo/<ID>.json) + legado data/linha_do_tempo.json.
// Evento sem id recebe '<arquivo>-<n>' (o mesmo de scripts/projeto.py: id_evento).
const slug = (t) => String(t).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim().replace(/ /g, '-');
const linhaJson = {
  eventos: Object.entries(linhaMod).sort(([a], [b]) => a.localeCompare(b)).flatMap(([caminho, m]) => {
    const d = valor(m) || {};
    const stem = caminho.split('/').pop().replace(/\.json$/, '');
    return (Array.isArray(d.eventos) ? d.eventos : []).map((e, i) => ({ ...e, id: e.id || `${slug(stem)}-${i + 1}` }));
  }),
};
export const chaveData = (d) => {
  if (d === null || d === undefined) return [0, 0, 0];
  if (d instanceof Date) d = d.toISOString().slice(0, 10);
  if (typeof d === 'number') return [d, 0, 0];
  const neg = String(d).startsWith('-');
  const p = String(d).replace(/^-/, '').split('-').map(Number);
  if (neg) p[0] = -p[0];
  return [p[0] || 0, p[1] || 0, p[2] || 0];
};
const cmpData = (a, b) => { const x = chaveData(a), y = chaveData(b); return x[0] - y[0] || x[1] - y[1] || x[2] - y[2]; };
export const eventos = [...(linhaJson.eventos || [])].sort((a, b) => cmpData(a.data, b.data) || a.titulo.localeCompare(b.titulo, 'pt-BR'));
export const MESES = ['jan.', 'fev.', 'mar.', 'abr.', 'maio', 'jun.', 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.'];
const ROMANOS = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI'];
export function formatarData(d, aproximada = false, precisao = undefined) {
  if (d === null || d === undefined || d === '') return '';
  const [a, m, dia] = chaveData(d);
  if (precisao === 'decada' && a > 0) return `década de ${Math.floor(a / 10) * 10}`;
  if (precisao === 'seculo' && a > 0) return `século ${ROMANOS[Math.floor((a - 1) / 100) + 1] || Math.floor((a - 1) / 100) + 1}`;
  if (precisao === 'ano' && a) return (aproximada ? 'c. ' : '') + String(a);
  if (precisao === 'mes' && a && m) return (aproximada ? 'c. ' : '') + `${MESES[m - 1]} ${a}`;
  if (!a && !m) return String(d);
  const ano = a < 0 ? `${-a} a.C.` : String(a);
  const s = dia ? `${dia} ${MESES[m - 1]} ${ano}` : m ? `${MESES[m - 1]} ${ano}` : ano;
  return aproximada ? `c. ${s}` : s;
}
export const anoDe = (d) => chaveData(d)[0];

// ---------------------------------------------------------------- conexões
const conexoesJson = valor(Object.values(conexoesMod)[0]) || { conexoes: [] };
export const conexoes = conexoesJson.conexoes || [];

// Arestas do grafo: `relacionados` do front matter + data/conexoes.json, só entre
// verbetes existentes (o validador avisa das pendentes).
export function arestasGrafo() {
  const out = [];
  const chave = new Set();
  for (const v of verbetes) {
    for (const r of v.relacionados || []) {
      if (!r || !verbetePorId[r.id] || r.id === v.id) continue;
      const k = [v.id, r.id].sort().join('|') + '|' + r.rel;
      if (chave.has(k)) continue;
      chave.add(k);
      out.push({ origem: v.id, destino: r.id, rel: r.rel, fontes: [], tipo: 'relacionado' });
    }
  }
  for (const c of conexoes) {
    if (!verbetePorId[c.origem] || !verbetePorId[c.destino]) continue;
    out.push({ ...c, tipo: 'conexao' });
  }
  return out;
}

// Verbetes que citam cada fonte (página da fonte)
export const citadaPor = {};
for (const v of verbetes) for (const s of v.fontes || []) (citadaPor[s] ||= []).push(v);
for (const e of eventos) for (const s of e.fontes || []) (citadaPor['__ev__' + s] ||= []).push(e);

// ---------------------------------------------------------------- glossário (sessão V08)
// Formato esperado: {"termos": [{"id", "termo", "definicao", "fontes": [...], "verbete"?, "variantes"?: [...]}]}
const glossarioJson = valor(Object.values(glossarioMod)[0]) || { termos: [] };
export const glossario = (glossarioJson.termos || [])
  .filter((t) => t && (t.termo || t.id))
  .map((t) => ({ ...t, id: t.id || slug(t.termo), termo: t.termo || t.id }))
  .sort((a, b) => a.termo.localeCompare(b.termo, 'pt-BR'));
