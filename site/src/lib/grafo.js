// Elementos do grafo (Cytoscape): nós = verbetes; arestas = `relacionados` + data/conexoes.json.
import { verbetes, arestasGrafo, url } from './dados.js';

export const CORES_CATEGORIA = {
  ritos: '#4d6fae', graus: '#7d5ea3', potencias: '#b0503c', documentos: '#8a6215', principios: '#4f7a45',
  simbolos: '#c19a2e', eventos: '#3b8686', brasil: '#2f8f4e', personalidades: '#b05f8a', lugares: '#6b7280',
  'ordens-anexas': '#9b6b3d', antimaconaria: '#5b5b5b', conceitos: '#3d7ab0',
};
export const corCategoria = (c) => CORES_CATEGORIA[c] || '#888888';

export function elementosGrafo() {
  const arestas = arestasGrafo();
  const grau = {};
  for (const a of arestas) { grau[a.origem] = (grau[a.origem] || 0) + 1; grau[a.destino] = (grau[a.destino] || 0) + 1; }
  const nos = verbetes.map((v) => ({ data: {
    id: v.id, label: v.titulo, categoria: v.categoria, cor: corCategoria(v.categoria),
    tam: 18 + Math.min(30, (grau[v.id] || 0) * 3), href: url(`verbetes/${v.id}`),
  } }));
  const ares = arestas.map((a, i) => ({ data: {
    id: `e${i}`, source: a.origem, target: a.destino, rel: a.rel, tipo: a.tipo,
    seta: a.tipo === 'conexao' && a.direcionada ? 'triangle' : 'none',
  } }));
  return { nos, arestas: ares, lista: arestas };
}
