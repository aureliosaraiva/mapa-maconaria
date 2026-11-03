// @ts-check
import { defineConfig } from 'astro/config';
import remarkEnciclopedia from './src/lib/remark-enciclopedia.mjs';

// Publicação: GitHub Pages em https://aureliosaraiva.github.io/mapa-maconaria/ (workflow
// .github/workflows/deploy-pages.yml). SITE_BASE troca o subcaminho (SITE_BASE=/ para a raiz,
// ex.: domínio próprio); SITE_URL troca a origem. scripts/qa_site.py usa o mesmo SITE_BASE.
const BASE = (process.env.SITE_BASE ?? '/mapa-maconaria') || '/';
export default defineConfig({
  output: 'static',
  site: process.env.SITE_URL || 'https://aureliosaraiva.github.io',
  base: BASE,
  trailingSlash: 'ignore',
  build: { format: 'directory', inlineStylesheets: 'always' },
  markdown: {
    // [[id]] -> link para o verbete; source_id nas notas [^n] -> link para a fonte
    remarkPlugins: [[remarkEnciclopedia, { base: BASE }]],
    gfm: true,
  },
  vite: {
    // os dados ficam na raiz do repositório (data/), fora de site/
    server: { fs: { allow: ['..'] } },
  },
});
