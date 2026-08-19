# Diagrama técnico — Comunicación síncrona vs asíncrona (Clase 5)

> Generado con el skill `diagram-design` (HTML + SVG inline), paleta por defecto (misma
> que `clase-05-arquitectura-microservicios/`, para mantener consistencia visual en la
> página).

## Qué muestra

Contrasta las dos formas en que los microservicios `users`, `orders`, `products` (ya
introducidos en el diagrama de arquitectura) se hablan entre sí:

- **Síncrono:** `orders` llama por **gRPC** a `users` y espera la respuesta.
- **Asíncrono:** `orders` publica el evento `order.created` en un *topic* de **Kafka**
  (broker, foco del diagrama); `products` y `notifications` lo consumen cada uno por su
  cuenta, sin que `orders` sepa quién escucha.

## Archivos

| Archivo | Qué es |
|---|---|
| `src/diagrama.html` | Fuente editable (HTML + SVG inline + CSS del skill `diagram-design`) |
| `svg/diagrama.svg` | Export standalone del `<svg>` |

La copia que sirve el sitio VitePress está en
`public/clase-05-diagrama-comunicacion-async.svg`. Si se edita `src/diagrama.html`, hay
que volver a exportar y copiar a `public/` — no se actualiza solo.

## Regenerar el SVG

```bash
python3 - << 'EOF'
import re
src = open("src/diagrama.html", encoding="utf-8").read()
svg = re.search(r'(<svg .*?</svg>)', src, re.S).group(1)
open("svg/diagrama.svg", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
EOF
cp svg/diagrama.svg ../../../public/clase-05-diagrama-comunicacion-async.svg
```

> 📝 A diferencia del primer diagrama de Clase 5, este **no** inyecta el `@import` de
> Google Fonts en el `<style>` del SVG exportado: ese bloque rompía el XML (un `&` sin
> escapar en la URL de fonts.googleapis.com) y el navegador no podía cargarlo como
> `<img>` — fallaba en silencio (`naturalWidth/Height: 0`, sin error visible en pantalla).
> Además ese `@import` no funciona en contexto `<img>` de todos modos (los navegadores
> bloquean fuentes externas ahí). Si se regenera el SVG a mano, no agregar ese bloque.
