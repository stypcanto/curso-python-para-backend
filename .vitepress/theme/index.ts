import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import SidebarSearch from './SidebarSearch.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  // Inserta la caja de búsqueda ARRIBA del menú lateral (encima de "Clases").
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'sidebar-nav-before': () => h(SidebarSearch),
    })
  },
}
