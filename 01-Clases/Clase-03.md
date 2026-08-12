---
sidebar: "Clase 3 · FastAPI y APIs REST"
---

# 📙 Clase 3 — Introducción a FastAPI y APIs REST

> Python para Backend · 2026-08-06 · Carpeta: `02-Ejercicios/Clase-03`
> ⬅️ Volver al [índice de clases](00-Indice.md)

## 🎯 Qué aprendí (según temario — por confirmar/completar al documentar la clase)
- Creación del primer proyecto FastAPI
- Endpoints y rutas
- Métodos HTTP
- Validación con Pydantic
- Manejo de Request y Response
- Swagger y OpenAPI
- Diseño de APIs RESTful
- Parámetros y query strings
- Manejo de errores
- Middleware
- Versionamiento de APIs
- Buenas prácticas REST

# 📖 PARTE TEÓRICA

> 📌 **Esta teoría no viene de la clase real dictada por el profe** (todavía no pasé
> capturas ni grabación de la Clase 3) — es **teoría estándar de referencia**, armada solo
> a partir de los 12 puntos del temario (ver "Qué aprendí" arriba), verificada con
> fuentes externas y con `TestClient` en terminal (mismo criterio que usé para la
> [Clase 2](Clase-02.md)). Cuando tenga el material real de la clase, esta sección se
> revisa y se completa con los ejemplos/orden que haya dado el profe — no se descarta,
> se enriquece.

## 🚀 1. Qué es FastAPI y primer proyecto
**FastAPI** es un framework para construir APIs con Python, pensado sobre dos ideas
centrales: usar los **type hints** de Python (ya vistos en la Clase 1) para validar datos
automáticamente, y generar **documentación interactiva** sola, sin escribir nada extra.

```bash
# Entorno virtual y dependencias (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]"
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "API de tickets funcionando"}
```

```bash
uvicorn main:app --reload
```
```
{'mensaje': 'API de tickets funcionando'}
```
*(salida verificada con `TestClient` haciendo `GET /` — mismo resultado que abrir
`http://127.0.0.1:8000/` en el navegador una vez corriendo `uvicorn`)*

| Pieza | Qué es |
|---|---|
| `FastAPI()` | Crea la aplicación — es el objeto central al que se le "cuelgan" todas las rutas. |
| `uvicorn` | El **servidor ASGI** que hace correr la app — FastAPI define la lógica, `uvicorn` la sirve por HTTP. |
| `main:app` | Le dice a `uvicorn` "en el archivo `main.py`, la variable `app`". |
| `--reload` | Reinicia el servidor solo cuando cambia el código — para desarrollo, nunca en producción. |

> 💡 FastAPI está construido sobre dos librerías que ya conocemos: **Starlette** (la
> parte que maneja HTTP de bajo nivel) y **Pydantic** (la que valida los datos con las
> clases que vimos en la Clase 2/1). Elegirlo no es magia — combina piezas ya probadas.

> 🧪 Tip de entrevista: ¿por qué FastAPI se considera "rápido" en dos sentidos? Rápido en
> **ejecución** (por Starlette + soporte async) y rápido en **desarrollo** (menos código
> repetido gracias a los type hints y la documentación automática).

## 🛣️ 2. Endpoints, rutas y métodos HTTP
Un **endpoint** (o *path operation*) es la combinación de una **ruta** (URL) y un
**método HTTP** — cada combinación dispara una función Python distinta.

```python
from fastapi import FastAPI

app = FastAPI()

tickets_db = [
    {"id": 1001, "title": "Error de acceso", "priority": "Alta"},
    {"id": 1002, "title": "Lentitud del sistema", "priority": "Media"},
]

@app.get("/tickets")               # GET: leer (todos)
def list_tickets():
    return tickets_db

@app.get("/tickets/{ticket_id}")   # GET: leer (uno, por id en la ruta)
def get_ticket(ticket_id: int):
    for t in tickets_db:
        if t["id"] == ticket_id:
            return t
    return {"error": "no encontrado"}

@app.post("/tickets")              # POST: crear
def create_ticket(title: str, priority: str = "Media"):
    new_ticket = {"id": 1003, "title": title, "priority": priority}
    tickets_db.append(new_ticket)
    return new_ticket

@app.put("/tickets/{ticket_id}")   # PUT: actualizar
def update_ticket(ticket_id: int, priority: str):
    for t in tickets_db:
        if t["id"] == ticket_id:
            t["priority"] = priority
            return t
    return {"error": "no encontrado"}

@app.delete("/tickets/{ticket_id}")  # DELETE: borrar
def delete_ticket(ticket_id: int):
    global tickets_db
    tickets_db = [t for t in tickets_db if t["id"] != ticket_id]
    return {"eliminado": ticket_id}
```
```
GET    /tickets        -> [{'id': 1001, ...}, {'id': 1002, ...}]
GET    /tickets/1001    -> {'id': 1001, 'title': 'Error de acceso', 'priority': 'Alta'}
POST   /tickets         -> {'id': 1003, 'title': 'Nueva falla', 'priority': 'Baja'}
PUT    /tickets/1001    -> {'id': 1001, 'title': 'Error de acceso', 'priority': 'Cerrado'}
DELETE /tickets/1002    -> {'eliminado': 1002}
```

| Método | Para qué | Analogía CRUD |
|---|---|---|
| `GET` | Leer/consultar (no modifica nada) | Read |
| `POST` | Crear un recurso nuevo | Create |
| `PUT` | Reemplazar/actualizar un recurso existente | Update |
| `PATCH` | Actualizar **parcialmente** (solo algunos campos) | Update parcial |
| `DELETE` | Eliminar un recurso | Delete |

> ⚠️ `GET` nunca debería modificar datos (no debería tener efectos secundarios) — si una
> operación cambia algo, el método correcto es `POST`/`PUT`/`PATCH`/`DELETE`, nunca `GET`.

## 🧾 3. Parámetros: path, query y body (validación con Pydantic)
Una petición le puede pasar datos a un endpoint de **tres formas distintas**, y FastAPI
decide de cuál se trata según **dónde** está declarado el parámetro en la función:

```python
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

# Path parameter: va EN la ruta, es obligatorio y es PARTE de la URL
@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int = Path(..., gt=0, description="ID del ticket")):
    return {"ticket_id": ticket_id}

# Query parameter: va DESPUÉS del ?, es opcional (tiene default)
@app.get("/tickets")
def list_tickets(priority: str | None = Query(default=None), limit: int = Query(default=10, le=100)):
    return {"priority": priority, "limit": limit}

# Request body: JSON en el cuerpo de la petición, validado con un modelo Pydantic
class TicketCreate(BaseModel):
    title: str = Field(min_length=5)
    priority: str = "Media"

@app.post("/tickets")
def create_ticket(ticket: TicketCreate):
    return {"creado": ticket.model_dump()}
```
```
GET  /tickets/1001                       -> {'ticket_id': 1001}
GET  /tickets?priority=Alta&limit=5      -> {'priority': 'Alta', 'limit': 5}
POST /tickets {"title": "Error de acceso", "priority": "Alta"}
     -> 200 {'creado': {'title': 'Error de acceso', 'priority': 'Alta'}}
POST /tickets {"title": "Hi"}
     -> 422 {'detail': [{'type': 'string_too_short', 'loc': ['body', 'title'],
              'msg': 'String should have at least 5 characters', ...}]}
```

| Tipo | Dónde viaja | Ejemplo | Obligatorio por defecto |
|---|---|---|---|
| **Path** (`{ticket_id}`) | Parte de la URL | `/tickets/1001` | Sí — si falta, la ruta ni matchea |
| **Query** (`?clave=valor`) | Después del `?` | `/tickets?priority=Alta` | No (a menos que no tenga default) |
| **Body** (JSON) | Cuerpo de la petición | `{"title": "...", "priority": "Alta"}` | Depende del modelo Pydantic |

> 💡 Este es el mismo patrón `Field(min_length=..., gt=...)` que ya usamos en `schemas/
> ticket.py` de la [Clase 4](Clase-04.md) — la Clase 3 es literalmente donde ese patrón
> se aprende por primera vez, antes de aplicarlo con una base de datos real detrás.

> 🧪 Tip de entrevista: si al `422` de validación fallida no lo escribiste vos, ¿de dónde
> sale? Lo genera FastAPI **automáticamente** en cuanto un dato no cumple lo que pide el
> modelo Pydantic o el `Path`/`Query` — no hace falta un `try`/`except` a mano para eso.

## 📤 4. Request y Response: status codes y `response_model`
Además de **qué** devuelve un endpoint, importa **con qué forma** y **con qué código de
estado HTTP** lo devuelve — dos cosas que FastAPI deja declarar explícitamente.

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class TicketCreate(BaseModel):
    title: str
    priority: str = "Media"

class TicketResponse(BaseModel):
    id: int
    title: str
    priority: str

@app.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate):
    return TicketResponse(id=1001, title=ticket.title, priority=ticket.priority)
```
```
POST /tickets {"title": "Error de acceso"}
-> 201 {'id': 1001, 'title': 'Error de acceso', 'priority': 'Media'}
```

| Rango de código | Significa |
|---|---|
| `2xx` | Éxito (`200` OK, `201` Created, `204` No Content) |
| `3xx` | Redirección |
| `4xx` | Error del **cliente** (`400` Bad Request, `404` Not Found, `422` Unprocessable Entity) |
| `5xx` | Error del **servidor** (`500` Internal Server Error) |

> 📌 `response_model=TicketResponse` hace dos cosas a la vez: **filtra** la respuesta (si
> la función devolviera de más, solo se manda lo que el modelo declara) y **documenta**
> automáticamente en Swagger cómo luce la respuesta — ver sección siguiente.

## 📚 5. Documentación automática: Swagger UI y OpenAPI
Sin escribir nada extra, FastAPI genera un **esquema OpenAPI** (una descripción
estandarizada de toda la API) y lo sirve en dos interfaces interactivas:

| Ruta | Qué muestra |
|---|---|
| `/docs` | **Swagger UI** — interactiva: se pueden probar los endpoints en vivo desde el navegador. |
| `/redoc` | **ReDoc** — una versión más de lectura/documento, sin botones para probar. |
| `/openapi.json` | El esquema OpenAPI en crudo (JSON) — lo que consumen ambas interfaces. |

> 💡 Esa documentación **se arma sola** a partir de los type hints, los modelos Pydantic
> (`TicketCreate`, `TicketResponse`) y los `Path`/`Query` que ya declaramos — es la misma
> información que usa FastAPI para *validar*, reutilizada para *documentar*. No hay que
> mantener un Swagger a mano por separado.

> 🧪 Tip de entrevista: ¿qué es OpenAPI, exactamente? Es el **estándar** (antes llamado
> Swagger) que describe una API en JSON/YAML — endpoints, parámetros, esquemas de
> entrada/salida. Swagger UI es solo **una** herramienta que sabe leer ese estándar y
> mostrarlo como una página interactiva; podría haber otras.

## 🚨 6. Manejo de errores con `HTTPException`
Cuando algo sale mal por una razón de negocio (no un bug), se lanza una `HTTPException`
con el código HTTP correcto — FastAPI la convierte en una respuesta JSON de error.

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

tickets_db = {1001: {"id": 1001, "title": "Error de acceso"}}

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    if ticket_id not in tickets_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} no encontrado",
        )
    return tickets_db[ticket_id]
```
```
GET /tickets/1001 -> 200 {'id': 1001, 'title': 'Error de acceso'}
GET /tickets/9999 -> 404 {'detail': 'Ticket 9999 no encontrado'}
```

> 💡 Es el mismo principio que `raise ValueError(...)` de la Clase 1, adaptado a HTTP:
> en vez de una excepción genérica de Python, `HTTPException` lleva **el código de
> estado** pegado al error, para que quien consuma la API sepa exactamente qué pasó.

> 📌 Cuando el proyecto tiene varias excepciones propias del dominio (como las
> `DomainError`/`RequestNotFoundError` que vimos en la Clase 1), FastAPI permite
> registrar un **`exception_handler`** que traduce cada una a su `HTTPException`
> correspondiente en un solo lugar, en vez de repetir el `if`/`raise` en cada endpoint.

## 🧱 7. Middleware
Un **middleware** es código que se ejecuta **alrededor de cada petición**, antes y/o
después de que llegue al endpoint — sirve para lógica transversal (logging, medir
tiempos, agregar headers) sin repetirla en cada función.

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)          # deja pasar la petición al endpoint
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)   # agrega algo a TODAS las respuestas
    return response

@app.get("/tickets")
def list_tickets():
    return {"tickets": []}
```
```
GET /tickets -> 200, header 'X-Process-Time' presente en la respuesta
```

> 💡 `call_next(request)` es la bisagra: todo lo que va **antes** de esa línea corre
> antes del endpoint, todo lo que va **después** corre una vez que el endpoint ya
> respondió — así un mismo middleware puede envolver la petición por los dos lados.

## 🌐 8. Diseño de APIs RESTful: buenas prácticas y versionamiento
**REST** no es una tecnología sino un **estilo** de diseño de API, con convenciones que
la hacen predecible para cualquiera que la use:

| Buena práctica | Ejemplo |
|---|---|
| Recursos como **sustantivos en plural** en la URL, no verbos | `/tickets` (bien) vs. `/getTickets` (mal — el verbo ya lo dice el método HTTP) |
| Jerarquía de recursos anidados cuando hay relación | `/tickets/1001/comments` (comentarios de ESE ticket) |
| Usar el **método HTTP** correcto para la acción (sección 2) | `DELETE /tickets/1001`, no `POST /tickets/1001/delete` |
| Devolver el **código de estado** correcto (sección 4) | `404` si no existe, no un `200` con `{"error": "..."}` |
| **Versionar** la API cuando hay cambios que rompen compatibilidad | `/v1/tickets` → `/v2/tickets` |

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

v1 = APIRouter(prefix="/v1")

@v1.get("/tickets")
def list_tickets_v1():
    return {"version": 1, "tickets": []}

app.include_router(v1)
# la ruta real queda montada en /v1/tickets
```

> ⚠️ Confundir "cambiar algo en la API" con "romper la API" es un error común: agregar un
> campo nuevo opcional a una respuesta normalmente **no** rompe a los clientes actuales;
> quitar un campo o cambiarle el tipo, sí — eso es lo que justifica subir de versión.

> 🧪 Tip de entrevista: ¿por qué versionar en la URL (`/v1/...`) y no solo con un header?
> Versionar en la URL es más simple de probar (se puede pegar en el navegador o en
> Swagger) y más visible; versionar por header es más "puro" a nivel REST pero menos
> práctico para debuggear rápido. FastAPI soporta ambos con `APIRouter`.

> 🔗 Fuentes usadas para verificar esta teoría (búsqueda web, agosto 2026):
> [Primeros pasos — FastAPI (docs oficiales)](https://fastapi.tiangolo.com/es/tutorial/first-steps/) ·
> [Query Parameters and String Validations — FastAPI](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/) ·
> [Documentación automática con Swagger y OpenAPI en FastAPI](https://certidevs.com/tutorial-fastapi-swagger-openapi-docs) ·
> [Diseño de RESTful APIs — buenas prácticas](https://www.arsys.es/blog/guia-completa-para-el-diseno-de-restful-api-conceptos-y-mejores-practicas) ·
> [Versionamiento de APIs REST](https://medium.com/@espinozajge/versionamiento-de-apis-rest-mejores-pr%C3%A1cticas-y-consideraciones-4b5021dd0a11)

# 💻 PARTE PRÁCTICA
*(pendiente)*

# 🏋️ EJERCICIOS CON SOLUCIÓN
*(pendiente — se documentan 10 ejercicios graduales cuando haya contenido de la clase)*

## ❓ Preguntas y respuestas (autoevaluación)
*(pendiente — 10 preguntas graduales)*

## 📎 Apuntes relacionados
*(pendiente)*

## ➡️ Siguiente
[Clase 4](Clase-04.md)
