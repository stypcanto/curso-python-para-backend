# 🏗️ Estructura de un proyecto FastAPI (arquitectura por capas)

> Anatomía de carpetas que usa el profe desde la **Clase 4** (PostgreSQL + SQLAlchemy) en
> adelante. Cada capa tiene una sola responsabilidad — así se puede cambiar una sin romper
> las demás (p. ej. cambiar de Postgres a MySQL solo toca `db/` y `repositories/`).

## 📂 Carpetas y qué va en cada una

| Carpeta | Qué contiene | Responsabilidad |
|---|---|---|
| `core/` | Configuración central: variables de entorno, settings de la app, (más adelante) seguridad/JWT | "El panel de control" del proyecto |
| `db/` | Conexión a la base de datos: `engine`, `SessionLocal`, la `Base` declarativa de SQLAlchemy | Cómo hablamos con Postgres |
| `models/` | Clases ORM (SQLAlchemy) que representan las **tablas** (`User`, `Category`, `Ticket`) | El "mundo de tablas" mapeado a Python — ver [Clase 4](../01-Clases/Clase-04.md) |
| `repositories/` | Funciones que encapsulan el acceso a datos (`create`, `get`, `update`, `delete`) usando los `models` | **Repository Pattern**: aísla el SQL/ORM del resto de la app |
| `schemas/` | Clases Pydantic para **validar** lo que entra y sale de la API (request/response) | El "contrato" de la API — no es lo mismo que un `model` |
| `services/` | Lógica de negocio: orquesta uno o varios `repositories`, aplica reglas antes/después de tocar la BD | Las "reglas del negocio" |
| `routers/` | Los endpoints de FastAPI (`@router.get`, `@router.post`, …) | Las rutas HTTP — el punto de entrada |
| `migrations/` | Historial de migraciones generado por **Alembic** | Versiona los cambios de esquema de la BD |
| `requirements.txt` | Dependencias del proyecto (`fastapi`, `sqlalchemy`, `alembic`, `psycopg2-binary`, …) | Qué instalar con `pip install -r requirements.txt` |

## 🔁 Flujo de una petición (de afuera hacia la base de datos)

```
Cliente HTTP
     │
     ▼
┌──────────┐   valida entrada/salida    ┌──────────┐
│ routers/ │ ─────────────────────────► │ schemas/ │
└────┬─────┘                            └──────────┘
     │ llama a la lógica de negocio
     ▼
┌────────────┐   aplica reglas, orquesta   ┌────────────────┐
│ services/  │ ───────────────────────────►│ repositories/  │
└────────────┘                              └───────┬────────┘
                                                     │ usa los modelos ORM
                                                     ▼
                                              ┌────────────┐    engine/sesión   ┌──────┐
                                              │  models/    │ ─────────────────►│ db/  │
                                              └────────────┘                    └──┬───┘
                                                                                     │
                                                                                     ▼
                                                                              PostgreSQL
```

> 💡 **Por qué separar `models/` de `schemas/`:** el `model` es la tabla real en la base
> de datos (lo que sabe SQLAlchemy); el `schema` es lo que la API expone/recibe (lo que
> sabe Pydantic). No siempre coinciden — por ejemplo, un `schema` de creación de usuario
> puede pedir `password` pero el `schema` de respuesta nunca lo devuelve, aunque el
> `model` sí lo guarde (hasheado) en la tabla.

> 🧪 **Tip de entrevista:** *¿Para qué sirve el Repository Pattern si ya tengo el ORM?*
> Para que el resto de la app (`services/`, `routers/`) no dependa directamente de
> SQLAlchemy — si mañana cambiás de ORM o de base de datos, solo tocás `repositories/` y
> `db/`, el resto del código no se entera.

## 📎 Apuntes relacionados
- [Clase 4 — PostgreSQL y persistencia de datos](../01-Clases/Clase-04.md) — incluye la
  versión de este mismo diagrama con los nombres reales del código
  (`TicketRepository`, `curso-postgres`, etc.)
