# Diagrama técnico — Bounded Contexts y Anti-Corruption Layer (Clase 5)

> Generado con el skill `diagram-design` (HTML + SVG inline), paleta por defecto.

## Qué muestra

Tres *bounded contexts* — Catalog, Sales e Identity — mapeados sobre los
microservicios que ya existen en el resto de `Clase-05.md` (`products`, `orders`,
`users`), cada uno con su propio lenguaje ubicuo (`Product · SKU · Stock`,
`Order · OrderItem · Reserve`, `Customer · Account`). Dos relaciones cruzan los
límites de contexto:

- `dummyjson.com` (la API externa que ya consume `products-service-flask`) entra al
  Catalog Context solo a través de un **Anti-Corruption Layer** — el mismo código que
  reforma el JSON crudo antes de exponerlo (`services/products.py`,
  `04-Recursos/diagramas-tecnicos/clase-05-comunicacion-async/` para el contexto).
- `orders` llama a `products` (`reserve_stock()`) cruzando su propio límite de
  contexto — foco del diagrama (coral), para remarcar que es la excepción, no la regla.

## Archivos

| Archivo | Qué es |
|---|---|
| `src/diagrama.html` | Fuente editable (HTML + SVG inline + CSS del skill `diagram-design`) |
| `svg/diagrama.svg` | Export standalone del `<svg>` |

La copia que sirve el sitio VitePress está en
`public/clase-05-diagrama-bounded-contexts.svg`. Si se edita `src/diagrama.html`, hay
que volver a exportar y copiar a `public/` — no se actualiza solo.

## Regenerar el SVG

```bash
python3 - << 'EOF'
import re
src = open("src/diagrama.html", encoding="utf-8").read()
svg = re.search(r'(<svg .*?</svg>)', src, re.S).group(1)
open("svg/diagrama.svg", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
EOF
cp svg/diagrama.svg ../../../public/clase-05-diagrama-bounded-contexts.svg
```

> 📝 Sin `@import` de Google Fonts en el SVG exportado — ver la nota en el README de
> `clase-05-arquitectura-microservicios/` sobre por qué rompe el XML y no aporta nada
> en contexto `<img>`.
