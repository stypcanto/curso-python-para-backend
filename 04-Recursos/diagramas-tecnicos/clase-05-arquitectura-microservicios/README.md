# Diagrama técnico — Arquitectura de microservicios (Clase 5)

> Generado con el skill `diagram-design` (HTML + SVG inline), paleta por defecto.

## Qué muestra

Frontend → API Gateway (`localhost:8080`) → tres microservicios independientes
(`users`, `orders`, `products`), cada uno enrutado por path (`/api/users`, `/api/orders`,
`/api/products`). Los tres microservicios se dibujan con una conexión punteada a su propia
base de datos PostgreSQL — el patrón **Database per Service**, marcado como "patrón
objetivo" porque todavía no está conectado, es el punto de llegada que desarrolla la
sección 3 de `Clase-05.md`.

## Archivos

| Archivo | Qué es |
|---|---|
| `src/diagrama.html` | Fuente editable (HTML + SVG inline + CSS del skill `diagram-design`) |
| `svg/diagrama.svg` | Export standalone del `<svg>` |

La copia que sirve el sitio VitePress está en
`public/clase-05-diagrama-arquitectura-microservicios.svg`. Si se edita `src/diagrama.html`,
hay que volver a exportar el `<svg>` y copiar a `public/` — no se actualiza solo.

## Regenerar el SVG

```bash
python3 - << 'EOF'
import re
src = open("src/diagrama.html", encoding="utf-8").read()
svg = re.search(r'(<svg .*?</svg>)', src, re.S).group(1)
open("svg/diagrama.svg", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
EOF
cp svg/diagrama.svg ../../../public/clase-05-diagrama-arquitectura-microservicios.svg
```

> 📝 **No** agregues un `<style>@import url('fonts.googleapis.com/...')</style>` al SVG
> exportado — se probó y rompe el XML (el `&` de la URL de Google Fonts sin escapar) y el
> navegador no puede cargarlo como `<img>`: falla en silencio (`naturalWidth/Height: 0`,
> sin error visible en pantalla). Tampoco serviría de nada: los navegadores bloquean
> fuentes externas dentro de un SVG cargado como `<img>`. El SVG standalone se sirve
> directo desde `public/` con la tipografía de reserva (`sans-serif`/`monospace`) — sigue
> siendo legible, solo no carga Geist/Instrument Serif.
>
> No se generó PNG: `playwright` no está instalado en el entorno (`pip install
> playwright && playwright install chromium` lo habilitaría).
