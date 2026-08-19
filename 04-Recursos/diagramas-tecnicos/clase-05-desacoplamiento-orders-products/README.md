# Diagrama técnico — Bajo acoplamiento: orders → products → su propia BD (Clase 5)

> Generado con el skill `diagram-design` (HTML + SVG inline), paleta por defecto.
> Redibuja un boceto de pizarra (3 cajas de colores: Order Service → Product Service →
> Products DB) que resuelve la ambigüedad del cuadrante `clase-05-desacoplamiento-
> cuadrante.png` — acá no hay dos lecturas posibles, es un único camino correcto.

## Qué muestra

`Order Service` llama a `Product Service` por contrato (`GET /products/:id`, foco
coral). Solo `Product Service` toca la base de datos `Products` — es su dueño
exclusivo. Un camino punteado y tachado, desde `Order Service` directo hacia la base de
datos, marca explícitamente el camino **prohibido**: `orders` nunca lee esa base de
datos por su cuenta.

## Archivos

| Archivo | Qué es |
|---|---|
| `src/diagrama.html` | Fuente editable |
| `svg/diagrama.svg` | Export standalone del `<svg>` |

Copia servida por VitePress: `public/clase-05-diagrama-desacoplamiento-orders-products.svg`.

## Regenerar el SVG

```bash
python3 - << 'EOF'
import re
src = open("src/diagrama.html", encoding="utf-8").read()
svg = re.search(r'(<svg .*?</svg>)', src, re.S).group(1)
open("svg/diagrama.svg", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
EOF
cp svg/diagrama.svg ../../../public/clase-05-diagrama-desacoplamiento-orders-products.svg
```
