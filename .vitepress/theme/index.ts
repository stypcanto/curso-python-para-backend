import DefaultTheme from 'vitepress/theme'
import { h, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vitepress'
import Viewer from 'viewerjs'
import 'viewerjs/dist/viewer.css'
import SidebarSearch from './SidebarSearch.vue'
import './custom.css'

// Visor de imágenes (zoom, pantalla completa, navegación) para los diagramas
// embebidos en las notas — ver skill crear-diagrama §14. Se re-engancha en
// cada navegación porque VitePress es una SPA (el contenido cambia sin recargar).
function montarVisorDeImagenes() {
  const contenedor = document.querySelector('.vp-doc')
  if (!contenedor) return

  const existente = (contenedor as any).__viewer__
  if (existente) existente.destroy()

  const visor = new Viewer(contenedor as HTMLElement, {
    toolbar: {
      zoomIn: true,
      zoomOut: true,
      oneToOne: true,
      reset: true,
      prev: true,
      play: false,
      next: true,
      rotateLeft: true,
      rotateRight: true,
      flipHorizontal: true,
      flipVertical: true,
    },
    navbar: true,
    title: true,
    movable: true,
    zoomable: true,
    tooltip: true,
    transition: true,
  })
  ;(contenedor as any).__viewer__ = visor
}

export default {
  extends: DefaultTheme,
  Layout: {
    setup() {
      const route = useRoute()

      onMounted(() => {
        nextTick(montarVisorDeImagenes)
      })
      watch(
        () => route.path,
        () => {
          nextTick(montarVisorDeImagenes)
        }
      )

      // Inserta la caja de búsqueda ARRIBA del menú lateral (encima de "Clases").
      return () =>
        h(DefaultTheme.Layout, null, {
          'sidebar-nav-before': () => h(SidebarSearch),
        })
    },
  },
}
