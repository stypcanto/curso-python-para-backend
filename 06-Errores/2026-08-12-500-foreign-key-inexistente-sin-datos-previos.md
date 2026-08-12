---
categoria: "🧠 Lógica y tipos"
sidebar: "500 al crear un Ticket sin datos previos"
---

# ❌ 500 Internal Server Error al hacer `POST /tickets/` (Postman)

> [Clase 4](../01-Clases/Clase-04.md) · probando el endpoint de crear ticket desde
> Postman, con la base recién migrada (tablas vacías)

## 🧨 Qué pasó

```json
POST {{base_url}}/tickets/
{
  "title": "No carga el dashboard",
  "description": "El dashboard principal no carga desde ayer",
  "priority": "Alta",
  "requester_id": 1,
  "category_id": 1
}
```
```
HTTP 500 Internal Server Error
```

Los campos del body están bien — `TicketCreate` (sección 8) los valida todos sin
problema. El error no sale ahí.

## 🔍 Causa

`requester_id: 1` y `category_id: 1` son **Foreign Keys** (`ForeignKeyConstraint`,
sección 9): le dicen a Postgres "este ticket pertenece al usuario/categoría con ese
`id`". Pero justo después de `alembic upgrade head` las tablas `users` y `categories`
quedan **vacías** — nadie cargó datos de prueba todavía:

```sql
SELECT COUNT(*) FROM users;      -- 0
SELECT COUNT(*) FROM categories; -- 0
```

Cuando `TicketRepository.create()` (sección 10) hace `db.commit()`, Postgres rechaza el
`INSERT` porque esos ids no existen — una violación de integridad referencial
(`IntegrityError`). Como nadie captura ese error puntual (ni el repository ni el
service tienen un `try/except` para él), la excepción sube sin controlar hasta FastAPI,
que responde el genérico `500` en vez de un `400`/`404` con un mensaje claro.

> 📝 Agregar un campo `"status"` al body (como se probó al principio) no soluciona
> nada — `status` ni siquiera es un campo de `TicketCreate` (Pydantic lo ignora
> silenciosamente); el problema nunca fue de validación de schema, es un nivel más
> abajo, al guardar contra la base.

## ✅ Solución

Crear primero un `user` y una `category` reales (todavía no hay routers `/users` ni
`/categories`, así que se insertan directo por SQL):

```bash
docker exec curso-postgres psql -U postgres -d curso_backend -c \
  "INSERT INTO users (name, email) VALUES ('Styp Canto', 'styp@example.com');" \
  -c "INSERT INTO categories (name) VALUES ('Infraestructura');"
```

Con `id=1` ya existente en las dos tablas, el mismo `POST` da `201 Created`.

## 📎 Relacionado
- [[invalidrequesterror-relationship-no-resuelve]] — otro error de esta clase por
  relaciones/FK entre modelos.
