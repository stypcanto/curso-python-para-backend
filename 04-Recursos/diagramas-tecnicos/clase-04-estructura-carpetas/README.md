# Diagrama de estructura de carpetas — `app/` (Clase 4)

Reemplaza/complementa el árbol ASCII de `01-Clases/Clase-04.md` (sección
"Arquitectura del proyecto"). Muestra las 9 carpetas/archivos de
`02-Ejercicios/Clase-04/app/`, agrupadas y diferenciadas por color según su capa
(API, negocio, datos, herramientas) — a diferencia de
`clase-04-arquitectura-capas`, este diagrama **no** muestra el flujo de una
petición, solo la estructura estática.

**Regenerar tras un cambio:**
```bash
cd 04-Recursos/diagramas-tecnicos/clase-04-estructura-carpetas
dot -Tsvg src/estructura-carpetas-app.dot -o svg/estructura-carpetas-app.svg
dot -Tpng -Gdpi=180 src/estructura-carpetas-app.dot -o png/estructura-carpetas-app.png
cp png/estructura-carpetas-app.png ../../../public/clase-04-estructura-carpetas.png
```
