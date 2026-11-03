// Plugin remark dos verbetes (data/verbetes/**/*.md):
//  - [[id]] ou [[id|rótulo]] vira link para /verbetes/<id>/ quando o verbete existe;
//    senão fica como texto (rótulo ou id) — o validador avisa;
//  - dentro das notas de rodapé ([^n]: ...), cada source_id do catálogo vira link para
//    /fontes/<id>/.
// Os ids existentes são lidos do disco (data/fontes/*.json e data/verbetes/**/*.md).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

function idsFontes() {
  const dir = path.join(RAIZ, 'data', 'fontes');
  const ids = new Set();
  if (!fs.existsSync(dir)) return ids;
  for (const n of fs.readdirSync(dir)) {
    if (!n.endsWith('.json')) continue;
    try {
      for (const f of JSON.parse(fs.readFileSync(path.join(dir, n), 'utf8')).fontes || []) ids.add(f.id);
    } catch { /* lote inválido: o validador de fontes acusa */ }
  }
  return ids;
}

function idsVerbetes() {
  const ids = new Set();
  const andar = (d) => {
    if (!fs.existsSync(d)) return;
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      if (e.isDirectory()) andar(path.join(d, e.name));
      else if (e.name.endsWith('.md') && !/^(readme|leiame)\.md$/i.test(e.name)) ids.add(e.name.slice(0, -3));
    }
  };
  andar(path.join(RAIZ, 'data', 'verbetes'));
  return ids;
}

const WIKI = /\[\[([a-z0-9]+(?:-[a-z0-9]+)*)(?:\|([^\]]+))?\]\]/g;
const TOKEN = /[a-z0-9]+(?:-[a-z0-9]+)+/g;

function dividir(valor, re, fazer) {
  const out = [];
  let ult = 0;
  for (const m of valor.matchAll(re)) {
    const no = fazer(m);
    if (!no) continue;
    if (m.index > ult) out.push({ type: 'text', value: valor.slice(ult, m.index) });
    out.push(no);
    ult = m.index + m[0].length;
  }
  if (!out.length) return null;
  if (ult < valor.length) out.push({ type: 'text', value: valor.slice(ult) });
  return out;
}

export default function remarkEnciclopedia({ base = '/' } = {}) {
  const b = base.endsWith('/') ? base : base + '/';
  return (tree) => {
    const fontes = idsFontes();
    const verbetes = idsVerbetes();
    const andar = (no, emNota) => {
      if (!no.children) return;
      const nota = emNota || no.type === 'footnoteDefinition';
      const novos = [];
      for (const filho of no.children) {
        if (filho.type === 'text') {
          let partes = dividir(filho.value, WIKI, (m) => verbetes.has(m[1])
            ? { type: 'link', url: `${b}verbetes/${m[1]}/`, children: [{ type: 'text', value: m[2] || m[1] }] }
            : { type: 'text', value: m[2] || m[1] });
          partes = partes || [filho];
          if (nota) {
            partes = partes.flatMap((p) => (p.type === 'text'
              ? dividir(p.value, TOKEN, (m) => (fontes.has(m[0])
                ? { type: 'link', url: `${b}fontes/${m[0]}/`, data: { hProperties: { className: ['ref-fonte'] } }, children: [{ type: 'text', value: m[0] }] }
                : null)) || [p]
              : [p]));
          }
          novos.push(...partes);
        } else {
          if (filho.type !== 'link') andar(filho, nota);
          novos.push(filho);
        }
      }
      no.children = novos;
    };
    andar(tree, false);
  };
}
