# Diagrama de flujo — Cómo el ORM traduce Python a SQL (Clase 4)

Reemplaza el ASCII a mano que estaba en `01-Clases/Clase-04.md` (sección "¿Qué es un
ORM?"). Muestra, en 2 filas paralelas, cómo SQLAlchemy traduce código Python a SQL real:
1. `class Ticket` → `CREATE TABLE tickets (...)`
2. `ticket = Ticket(...)` → `INSERT INTO tickets (...)`

**Regenerar tras un cambio:**
```bash
cd 04-Recursos/diagramas-tecnicos/clase-04-orm-flujo
dot -Tsvg src/orm-traduce-python-a-sql.dot -o svg/orm-traduce-python-a-sql.svg
dot -Tpng -Gdpi=180 src/orm-traduce-python-a-sql.dot -o png/orm-traduce-python-a-sql.png
cp png/orm-traduce-python-a-sql.png ../../../public/clase-04-orm-flujo.png
```

> ⚠️ Si se necesita alinear filas paralelas (sin conectarlas) bajo `rankdir=LR`: usar
> `{rank=same; nodo_fila1; nodo_fila2;}` + una arista invisible entre ellos
> (`nodo_fila1 -> nodo_fila2 [style=invis]`) para fijar el orden vertical — sin esto
> Graphviz puede invertir el orden de las filas a su criterio.
