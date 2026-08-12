# Diagrama de arquitectura — Capas del proyecto (Clase 4)

Reemplaza el flujo ASCII genérico ("router → schema → service → repository → model →
db") de `00-Notas/05-Estructura-Proyecto-FastAPI.md` por uno con los nombres reales del
código de `02-Ejercicios/Clase-04/app/`. Marca con borde punteado lo que todavía no
está escrito (`routers/`, `services/`) vs. lo ya construido y verificado.

**Regenerar tras un cambio:**
```bash
cd 04-Recursos/diagramas-tecnicos/clase-04-arquitectura-capas
dot -Tsvg src/arquitectura-por-capas.dot -o svg/arquitectura-por-capas.svg
dot -Tpng -Gdpi=180 src/arquitectura-por-capas.dot -o png/arquitectura-por-capas.png
cp png/arquitectura-por-capas.png ../../../public/clase-04-arquitectura-capas.png
```

> 💡 Cuando se escriban `routers/` y `services/`, actualizar sus nodos en el `.dot`
> (sacar `style="rounded,filled,dashed"` y el texto "(pendiente)") y volver a renderizar.
