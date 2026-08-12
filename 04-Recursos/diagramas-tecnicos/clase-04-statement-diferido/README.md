# Diagrama de flujo — Evaluación diferida de un `statement` (Clase 4)

Reemplaza el ASCII a mano que estaba en `01-Clases/Clase-04.md` (sección "Repository
Pattern"). Muestra que `select(Ticket).order_by(...)` no ejecuta nada por sí solo — es
`db.scalars(statement)` quien lo traduce a SQL real y lo corre en Postgres.

**Regenerar tras un cambio:**
```bash
cd 04-Recursos/diagramas-tecnicos/clase-04-statement-diferido
dot -Tsvg src/statement-evaluacion-diferida.dot -o svg/statement-evaluacion-diferida.svg
dot -Tpng -Gdpi=180 src/statement-evaluacion-diferida.dot -o png/statement-evaluacion-diferida.png
cp png/statement-evaluacion-diferida.png ../../../public/clase-04-statement-diferido.png
```
