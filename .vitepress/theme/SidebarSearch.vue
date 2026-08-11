<script setup lang="ts">
// Caja de búsqueda que se muestra ARRIBA del menú lateral (encima de "Clases").
// Al hacer clic abre el buscador local de VitePress, que indexa TODAS las
// páginas (clases, notas, errores) y muestra coincidencias por palabra.
function abrirBuscador() {
  // 1) Intento hacer clic en el botón de búsqueda del nav (buscador local).
  const btn =
    document.querySelector<HTMLElement>('#local-search button') ||
    document.querySelector<HTMLElement>('.DocSearch-Button') ||
    document.querySelector<HTMLElement>('.VPNavBarSearch button')
  if (btn) {
    btn.click()
    return
  }
  // 2) Fallback: simulo Cmd/Ctrl + K (atajo que abre el buscador).
  const esMac = /mac/i.test(navigator.userAgent)
  window.dispatchEvent(
    new KeyboardEvent('keydown', {
      key: 'k',
      code: 'KeyK',
      metaKey: esMac,
      ctrlKey: !esMac,
      bubbles: true,
    }),
  )
}
</script>

<template>
  <button
    class="apuntes-search"
    type="button"
    aria-label="Buscar en los apuntes"
    @click="abrirBuscador"
  >
    <span class="apuntes-search__icon" aria-hidden="true">🔎</span>
    <span class="apuntes-search__text">Buscar en los apuntes…</span>
    <kbd class="apuntes-search__kbd">⌘K</kbd>
  </button>
</template>
