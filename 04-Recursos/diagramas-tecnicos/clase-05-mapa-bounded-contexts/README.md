# Diagrama técnico — Mapa de Bounded Contexts (Clase 5)

> Generado con el skill `diagram-design` (HTML + SVG inline), paleta por defecto.
> Redibuja el mapa de 4 contextos que corrigió al diagrama anterior
> (`clase-05-bounded-contexts/`): ese tenía `Inventory` mezclado dentro de `Catalog`
> (`products`); acá `Inventory` es su propio Bounded Context, separado.

## Qué muestra

Cuatro Bounded Contexts en cuadrícula 2×2 — **Identity** (`User · Role ·
Authentication`), **Catalog** (`Product · Category · Price`), **Orders** (`Order ·
OrderItem · OrderStatus`) e **Inventory** (`Stock · Reservation · Warehouse`) — con
líneas punteadas marcando qué contextos se relacionan entre sí: Identity–Catalog,
Identity–Orders, Catalog–Inventory, Orders–Inventory. Cada contexto lleva, en cursiva,
el archivo/servicio real del curso que lo implementa (`users-service`,
`products-service`, `orders (boceto)`, `inventory_item.py`).

## Archivos

| Archivo | Qué es |
|---|---|
| `src/diagrama.html` | Fuente editable |
| `svg/diagrama.svg` | Export standalone del `<svg>` |

Copia servida por VitePress: `public/clase-05-mapa-bounded-contexts.svg`.

## Regenerar el SVG

```bash
python3 - << 'EOF'
import re
src = open("src/diagrama.html", encoding="utf-8").read()
svg = re.search(r'(<svg .*?</svg>)', src, re.S).group(1)
open("svg/diagrama.svg", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
EOF
cp svg/diagrama.svg ../../../public/clase-05-mapa-bounded-contexts.svg
```
