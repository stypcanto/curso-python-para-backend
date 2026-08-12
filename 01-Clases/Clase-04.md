---
sidebar: "Clase 4 · PostgreSQL"
---

# 📙 Clase 4 — PostgreSQL y persistencia de datos

> Python para Backend · 2026-08-11 · Carpeta: `02-Ejercicios/Clase-04`
> ⬅️ Volver al [índice de clases](00-Indice.md)

## 🎯 Qué aprendí (según temario — por confirmar/completar al documentar la clase)
- Introducción a PostgreSQL
- Modelado de datos
- Relaciones entre tablas
- Consultas SQL esenciales
- Integración con FastAPI
- Preparación para ORM
- ORM con SQLAlchemy
- CRUD completo
- Relaciones entre entidades
- Repository Pattern
- Migraciones con Alembic
- Buenas prácticas de persistencia

# 📖 PARTE TEÓRICA

## 🗄️ 1. ¿Qué es un ORM?

El profe arrancó definiendo el **ORM (Object-Relational Mapping / Mapeo
Objeto-Relacional)**: la capa que **traduce información entre dos mundos que hablan
distinto**:

- El mundo de **Python** (clases, objetos, atributos).
- El mundo de la **base de datos relacional** (tablas, filas, columnas).

La idea central es **modelar información como tablas, pero manipularla como objetos**:

```
Python (código)              ORM (SQLAlchemy)         PostgreSQL (base de datos)
─────────────────            ─────────────────         ──────────────────────────
class Ticket:          ──►   traduce la clase   ──►    CREATE TABLE tickets (
    title: str                a una tabla                 id SERIAL PRIMARY KEY,
    priority: str                                          title TEXT,
                                                             priority TEXT
                                                         );

ticket = Ticket(       ──►   traduce el objeto   ──►    INSERT INTO tickets
    title="Error login",       a un INSERT               (title, priority)
    priority="Alta")                                     VALUES ('Error login','Alta');
```

| Mundo Python (objetos) | Mundo SQL (tablas) |
|---|---|
| Clase (`class Ticket`) | Tabla (`tickets`) |
| Atributo (`ticket.priority`) | Columna (`priority`) |
| Instancia/objeto (`ticket = Ticket(...)`) | Fila/registro (`INSERT INTO ...`) |
| `ticket.priority = "Cerrado"` | `UPDATE tickets SET priority = 'Cerrado'` |

> 💡 En resumen: el ORM te deja **modelar tus datos como clases de Python** y él se
> encarga de generar el SQL correspondiente (INSERT/SELECT/UPDATE/DELETE) por debajo.

### 🗺️ Ejemplo en vivo: modelando un sistema de tickets

El profe dibujó a mano el modelo de datos de un sistema de tickets (el mismo dominio de
los ejemplos SQL de arriba), con 3 entidades y sus relaciones:

```
┌───────────────────┐          ┌───────────────────┐
│       user         │          │      category      │
├───────────────────┤          ├───────────────────┤
│ id                  │          │ id                  │
│ name                │          │ name                │
│ email               │          └──────────┬─────────┘
└──────────┬─────────┘                     │
           │ 1                              │ 1
           │                                │
           │ N                              │ N
           ▼                                ▼
              ┌───────────────────────┐
              │         ticket          │
              ├───────────────────────┤
              │ id                       │
              │ title                    │
              │ description              │
              │ priority                 │
              │ status                   │
              │ requester_id  (FK → user.id)
              │ category_id   (FK → category.id)
              └───────────────────────┘
```

| Entidad | Campos | Rol |
|---|---|---|
| `user` | `id`, `name`, `email` | Quién reporta el ticket |
| `category` | `id`, `name` | Cómo se clasifica el ticket |
| `ticket` | `id`, `title`, `description`, `priority`, `status`, `requester_id`, `category_id` | El registro central; conecta con las otras dos |

| Relación | Cardinalidad | Cómo se implementa |
|---|---|---|
| `user` → `ticket` | **1:N** (un usuario puede tener muchos tickets) | `ticket.requester_id` es **clave foránea (FK)** que apunta a `user.id` |
| `category` → `ticket` | **1:N** (una categoría agrupa muchos tickets) | `ticket.category_id` es **FK** que apunta a `category.id` |

> 💡 Esto es lo que en SQL puro se resolvía con el `JOIN` de la sección anterior
> (`SELECT t.title, c.name FROM tickets t JOIN categories c ON t.category_id = c.id`):
> ese `t.category_id = c.id` es exactamente la flecha `category_id (FK → category.id)`
> del dibujo. El ORM va a modelar esta misma relación como **clases con atributos que
> se referencian entre sí**, en vez de escribir el `JOIN` a mano.

> 📌 Convención que usa el profe: el campo de la FK se nombra `<entidad>_id`
> (`requester_id`, `category_id`) — así se lee directo qué tabla referencia.

## 🐘 2. SQL esencial — lo que SQLAlchemy hará por nosotros

> Aunque usemos ORM, **comprender SQL es imprescindible** para depurar, optimizar y
> tomar decisiones informadas.

El profe repasó las 4 operaciones base que después el ORM va a generar por nosotros:

**INSERT** — crear un registro nuevo:
```sql
INSERT INTO tickets (title, priority) VALUES ('Error login', 'Alta');
```

**SELECT + WHERE** — consultar filtrando:
```sql
SELECT * FROM tickets WHERE priority = 'Alta';
```

**UPDATE / DELETE** — modificar o borrar un registro existente:
```sql
UPDATE tickets SET status = 'Cerrado' WHERE id = 1;
```

**JOIN** — combinar datos de varias tablas relacionadas:
```sql
SELECT t.title, c.name
FROM tickets t
JOIN categories c ON t.category_id = c.id;
```

> ⚠️ **Clave del profe:** *"ORM no significa «no necesito saber SQL»."* El ORM te
> ahorra escribir el SQL a mano en el día a día, pero cuando algo va lento, una
> consulta no trae lo esperado, o hay que optimizar un `JOIN` complejo, necesitás
> entender qué SQL está generando el ORM por debajo.

## 🏗️ 3. Arquitectura del proyecto (estructura de carpetas)

El profe armó en VS Code la estructura por capas que va a usar de acá en adelante para
el proyecto con FastAPI + SQLAlchemy + Alembic:

```
app/
├── core/           # configuración central (settings, variables de entorno)
├── db/             # conexión a la BD (engine, sesión, Base de SQLAlchemy)
├── models/         # modelos ORM = las tablas (User, Category, Ticket)
├── repositories/   # Repository Pattern: acceso a datos (create/get/update/delete)
├── routers/        # endpoints de FastAPI (las rutas HTTP)
├── schemas/        # esquemas Pydantic (validación de entrada/salida de la API)
├── services/       # lógica de negocio (orquesta los repositories)
├── migrations/     # historial de migraciones de Alembic
└── requirements.txt # dependencias del proyecto
```

Ya quedó creada igual en `02-Ejercicios/Clase-04/app/` (con `__init__.py` en cada
paquete Python).

> 📎 Detalle de qué va en cada carpeta y el flujo de una petición (router → schema →
> service → repository → model → db), en la nota temática:
> [00-Notas/05-Estructura-Proyecto-FastAPI.md](../00-Notas/05-Estructura-Proyecto-FastAPI.md)

# 💻 PARTE PRÁCTICA

Carpeta de trabajo: `02-Ejercicios/Clase-04/app/`

### 🐘 1. PostgreSQL corriendo en Docker

Para no instalar Postgres directo en el Mac, se levantó en un contenedor:

```bash
docker run -d \
  --name curso-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=curso_backend \
  -p 5432:5432 \
  postgres:16-alpine
```

Datos de conexión para usar desde SQLAlchemy:

| Dato | Valor |
|---|---|
| host | `localhost` |
| puerto | `5432` |
| usuario | `postgres` |
| password | `postgres` |
| base de datos | `curso_backend` |

> ⚠️ Password de **desarrollo local únicamente** — no usar en algo expuesto a internet.

### 🐍 2. Entorno virtual y dependencias

```bash
# Crear y activar el entorno virtual (macOS/Linux — en Mac es python3, no python)
cd 02-Ejercicios/Clase-04/app
python3 -m venv .venv
source .venv/bin/activate

# Instalar las dependencias de esta clase
pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary

# Congelar versiones exactas en requirements.txt (queda listo para "pip install -r")
pip freeze > requirements.txt
```

`requirements.txt` quedó con (entre otras, resueltas como dependencias):

| Paquete | Para qué |
|---|---|
| `fastapi` | El framework de la API |
| `uvicorn[standard]` | El servidor que corre la app FastAPI |
| `sqlalchemy` | El ORM — mapea clases Python ↔ tablas de Postgres |
| `psycopg2-binary` | El **driver**: el traductor que permite a SQLAlchemy hablar con Postgres |
| `pydantic` | Viene con FastAPI — valida los `schemas/` |

> 🧪 **Tip de entrevista:** *¿SQLAlchemy sirve para conectar a cualquier base de datos?*
> El ORM sí es agnóstico, pero necesita un **driver específico** por motor —
> `psycopg2-binary` para Postgres, `pymysql`/`mysqlclient` para MySQL, etc. El ORM
> habla con el driver, y el driver habla con la base de datos real.

### 📄 3. Primer schema: `schemas/ticket.py`

Primer archivo de código de la clase — los schemas de Pydantic (capa `schemas/`, ver la
sección teórica "🏗️ Arquitectura del proyecto" arriba) para validar los datos de un
ticket:

```python
# 02-Ejercicios/Clase-04/app/schemas/ticket.py
from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=500)
    priority: str = Field(default="Media")

    requester_id: int = Field(gt=0)
    category_id: int = Field(gt=0)


class TicketUpdate(BaseModel):
    priority: str | None = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str

    requester_id: int
    category_id: int
```

**Por qué son 3 clases para la misma entidad, y no una sola:**

| Clase | Para qué | Detalle |
|---|---|---|
| `TicketCreate` | Lo que el **cliente manda** al crear un ticket (entrada) | No tiene `id` ni `status` — eso lo pone el servidor, no el cliente |
| `TicketUpdate` | Lo que el cliente manda al **actualizar** | Todos los campos opcionales (`str \| None = None`) — una actualización puede tocar solo algunos campos, no todos de nuevo |
| `TicketResponse` | Lo que la API **devuelve** (salida) | Sí trae `id` (ya lo generó la base de datos); no repite las validaciones de `Field`, porque esas ya se aplicaron al crear |

> 💡 `Field(min_length=..., max_length=...)` define **validaciones** directo en el
> schema — si alguien manda un `title` de 3 caracteres, FastAPI responde error 422
> automáticamente, sin que escribas ese `if` a mano.

> 💡 `Field(gt=0)` ("greater than 0") en `requester_id`/`category_id`: son las mismas FK
> del diagrama "Ejemplo en vivo: modelando un sistema de tickets" (arriba en esta misma
> clase) — `ticket.requester_id → user.id`, `ticket.category_id → category.id`. `gt=0`
> evita que llegue un id inválido como `0` o negativo.

> 🧪 **Tip de entrevista:** *¿Por qué separar Create/Update/Response en vez de un solo
> schema?* Porque cada uno valida un **contrato distinto** de la API — lo que se puede
> mandar al crear no es lo mismo que lo que se puede mandar al actualizar, ni lo que se
> devuelve. Meterlos en un solo schema obliga a hacer todos los campos opcionales,
> perdiendo validaciones (ej. `title` dejaría de ser obligatorio al crear).

### 🐞 Errores de esta clase (con solución)

Documentados en detalle en `06-Errores/`:

| Error | Causa | Nota |
|---|---|---|
| `zsh: command not found: python` | En macOS es `python3`, no `python` | [ver](../06-Errores/2026-08-11-python-command-not-found.md) |
| `zsh: command not found: pip` | El `.venv` no estaba activado en esa terminal | [ver](../06-Errores/2026-08-11-pip-command-not-found-venv-inactivo.md) |
| Pylance: *"No se ha podido resolver la importación pydantic"* | VS Code usaba otro intérprete de Python, no el `.venv` del proyecto | [ver](../06-Errores/2026-08-11-pylance-no-resuelve-import-pydantic.md) |

*(sigue pendiente documentar `models/`, `repositories/`, la conexión real en `db/`, etc.
a medida que avanza la clase)*

# 🏋️ EJERCICIOS CON SOLUCIÓN
*(pendiente — se documentan 10 ejercicios graduales cuando haya contenido de la clase)*

## ❓ Preguntas y respuestas (autoevaluación)
*(pendiente — 10 preguntas graduales)*

## 📎 Apuntes relacionados
*(pendiente)*

## ➡️ Siguiente
[Clase 5](Clase-05.md)
