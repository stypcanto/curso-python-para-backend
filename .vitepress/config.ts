import { defineConfig } from 'vitepress'
import type MarkdownIt from 'markdown-it'
import { readFileSync, readdirSync, existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

// ╔══════════════════════════════════════════════════════════╗
// ║  AJUSTA SOLO ESTO POR CURSO                               ║
// ║  (el color de marca se cambia en theme/custom.css)       ║
// ╚══════════════════════════════════════════════════════════╝
const CURSO = 'Python para Backend'

// Raíz del proyecto (una carpeta arriba de /.vitepress)
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')

// Secciones estándar de un curso (estilo Styp). En el sidebar
// SOLO aparecen las carpetas que existen y tienen algún .md,
// así la misma config sirve para cualquier curso sin tocarla.
// 'agrupar: true' → los .md de esa carpeta se reparten en subgrupos plegables
// según su frontmatter 'categoria'. 'orden' fija el orden de las categorías
// (las no listadas van al final, alfabéticas). Útil para 06-Errores.
const SECCIONES: Array<{ carpeta: string; texto: string; agrupar?: boolean; orden?: string[] }> = [
  { carpeta: '01-Clases', texto: '📚 Clases' },
  { carpeta: '00-Notas', texto: '🗒️ Notas' },
  { carpeta: '05-Snippets', texto: '🧩 Snippets' },
  { carpeta: '03-Proyectos', texto: '🚀 Proyectos' },
  { carpeta: '06-Errores', texto: '❌ Errores resueltos', agrupar: true, orden: [] },
  { carpeta: '90-Resumen', texto: '📝 Resumen' },
]

// ─────────────────────────────────────────────────────────────
// Plugin: convierte los blockquotes con emoji (⚠️ 💡 🧪 📌 …) en
// "callouts" de colores. Detecta el primer emoji y le pone clase.
// ─────────────────────────────────────────────────────────────
const CALLOUTS: Array<[string, string]> = [
  ['⚠️', 'warning'],
  ['⚠', 'warning'],
  ['💡', 'tip'],
  ['🧪', 'interview'],
  ['🎤', 'interview'],
  ['📌', 'note'],
  ['📝', 'note'],
  ['❓', 'question'],
  ['🎯', 'goal'],
]

function calloutsPlugin(md: MarkdownIt) {
  md.core.ruler.push('emoji_callouts', (state) => {
    const tokens = state.tokens
    for (let i = 0; i < tokens.length; i++) {
      if (tokens[i].type !== 'blockquote_open') continue
      let text = ''
      for (let j = i + 1; j < tokens.length && tokens[j].type !== 'blockquote_close'; j++) {
        if (tokens[j].type === 'inline' && tokens[j].content) {
          text = tokens[j].content.trimStart()
          break
        }
      }
      let cls = 'info'
      for (const [emoji, name] of CALLOUTS) {
        if (text.startsWith(emoji)) {
          cls = name
          break
        }
      }
      tokens[i].attrJoin('class', `callout callout-${cls}`)
    }
    return true
  })
}

// ─────────────────────────────────────────────────────────────
// Escapa `{{ }}` SOLO en el contenido (texto e inline code) para que
// VitePress (Vue) no lo interprete como interpolación. Imprescindible
// en cursos de frameworks que usan esa sintaxis (Angular, Vue, Handlebars).
// Sin esto, el build FALLA con "Error parsing JavaScript expression".
// Los bloques ``` ``` ya son seguros (VitePress los pone v-pre).
// Es inofensivo en cursos sin `{{ }}` (no cambia nada).
// ─────────────────────────────────────────────────────────────
function escaparInterpolacionPlugin(md: MarkdownIt) {
  const escapar = (html: string) =>
    html.replace(/\{\{/g, '&#123;&#123;').replace(/\}\}/g, '&#125;&#125;')
  const textRule = md.renderer.rules.text!
  md.renderer.rules.text = (tokens, idx, options, env, self) =>
    escapar(textRule(tokens, idx, options, env, self))
  const codeInlineRule = md.renderer.rules.code_inline!
  md.renderer.rules.code_inline = (tokens, idx, options, env, self) =>
    escapar(codeInlineRule(tokens, idx, options, env, self))
}

// ─────────────────────────────────────────────────────────────
// Sidebar automático: lee cada carpeta y crea un item por .md,
// usando su primer "# ..." como título. Un archivo nuevo aparece
// solo, sin tocar esta config.
// ─────────────────────────────────────────────────────────────
// Lee el frontmatter YAML (--- ... ---) de un .md como pares clave: valor.
function leerFrontmatter(rutaAbs: string): Record<string, string> {
  try {
    const m = readFileSync(rutaAbs, 'utf-8').match(/^---\r?\n([\s\S]*?)\r?\n---/)
    if (!m) return {}
    const fm: Record<string, string> = {}
    for (const linea of m[1].split('\n')) {
      const mm = linea.match(/^(\w+):\s*(.*)$/)
      if (mm) fm[mm[1]] = mm[2].trim().replace(/^["']|["']$/g, '')
    }
    return fm
  } catch {
    return {}
  }
}

// Título del item: 'sidebar' del frontmatter (etiqueta corta) si existe;
// si no, el primer "# ..." del archivo; si no, el fallback.
function tituloDe(rutaAbs: string, fallback: string): string {
  const fm = leerFrontmatter(rutaAbs)
  if (fm.sidebar) return fm.sidebar
  try {
    for (const linea of readFileSync(rutaAbs, 'utf-8').split('\n')) {
      const m = linea.match(/^#\s+(.*)$/)
      if (m) return m[1].trim()
    }
  } catch {}
  return fallback
}

function itemsDeCarpeta(carpeta: string) {
  const abs = join(ROOT, carpeta)
  if (!existsSync(abs)) return []
  return readdirSync(abs)
    .filter((f) => f.endsWith('.md') && f.toLowerCase() !== 'index.md')
    .sort((a, b) => a.localeCompare(b, 'es'))
    .map((f) => {
      const slug = f.replace(/\.md$/, '')
      return { text: tituloDe(join(abs, f), slug), link: `/${carpeta}/${slug}` }
    })
}

// Como itemsDeCarpeta, pero AGRUPA los .md en subgrupos plegables según su
// frontmatter 'categoria' (default "Otros"). Un archivo nuevo cae solo en su
// grupo con solo declarar su 'categoria'.
function subgruposDeCarpeta(carpeta: string, ordenCategorias: string[] = []) {
  const abs = join(ROOT, carpeta)
  if (!existsSync(abs)) return []
  const grupos: Record<string, Array<{ text: string; link: string }>> = {}
  for (const f of readdirSync(abs)
    .filter((f) => f.endsWith('.md') && f.toLowerCase() !== 'index.md')
    .sort((a, b) => a.localeCompare(b, 'es'))) {
    const absPath = join(abs, f)
    const cat = leerFrontmatter(absPath).categoria || 'Otros'
    const slug = f.replace(/\.md$/, '')
    ;(grupos[cat] ||= []).push({ text: tituloDe(absPath, slug), link: `/${carpeta}/${slug}` })
  }
  const orden = (c: string) => {
    const i = ordenCategorias.indexOf(c)
    return i === -1 ? 999 : i
  }
  return Object.keys(grupos)
    .sort((a, b) => orden(a) - orden(b) || a.localeCompare(b, 'es'))
    .map((cat) => ({ text: cat, collapsed: true, items: grupos[cat] }))
}

// Solo secciones con contenido real
const sidebar = SECCIONES
  .map((s) => ({
    text: s.texto,
    collapsed: false,
    items: s.agrupar ? subgruposDeCarpeta(s.carpeta, s.orden) : itemsDeCarpeta(s.carpeta),
  }))
  .filter((s) => s.items.length > 0)

// Primer enlace disponible (para el botón del hero / nav)
const primerLink = sidebar[0]?.items[0]?.link ?? '/'

export default defineConfig({
  title: `Apuntes de ${CURSO}`,
  description: `Notas y apuntes de mi autoestudio de ${CURSO}.`,
  lang: 'es',
  // Iconos del sitio. Coloca favicon.ico / favicon.png / apple-touch-icon.png
  // en la carpeta public/ (VitePress los sirve en la raíz). Si no tienes iconos,
  // borra este bloque o el sitio usará el favicon por defecto de VitePress.
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico', sizes: 'any' }],
    ['link', { rel: 'icon', type: 'image/png', href: '/favicon.png' }],
    ['link', { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' }],
  ],
  lastUpdated: true,
  cleanUrls: true,
  srcExclude: [
    '**/README.md', '**/CLAUDE.md', '**/node_modules/**', 'deploy/**',
    // Entornos virtuales de Python: la mayoría se llaman .venv (VitePress ya
    // ignora dotfiles/dot-folders por defecto), pero 02-Ejercicios/Clase-03/
    // usa "venv" sin punto — sin este patrón, los LICENSE.md de sus paquetes
    // instalados (site-packages) se compilan como páginas y se publican.
    '**/venv/**', '**/__pycache__/**',
  ],
  markdown: {
    lineNumbers: false,
    config: (md) => {
      md.use(calloutsPlugin)
      md.use(escaparInterpolacionPlugin)
    },
  },
  themeConfig: {
    outline: { label: 'En esta página', level: [2, 3] },
    docFooter: { prev: 'Anterior', next: 'Siguiente' },
    darkModeSwitchLabel: 'Apariencia',
    lightModeSwitchTitle: 'Cambiar a modo claro',
    darkModeSwitchTitle: 'Cambiar a modo oscuro',
    sidebarMenuLabel: 'Menú',
    returnToTopLabel: 'Volver arriba',
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: 'Buscar', buttonAriaLabel: 'Buscar' },
          modal: {
            noResultsText: 'Sin resultados para',
            resetButtonTitle: 'Limpiar búsqueda',
            footer: { selectText: 'seleccionar', navigateText: 'navegar', closeText: 'cerrar' },
          },
        },
      },
    },
    nav: [
      { text: '🏠 Inicio', link: '/' },
      { text: '📚 Empezar', link: primerLink },
    ],
    sidebar,
    socialLinks: [],
  },
})
