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

## 🗂️ Índice de esta clase

**📖 Parte teórica**
1. [¿Qué es una API REST?](#🌐-1-¿que-es-una-api-rest)
   - [Cómo se conectan frontend, backend y base de datos](#🔌-como-se-conectan-frontend-backend-y-base-de-datos) — con diagrama
2. [Qué es FastAPI y primer proyecto](#🚀-2-que-es-fastapi-y-primer-proyecto)
   - [¿Qué es Uvicorn y cómo se relaciona con main.py?](#🦄-¿que-es-uvicorn-y-como-se-relaciona-con-main-py) — con diagrama
3. [Endpoints, rutas y métodos HTTP](#🛣️-3-endpoints-rutas-y-metodos-http) — con captura real
4. [Parámetros: path, query y body (validación con Pydantic)](#🧾-4-parametros-path-query-y-body-validacion-con-pydantic)
5. [Request y Response: status codes y `response_model`](#📤-5-request-y-response-status-codes-y-response-model)
6. [Documentación automática: Swagger UI y OpenAPI](#📚-6-documentacion-automatica-swagger-ui-y-openapi)
7. [Manejo de errores con `HTTPException`](#🚨-7-manejo-de-errores-con-httpexception)
8. [Middleware](#🧱-8-middleware)
9. [Diseño de APIs RESTful: buenas prácticas y versionamiento](#🌐-9-diseno-de-apis-restful-buenas-practicas-y-versionamiento)

**💻 Parte práctica**
- [Primer proyecto — 02-Ejercicios/Clase-03/](#🧪-primer-proyecto-—-02-ejercicios-clase-03)

**🏋️ Ejercicios y autoevaluación**
- [Ejercicios con solución](#🏋️-ejercicios-con-solucion) *(pendiente)*
- [Preguntas y respuestas](#❓-preguntas-y-respuestas-autoevaluacion) *(pendiente)*

# 📖 PARTE TEÓRICA

> 📌 **La mayoría de esta teoría no viene de la clase real dictada** (no pasé grabación
> completa de la Clase 3) — es **teoría estándar de referencia**, armada a partir de los
> 12 puntos del temario (ver "Qué aprendí" arriba), verificada con fuentes externas y en
> terminal (mismo criterio que usé para la [Clase 2](Clase-02.md)). **Excepción: la
> sección 3 (Endpoints, rutas y métodos HTTP)** ya tiene una captura real de la
> diapositiva del profesor — el resto sigue pendiente. A medida que llegue más material
> real, esta sección se revisa y se completa con los ejemplos/orden que se hayan dado —
> no se descarta, se
> enriquece.

## 🌐 1. ¿Qué es una API REST?
**API** (*Application Programming Interface*) es el contrato que le permite a dos
programas hablarse sin que ninguno conozca los detalles internos del otro — pedís algo
por una interfaz conocida, no te importa cómo está resuelto adentro.

**REST** (*Representational State Transfer*) no es una tecnología ni un protocolo: es un
**estilo de diseño** para construir APIs sobre HTTP, definido por Roy Fielding en el año
2000. Una API se considera RESTful cuando sigue estos principios:

| Principio | Qué significa | Ejemplo en esta clase |
|---|---|---|
| Cliente-servidor | El cliente (frontend) y el servidor (backend) están separados — cada uno evoluciona solo. | El frontend no sabe si el backend usa PostgreSQL o SQLite. |
| Sin estado (*stateless*) | Cada petición trae **toda** la información que necesita; el servidor no recuerda peticiones anteriores. | Cada `GET /tickets/1001` es independiente — no hay "sesión" a medias. |
| Recursos identificados por URL | Cada "cosa" del dominio tiene su propia dirección. | `/tickets/1001` identifica **ese** ticket, no una acción. |
| Interfaz uniforme | Los mismos métodos HTTP (`GET`/`POST`/`PUT`/`PATCH`/`DELETE`, sección 3) sirven para cualquier recurso. | `DELETE /tickets/1001` borra igual que `DELETE /users/7`. |
| Representaciones | El recurso viaja como una **representación** (normalmente JSON), no como el objeto real del servidor. | El `Ticket` de Python nunca "viaja" — viaja su representación en JSON. |

> 💡 **Por qué "sin estado" es la parte que más sorprende:** significa que el backend no
> guarda "en qué paso vas" entre una petición y la siguiente — si hace falta identificar
> quién sos, esa información viaja **en cada petición** (por ejemplo, un token en el
> header), no queda guardada del lado del servidor esperando la próxima llamada.

### 🔌 Cómo se conectan frontend, backend y base de datos
Una petición REST típica atraviesa **tres capas**, cada una con una responsabilidad
distinta:

1. **Frontend** (navegador, app móvil, otro servicio) arma una petición HTTP — método,
   URL, y a veces un `body` JSON — y la envía a una URL del backend.
2. **Backend** (FastAPI) la recibe, **valida** los datos con Pydantic (sección 4), ejecuta
   la lógica de negocio, y si necesita datos persistentes, se los pide a la base de datos
   (normalmente a través de un ORM como SQLAlchemy — se ve completo en la
   [Clase 4](Clase-04.md)).
3. **Base de datos** ejecuta la consulta y devuelve filas al backend, que las convierte de
   vuelta en una respuesta (JSON + código de estado, sección 5) y se la manda al frontend.

El diagrama siguiente muestra ese recorrido completo con un ejemplo real de esta clase
(`GET /tickets/{id}`), incluyendo el camino cuando el ticket **sí** existe y cuando
**no** existe (`404`, sección 7):

![Diagrama de secuencia: Cliente pide GET /tickets/{id} a FastAPI; dentro de un fragmento ALT, si el ticket existe FastAPI consulta la base de datos, recibe la fila y responde 200 OK con el JSON al cliente; si no existe, FastAPI consulta igual, la base de datos no devuelve resultados y FastAPI responde 404 Not Found](/clase-03-frontend-backend-bd.svg)

> 📎 Versión interactiva en el
> [Artifact publicado](https://claude.ai/code/artifact/6d30adf9-de87-4385-8adf-efc3238f1a91) —
> fuente editable en `04-Recursos/diagramas/clase-03-frontend-backend-bd.html`.

> ⚠️ **Punto clave del diagrama:** el frontend **nunca** habla directo con la base de
> datos — siempre pasa por el backend. Es el backend el único que conoce las credenciales
> de la base de datos y las reglas de negocio; el frontend solo conoce la URL de la API.

## 🚀 2. Qué es FastAPI y primer proyecto
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
# app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="Mi primera API con FastAPI",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message": "¡Hola, mundo! Helpdesk API funcionando correctamente."}
```

```bash
python -m uvicorn app.main:app --reload
```
```
{"message":"¡Hola, mundo! Helpdesk API funcionando correctamente."}
```
*(salida real — mismo código y comando que corriste vos en la Parte Práctica más abajo,
verificado levantando el servidor y pidiendo `GET /` con `curl`)* — y así se ve en el
navegador, como resultado:

![Captura real del navegador en localhost:8000, mostrando la respuesta JSON de la primera API: {"message": "¡Hola, mundo! Helpdesk API funcionando correctamente."}](/clase-03-primera-api-navegador.png)

| Pieza | Qué es |
|---|---|
| `FastAPI(title=..., version=...)` | Crea la aplicación — es el objeto central al que se le "cuelgan" todas las rutas. `title`/`version` son opcionales: no cambian el comportamiento, solo lo que se muestra en `/docs` (sección 6). |
| `uvicorn` | El **servidor ASGI** que hace correr la app — FastAPI define la lógica, `uvicorn` la sirve por HTTP (ver [¿Qué es Uvicorn?](#🦄-¿que-es-uvicorn-y-como-se-relaciona-con-main-py) abajo). |
| `python -m uvicorn` | Le pide a **este `python3` puntual** (el del venv activo) que ejecute el módulo `uvicorn` — evita el clásico "¿cuál `uvicorn` está corriendo?" si el del `PATH` no es el del venv. `uvicorn ...` a secas funciona igual una vez activado el venv, pero `python -m uvicorn` es más a prueba de errores. |
| `app.main:app` | Le dice a Uvicorn "en el paquete `app`, módulo `main.py`, la variable `app`" — `app.main` es la ruta del módulo (con puntos, no barras), lo que sigue a `:` es el nombre de la variable `app = FastAPI()` dentro de ese archivo. |
| `--reload` | Reinicia el servidor solo cuando cambia el código — para desarrollo, nunca en producción. |

> 💡 FastAPI está construido sobre dos librerías que ya conocemos: **Starlette** (la
> parte que maneja HTTP de bajo nivel) y **Pydantic** (la que valida los datos con las
> clases que vimos en la Clase 2/1). Elegirlo no es magia — combina piezas ya probadas.

> 🧪 Tip de entrevista: ¿por qué FastAPI se considera "rápido" en dos sentidos? Rápido en
> **ejecución** (por Starlette + soporte async) y rápido en **desarrollo** (menos código
> repetido gracias a los type hints y la documentación automática).

### 🦄 ¿Qué es Uvicorn y cómo se relaciona con `main.py`?
Ya apareció en la tabla de arriba: `uvicorn` es el **servidor ASGI** que hace correr la
app. Profundicemos qué significa eso — FastAPI define **qué** responder; Uvicorn es
quien la **sirve** por la red. Sin un servidor ASGI corriendo, `app = FastAPI()` es
solo un objeto en memoria, nadie puede pedirle nada por HTTP.

![Página de Uvicorn en PyPI: "uvicorn — The lightning-fast ASGI server", con el comando pip install uvicorn y el link a la documentación oficial uvicorn.dev](/clase-03-uvicorn-pypi.png)

> 🔗 Documentación oficial: [uvicorn.dev](https://uvicorn.dev) ·
> [pypi.org/project/uvicorn](https://pypi.org/project/uvicorn/)

**ASGI** (*Asynchronous Server Gateway Interface*) es el estándar que define cómo un
servidor como Uvicorn se comunica con un framework como FastAPI — el sucesor de WSGI
(el estándar más viejo, síncrono, que usan Flask/Django clásico) pensado para manejar
código `async`/`await` de forma nativa.

El diagrama siguiente muestra la relación completa: quién llama a quién, y de dónde
sale el propio ejecutable `uvicorn` — del `venv/` activado (ver Parte Práctica).

![Diagrama de arquitectura: Cliente hace GET / a Uvicorn; Uvicorn llama a read_root() dentro de app/main.py y devuelve la respuesta; abajo, venv/ provee el ejecutable bin/uvicorn a Uvicorn y el paquete fastapi instalado a main.py](/clase-03-uvicorn-main-py.svg)

> 📎 Versión interactiva en el
> [Artifact publicado](https://claude.ai/code/artifact/a92a04b4-8c5f-4813-acfd-0a9326e60bb2) —
> fuente editable en `04-Recursos/diagramas/clase-03-uvicorn-main-py.html`.

> ⚠️ **`app.main:app` — dos partes distintas, mismo nombre `app`:** a la izquierda de
> `:`, `app.main` es una **ruta de módulo** (`app/main.py`, con `app/` como paquete
> gracias a `__init__.py`). A la derecha de `:`, `app` es el **nombre de la variable**
> `app = FastAPI()` dentro de ese archivo — no tiene nada que ver con la carpeta `app/`
> aunque se llamen igual. Si `main.py` guardara la app en una variable `api` en vez de
> `app`, el comando sería `uvicorn app.main:api`.

## 🛣️ 3. Endpoints, rutas y métodos HTTP
Un **endpoint** (o *path operation*) es la combinación de una **ruta** (URL) y un
**método HTTP** — cada combinación dispara una función Python distinta.

![Tabla del profesor — un endpoint combina método HTTP + ruta + función: Listar (GET /tickets → 200), Consultar (GET /tickets/{id} → 200), Registrar (POST /tickets → 201), Actualizar (PATCH /tickets/{id} → 200), Eliminar (DELETE /tickets/{id} → 204)](/clase-03-tabla-endpoints-profesor.png)

> 📸 **Captura real de la Clase 3** (primera de esta clase — hasta acá la teoría era
> "estándar de referencia", ver nota al inicio de la Parte Teórica). El profesor definió
> el endpoint como **método + ruta + función**, con una tabla de las 5 operaciones CRUD
> del dominio de tickets y su código de estado esperado. El código de abajo ya está
> ajustado para devolver **exactamente** esos códigos — verificado en terminal.

```python
from fastapi import FastAPI, status

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

@app.post("/tickets", status_code=status.HTTP_201_CREATED)  # POST: crear
def create_ticket(title: str, priority: str = "Media"):
    new_ticket = {"id": 1003, "title": title, "priority": priority}
    tickets_db.append(new_ticket)
    return new_ticket

@app.patch("/tickets/{ticket_id}")   # PATCH: actualizar PARCIAL (solo priority)
def update_ticket(ticket_id: int, priority: str):
    for t in tickets_db:
        if t["id"] == ticket_id:
            t["priority"] = priority
            return t
    return {"error": "no encontrado"}

@app.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)  # DELETE: borrar
def delete_ticket(ticket_id: int) -> None:
    global tickets_db
    tickets_db = [t for t in tickets_db if t["id"] != ticket_id]
```
```
GET    /tickets       -> 200  [{'id': 1001, ...}, {'id': 1002, ...}]
GET    /tickets/1001  -> 200  {'id': 1001, 'title': 'Error de acceso', 'priority': 'Alta'}
POST   /tickets       -> 201  {'id': 1003, 'title': 'Nueva falla', 'priority': 'Baja'}
PATCH  /tickets/1001  -> 200  {'id': 1001, 'title': 'Error de acceso', 'priority': 'Cerrado'}
DELETE /tickets/1002  -> 204  (sin body — verificado: size_download 0)
```

| Método | Para qué | Analogía CRUD |
|---|---|---|
| `GET` | Leer/consultar (no modifica nada) | Read |
| `POST` | Crear un recurso nuevo | Create |
| `PUT` | Reemplazar/actualizar un recurso **entero** | Update total |
| `PATCH` | Actualizar **parcialmente** (solo algunos campos) | Update parcial |
| `DELETE` | Eliminar un recurso | Delete |

> ⚠️ **`PUT` vs. `PATCH` — por qué el ejemplo usa `PATCH`:** `update_ticket()` solo
> recibe y cambia `priority`, deja el resto del ticket intacto — eso es una
> actualización **parcial**, el caso de uso exacto de `PATCH`. `PUT` sería el método
> correcto si la función reemplazara el ticket **completo** (todos sus campos) en cada
> llamada. La versión anterior de este ejemplo usaba `PUT` para esto mismo — quedaba
> mal etiquetado (parcial con el método de "reemplazo total"); ya está corregido acá y
> coincide con la tabla real de la clase (`PATCH` → 200).
>
> 💡 **`status_code=...` en el decorador:** así se fuerza el código de estado que
> devuelve FastAPI — sin esto, `POST`/`PATCH`/`DELETE` devuelven `200` por defecto. La
> convención REST (y la tabla del profesor) pide `201` al crear y `204` (sin body) al
> borrar — `-> None` en `delete_ticket` es la pista para FastAPI de que no hay nada que
> serializar en la respuesta.

> ⚠️ `GET` nunca debería modificar datos (no debería tener efectos secundarios) — si una
> operación cambia algo, el método correcto es `POST`/`PUT`/`PATCH`/`DELETE`, nunca `GET`.

## 🧾 4. Parámetros: path, query y body (validación con Pydantic)
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

## 📤 5. Request y Response: status codes y `response_model`
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

## 📚 6. Documentación automática: Swagger UI y OpenAPI
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

## 🚨 7. Manejo de errores con `HTTPException`
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

## 🧱 8. Middleware
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

## 🌐 9. Diseño de APIs RESTful: buenas prácticas y versionamiento
**REST** no es una tecnología sino un **estilo** de diseño de API, con convenciones que
la hacen predecible para cualquiera que la use:

| Buena práctica | Ejemplo |
|---|---|
| Recursos como **sustantivos en plural** en la URL, no verbos | `/tickets` (bien) vs. `/getTickets` (mal — el verbo ya lo dice el método HTTP) |
| Jerarquía de recursos anidados cuando hay relación | `/tickets/1001/comments` (comentarios de ESE ticket) |
| Usar el **método HTTP** correcto para la acción (sección 3) | `DELETE /tickets/1001`, no `POST /tickets/1001/delete` |
| Devolver el **código de estado** correcto (sección 5) | `404` si no existe, no un `200` con `{"error": "..."}` |
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

## 🧪 Primer proyecto — `02-Ejercicios/Clase-03/`
Arranque del proyecto: entorno virtual creado y esqueleto del paquete `app/` — todavía
sin el código de la sección 2 adentro (ese es el próximo paso).

```bash
# Entorno virtual (macOS/Linux) — comando real ejecutado
python3 -m venv venv
```

> 📝 **Nombre distinto al resto del curso:** en las Clases 1 y 2 el entorno se creó como
> `.venv` (oculto, con punto inicial); acá se creó como `venv` (visible, sin punto). Los
> dos son válidos — `venv` es solo el nombre de una carpeta cualquiera — pero conviene
> elegir **un solo criterio** para todo el curso, si no hay que acordarse cuál usa cada
> clase. Si se quiere unificar con `.venv`, simplemente se borra esta carpeta y se vuelve
> a crear con `python3 -m venv .venv` (no hace falta reinstalar nada más, porque todavía
> no hay dependencias instaladas — ver nota siguiente).

```bash
# Activación (macOS/Linux)
source venv/bin/activate

# Activación (Windows, referencia)
.\venv\Scripts\activate
```

> ⚠️ **Error real al activar — comando de Windows en zsh:** el primer intento fue
> `venv\Scripts\activate` (sintaxis de Windows) copiado tal cual en la terminal de
> macOS, y tiró `zsh: command not found: venvScriptsactivate` — zsh no interpreta `\`
> como separador de carpetas, y en macOS el venv crea `bin/`, no `Scripts/`. La
> solución fue el comando de arriba (`source venv/bin/activate`) — mismo error ya
> documentado en [[2026-08-14-activate-sin-source-no-funciona]] (ahí pasó con `.venv`
> en la Clase 1; acá con `venv` en la Clase 3, mismo motivo).

**Dependencias instaladas — ya verificado en `venv/`:**
```bash
pip install fastapi "uvicorn[standard]"
```
```
fastapi           0.141.1
starlette         1.6.0
pydantic          2.13.4
uvicorn           0.52.4
```

**`app/main.py` — primer endpoint real, ya escrito:**
```python
from fastapi import FastAPI

app = FastAPI(
    title="Mi primera API con FastAPI",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message": "¡Hola, mundo! Helpdesk API funcionando correctamente."}
```

> 💡 Variante de la sección 2: acá `FastAPI(title=..., version=...)` — esos dos
> parámetros no cambian el comportamiento del endpoint, solo el nombre y la versión que
> se muestran en la documentación automática (`/docs`, sección 6). El nombre de la
> función (`home`) tampoco importa para la ruta — lo que decide la URL es
> `@app.get("/")`, no el nombre de la función de abajo.

**Estructura actual:**
```
02-Ejercicios/Clase-03/
├── venv/                 # entorno virtual, activado — fastapi + uvicorn instalados
├── requeriments.txt      # vacío todavía — falta `pip freeze > requeriments.txt`
└── app/
    ├── __init__.py       # vacío — convierte app/ en paquete Python
    └── main.py           # primer endpoint funcionando (arriba)
```

**Arrancado y probado — comando real ejecutado:**
```bash
python -m uvicorn app.main:app --reload
```
```
INFO:     Will watch for changes in these directories: ['.../02-Ejercicios/Clase-03']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [87104] using WatchFiles
INFO:     Started server process [87106]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

| Línea | Qué significa |
|---|---|
| `Will watch for changes in these directories` | Con `--reload` activo, Uvicorn vigila **todos los archivos `.py`** de esa carpeta — si guardás un cambio, reinicia el servidor solo (sección "Próximo paso" de más arriba, tabla de la sección 2). |
| `Uvicorn running on http://127.0.0.1:8000` | La URL real donde escucha — `127.0.0.1` es "esta misma máquina" (no accesible desde otra computadora), puerto `8000` por defecto. |
| `Started reloader process [87104] using WatchFiles` | Con `--reload`, Uvicorn arranca **dos procesos**: uno "vigía" (reloader, PID 87104) que solo mira archivos y reinicia al otro cuando cambian. |
| `Started server process [87106]` | El proceso que **realmente** corre tu app (PID distinto al reloader) — este es el que se reinicia cada vez que guardás. |
| `Waiting for application startup.` / `Application startup complete.` | Dos pasos separados porque FastAPI permite código que corre **una sola vez al arrancar** (`@app.on_event("startup")`, no visto todavía) — acá no hay ninguno definido, así que pasa de un mensaje al otro casi al instante. |

> ✅ **Verificado:** `GET http://127.0.0.1:8000/` responde `200` con
> `{"message": "¡Hola, mundo! Helpdesk API funcionando correctamente."}` — el primer
> endpoint de esta clase, corriendo de verdad (captura del resultado real en la
> sección 2, justo debajo del código).

> 📝 **Typo en el nombre del archivo:** `requeriments.txt` — el nombre estándar en
> proyectos Python es `requirements.txt` (con "i" antes de "re**i**ments" en vez de
> después). Sigue vacío — falta `pip freeze > requeriments.txt` para congelar
> `fastapi`/`uvicorn`. No rompe nada mientras nadie más lo busque por el nombre exacto
> (ni `pip` ni FastAPI asumen ese nombre — es solo convención), pero conviene
> corregirlo antes de que otros comandos/documentación lo referencien mal escrito.

# 🏋️ EJERCICIOS CON SOLUCIÓN
*(pendiente — se documentan 10 ejercicios graduales cuando haya contenido de la clase)*

## ❓ Preguntas y respuestas (autoevaluación)
*(pendiente — 10 preguntas graduales)*

## 📎 Apuntes relacionados
*(pendiente)*

## ➡️ Siguiente
[Clase 4](Clase-04.md)
