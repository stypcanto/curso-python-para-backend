# Diagrama ER — Sistema de tickets (Clase 4)

Modelo de datos real de `02-Ejercicios/Clase-04/app/models/` (`users`, `categories`,
`tickets`), con nombres de tabla, PK/FK y relaciones 1:N tal cual quedaron en el código
con SQLAlchemy 2.0. Reemplaza el boceto ASCII a mano que estaba en
`01-Clases/Clase-04.md`.

**Regenerar tras un cambio en los modelos:**
```bash
cd 04-Recursos/diagramas-tecnicos/clase-04-er-tickets
dot -Tsvg src/modelo-datos-tickets.dot -o svg/modelo-datos-tickets.svg
dot -Tpng -Gdpi=180 src/modelo-datos-tickets.dot -o png/modelo-datos-tickets.png
cp png/modelo-datos-tickets.png ../../../public/clase-04-er-tickets.png
```
