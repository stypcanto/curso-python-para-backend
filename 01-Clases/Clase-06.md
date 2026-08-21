---
sidebar: "Clase 6 · Microservicios FastAPI"
---

# 📙 Clase 6 — Construcción de microservicios con FastAPI

> Python para Backend · 2026-08-20 · Carpeta: `02-Ejercicios/Clase-06`
> ⬅️ Volver al [índice de clases](00-Indice.md)

## 🎯 Qué aprendí
- Creación del microservicio de usuarios
- Creación del microservicio de productos
- Configuración independiente por servicio
- Variables de entorno
- Documentación por servicio
- Ejecución y pruebas

> 📝 Clase completa: código verificado de punta a punta (ver
> [Verificación](#✅-verificacion-—-corri-ambos-servicios-de-verdad)), 10 ejercicios y
> 10 preguntas de autoevaluación.

# 📖 PARTE TEÓRICA

## 📚 1. Definiciones clave

### Pydantic
| Término | Qué es | Se profundiza en |
|---|---|---|
| `EmailStr` | Tipo de Pydantic que valida que el valor tenga **formato de correo electrónico** (`algo@dominio.com`); si no cumple el formato, Pydantic rechaza el dato antes de que llegue a la lógica del endpoint. Requiere el paquete extra `email-validator` instalado junto a Pydantic. | sección 4 |
| `Field(...)` | Ya visto en [Clase 4](Clase-04.md) — función de Pydantic para sumar reglas a un campo (`min_length`, `max_length`, etc.). Aquí se reutiliza igual. | sección 4 |
| Herencia de esquemas (`class B(A)`) | Un esquema de salida (`UserResponse`) puede **heredar** de uno de entrada (`UserCreate`) para no repetir sus campos, y sumar solo lo que le falta (p. ej. `id`). Mismo mecanismo de herencia de Python aplicado a modelos Pydantic. | sección 4 |

### Arquitectura de microservicios
| Término | Qué es | Se profundiza en |
|---|---|---|
| Servicio independiente (`users_service` / `products_service`) | Cada microservicio vive en su **propia carpeta**, con su propio `app/`, `venv/`, `requirements.txt`, `.env` y tests — no comparte código, proceso ni entorno con el otro. Es la aplicación práctica de "Database per Service" visto en la [Clase 5](Clase-05.md). | sección 2 |

### `pydantic-settings`
| Término | Qué es | Se profundiza en |
|---|---|---|
| `BaseSettings` / `SettingsConfigDict(env_file=...)` | Ya visto en [Clase 4](Clase-04.md#🗄️-9-modelos-sqlalchemy-orm-user-category-ticket) — mismo patrón para leer configuración desde un `.env`. Ahí se usó para `database_url`; acá se reaplica con otros campos (ver sección 3). | sección 3 |

### FastAPI
| Término | Qué es | Se profundiza en |
|---|---|---|
| `APIRouter` | Objeto de FastAPI para **agrupar endpoints relacionados** en su propio archivo (`routers/users.py`) en vez de meter todo en `main.py`; después se "engancha" a la app principal. | sección 5 |
| `APIRouter(prefix=..., tags=[...])` | `prefix` antepone una ruta base a todos los endpoints del router (`/users`); `tags` los agrupa visualmente en la documentación Swagger. | sección 5 |
| `summary="..."` | Título corto que muestra Swagger junto al método HTTP de **un endpoint puntual** (a diferencia de `tags`, que agrupa varios). Si no se pasa, FastAPI genera uno solo a partir del nombre de la función (`list_products` → "List Products"). | sección 5 |
| `status` (de `fastapi`) | Módulo con las constantes de códigos HTTP legibles (`status.HTTP_201_CREATED` en vez de escribir `201` a mano). | sección 5 |
| `@router.post(...)` | Decorador que registra una función como el **endpoint** que atiende `POST` a esa ruta del router. | sección 5 |
| `data: UserCreate` | Parámetro **tipado con un esquema Pydantic** — FastAPI lo usa para leer y validar el JSON del `body` de la petición automáticamente (si no cumple `UserCreate`, responde `422` sin llegar a ejecutar la función). | sección 5 |
| `.model_dump()` | Método de Pydantic que convierte una instancia del modelo (`data`) en un **`dict`** plano — necesario para mezclarlo con otros campos (`**data.model_dump()`). | sección 5 |
| `**data.model_dump()` | *Unpacking* de diccionario: "desempaqueta" cada clave del dict como si fuera escrita a mano — mecánica genérica de Python, no de Pydantic. | sección 5 |

### Testing
| Término | Qué es | Se profundiza en |
|---|---|---|
| `pytest` | Framework de testing de Python — descubre y corre funciones `test_*` automáticamente, sin necesidad de heredar de una clase (a diferencia de `unittest`, el módulo de testing de la librería estándar). | sección 7 |
| `httpx` | Cliente HTTP para Python, sucesor moderno de `requests` — mismo estilo de API (`httpx.get(...)`, `httpx.post(...)`), pero con soporte nativo para `async`/`await`. Es una dependencia que usa `TestClient` por debajo, aunque no se importe directo en el test. | sección 7 |
| `TestClient` (de `fastapi.testclient`) | Cliente que simula peticiones HTTP **contra tu propia app en memoria**, sin levantar un servidor real ni ocupar un puerto — así los tests corren rápido y aislados. | sección 7 |

## 🗂️ 2. Arquitectura: dos microservicios independientes

La Clase 6 arranca construyendo **dos microservicios independientes** dentro de un mismo
repo de trabajo (`project/`), cada uno con su propia estructura de carpetas — así
`users_service` no depende en nada de `products_service` (ni al revés), mismo principio
"Database per Service" que ya vimos en la [Clase 5](Clase-05.md):

```
project/
├── users_service/
│   ├── app/
│   │   ├── routers/
│   │   │   └── users.py      ← endpoints
│   │   ├── config.py         ← configuración
│   │   ├── main.py           ← arranque de la app FastAPI
│   │   └── schemas.py        ← esquemas Pydantic
│   ├── tests/
│   ├── venv/                 ← su propio entorno virtual
│   ├── .env
│   └── requirements.txt
│
└── products_service/
    ├── app/
    │   ├── routers/
    │   │   └── products.py   ← endpoints
    │   ├── config.py         ← configuración
    │   ├── main.py           ← arranque de la app FastAPI
    │   └── schemas.py        ← esquemas Pydantic
    ├── tests/
    ├── venv/                 ← su propio entorno virtual, aparte del de users_service
    ├── .env
    └── requirements.txt
```

> 💡 Mismo patrón que ya usamos con `products-service` / `notifications-service` en la
> [Clase 5](Clase-05.md), pero ahora con FastAPI en vez de Flask, y con una carpeta `app/`
> interna para separar routers de la configuración.

Los dos servicios quedaron **verificados y corriendo** (ver [Parte práctica](#💻-parte-practica))
— este documento sigue el mismo orden en el que se arma un servicio en la práctica:
**configuración → esquemas → endpoints → arranque de la app.**

### 🗺️ Diagrama: arquitectura de la Clase 6

![Diagrama de arquitectura: users_service (puerto 8001) y products_service (puerto 8002), cada uno con su config.py, main.py, routers/*.py y una lista en memoria; el Cliente llama a ambos por HTTP, y products_service consulta a users_service por su API pública (httpx) para validar un owner_id, sin conocer su modelo interno](/clase-06-arquitectura-microservicios.png)

> 📎 Fuente editable en
> `04-Recursos/diagramas-tecnicos/clase-06-arquitectura-microservicios/` (`.dot` + instrucciones
> para regenerarlo).

### ⚠️ "Microservicio" y "router" NO son lo mismo

Fácil de confundir porque en esta clase coinciden 1 a 1 (`users_service` tiene un solo
`users.py`, `products_service` tiene un solo `products.py`) — pero son conceptos
distintos, y esa coincidencia **no es una regla**:

| | Microservicio | Router |
|---|---|---|
| Qué es | Un **proceso independiente completo**: su propia carpeta, su propio `venv`, su propio puerto, su propio `main.py` | Un archivo que **agrupa endpoints** dentro de UNA sola app FastAPI (ver `APIRouter`, sección 5) |
| Ejemplo en tu proyecto | `users_service/` (carpeta entera, corre en el puerto 8001) | `users_service/app/routers/users.py` (un archivo *adentro* de esa carpeta) |
| Puede haber varios por... | — (cada microservicio es una unidad completa, no "vive dentro" de otra cosa) | Un microservicio puede tener **muchos routers** (`users.py`, `addresses.py`, `orders.py`, todos corriendo dentro del mismo proceso) |

**Ejemplo para notar la diferencia:** si mañana `users_service` necesita manejar también
las direcciones de los usuarios, agregarías `routers/addresses.py` **adentro de la misma
carpeta `users_service`** — seguiría siendo **un solo microservicio**, ahora con **2
routers**. Lo que define el límite de un microservicio es la carpeta/proceso/puerto
completo (ver arriba), no cuántos archivos de rutas tenga adentro.

### ❓ ¿Pueden dos microservicios usar la misma tecnología?

**Sí, sin problema** — de hecho es lo que hace este proyecto: los dos usan la misma pila
completa (Python, FastAPI, Pydantic, el mismo patrón de `config.py`/`schemas.py`/
`routers/`). La ventaja de los microservicios no es que **tengan** que usar tecnologías
distintas — es que **pueden**, si algún día hace falta (por ejemplo, reescribir solo
`products_service` en otro lenguaje sin tocar `users_service`, porque cada uno es un
proceso independiente). Lo que sí conviene mantener consistente entre servicios, usen o
no la misma tecnología, es **cómo se comunican entre ellos** — tema de la
[Clase 7](Clase-07.md).

### ❓ ¿Pueden dos microservicios usar el mismo puerto?

**No** — un puerto TCP solo admite **un proceso escuchando a la vez**, en la misma
máquina. Comprobado intentando levantar `users_service` en el 8002 (ya ocupado por
`products_service`):
```
ERROR: [Errno 48] error while attempting to bind on address ('127.0.0.1', 8002): address already in use
```
Por eso cada `config.py` de esta clase usa un puerto distinto (`8001` / `8002`, sección
3) — si coincidieran, el segundo servicio que arranque fallaría con este error.

### ❓ ¿`products_service` debe conocer el modelo interno de `users_service`?

**No.** Principio de desacoplamiento ya visto en la [Clase 5](Clase-05.md#🔓-principio-de-desacoplamiento-un-servicio-debe-conocer-lo-minimo-necesario):
*"un servicio no debería conocer más del otro que su contrato público"* (su API), nunca
su modelo interno. Si `products_service` necesitara un dato de un usuario, la forma
correcta es llamar a la **API** de `users_service` (`GET /api/v1/users/{user_id}`) y
quedarse solo con la forma del JSON que expone — nunca importar sus esquemas de
`users_service/app/schemas.py` ni leer directo su lista `users` en memoria.

| | 🔴 Alto acoplamiento (mal) | 🟢 Bajo acoplamiento (bien) |
|---|---|---|
| Acceso a datos de usuarios | `products_service` lee directo la estructura interna de `users_service` | `products_service` llama a `GET /api/v1/users/{id}` |
| Si `users_service` cambia su modelo interno | Puede romper `products_service` sin avisar | `products_service` no se entera — solo le importa que la API responda igual |

> 📝 Ahora mismo, en el código de esta clase, **esto todavía no aplica**: `products_service`
> y `users_service` no se comunican entre sí en absoluto, cada uno corre 100% aislado.
> Va a importar recién cuando algo necesite datos de los dos a la vez (por ejemplo, un
> futuro `orders_service` en la [Clase 7](Clase-07.md)).

### ❓ ¿Un microservicio puede tener su propio ritmo de versiones?

**Sí** — no comparten una sola versión global, cada uno se versiona por su cuenta. Prueba
concreta en este mismo proyecto: `users_service` quedó en `APP_VERSION=1.5.0` y
`products_service` en `APP_VERSION=1.1.0` (cada uno con su propio `.env`, sección 3) —
dos versiones distintas, al mismo tiempo, sin ningún conflicto entre ellas.

| | Monolito | Microservicios |
|---|---|---|
| Versión | Una sola para toda la app — cambia una línea, se redespliega todo junto | Una por servicio — cada uno se versiona, prueba y despliega de forma independiente |

Esa versión es la que arma Swagger (`title`/`version`, sección 6) — cada microservicio
muestra la suya en su propio `/docs`, sin relación con la del otro.

### ❓ ¿Quién es dueño de las reglas de un producto — `users_service` o `products_service`?

**`products_service`** — es su [Bounded Context](Clase-05.md#🧭-3-domain-driven-design-ddd-y-bounded-contexts)
(ya visto en Clase 5): el dueño de una regla es el servicio dueño del **dato** sobre el
que aplica. `users_service` no tiene ni debería tener ninguna línea de lógica sobre
productos. Ya está así en el código, sin que se haya pensado a propósito:

```python
# products_service/app/schemas.py — TODAS las reglas de un producto viven acá
price: Decimal = Field(gt=0, decimal_places=2)   # regla: precio > 0
stock: int = Field(default=0, ge=0)               # regla: stock no negativo
```

`users_service` no importa `Decimal` ni sabe que existe un campo `price` — si mañana
cambia una regla de negocio de producto, se toca **solo** `products_service`.

> 🧪 Tip de entrevista: si preguntan "¿dónde pongo esta validación?", la respuesta es
> "en el servicio dueño del dato", no "en el servicio que la necesita" — un futuro
> `orders_service` puede *necesitar* saber si hay stock, pero no es *dueño* de esa regla;
> se la pregunta a `products_service` por su API.

## 🔧 3. Configuración por servicio — `config.py`

Cada microservicio trae **su propia clase `Settings`** — no es un archivo compartido, es
un patrón que se repite en cada servicio, con sus propios valores:

**[`users_service/app/config.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/users_service/app/config.py)**
```python
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    app_name: str = "Users Service"
    app_version: str = "1.0.0"
    port: int = 8001

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
```

**[`products_service/app/config.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/products_service/app/config.py)** — idéntico en estructura, solo cambian los valores:
```python
class Settings(BaseSettings):
    app_name: str = "Products Service"
    app_version: str = "1.0.0"
    port: int = 8002          # ← distinto al 8001 de users_service
    # ... mismo model_config que arriba
```

| Línea | Qué hace |
|---|---|
| `class Settings(BaseSettings)` | Los 3 campos traen **valor por defecto** — si no hay `.env` o le falta alguna variable, la app arranca igual con estos valores. Distinto a Clase 4, donde `database_url: str` era **obligatorio** (sin default) porque sin conexión a la BD no tenía sentido arrancar. |
| `port: int = 8001` / `8002` | Cada servicio corre en **su propio puerto** — así pueden convivir en `localhost` al mismo tiempo, sin pisarse. |
| `model_config = SettingsConfigDict(env_file=".env", ...)` | Si existe un `.env` en la carpeta del servicio, `BaseSettings` lee de ahí y **sobreescribe** los valores por defecto. Mismo mecanismo que en [Clase 4](Clase-04.md). | |
| `settings = Settings()` | Instancia lista para importar desde `main.py` u otros módulos. |

**`users_service/.env`** — configurado y verificado (cargando `Settings()` real):
```env
APP_NAME=Users Service
APP_VERSION=1.5.0
PORT=8001
```
`APP_VERSION=1.5.0` sobreescribe el default `"1.0.0"` del código — confirmado con
`Settings().app_version == '1.5.0'`. `APP_NAME`/`PORT` quedan iguales al default, no
cambian nada. No hacen falta comillas en `Users Service` aunque tenga espacio:
`python-dotenv` toma todo lo que sigue al `=` tal cual, sin cortar en el espacio.

> ⚠️ `PORT` en el `.env` **no cambia en qué puerto arranca uvicorn** — eso lo define el
> flag `--port` al correr el servidor (sección práctica), no `settings.port`. Ahora mismo
> `main.py` no tiene ningún `uvicorn.run(app, port=settings.port)` que lea ese valor, así
> que `settings.port` es solo informativo por ahora.

**`products_service/.env`** — mismo patrón, con su propia versión:
```env
APP_NAME=Products Service
APP_VERSION=1.1.0
PORT=8002
```
Verificado igual que el de `users_service`: `Settings().app_version` sale `'1.1.0'`, no
el default `'1.0.0'` del código.

### ⏱️ ¿Cuándo se aplica el `.env`?

**Solo en un momento puntual: cuando arranca el proceso** — no de forma continua ni en
vivo:

```
1) Editás el .env
2) Guardás el archivo         ← el cambio SOLO existe en el archivo; la app corriendo
                                  no se entera
3) (nada pasa todavía)
4) Reiniciás el servidor      ← Settings() se crea DE NUEVO, recién ACÁ lee el .env
5) Recién ahí el cambio se refleja
```

`settings = Settings()` (última línea de `config.py`) corre **una sola vez**, la primera
vez que se importa el módulo — justo cuando arranca `uvicorn`. Desde ahí, `settings`
queda **congelado en memoria** con esos valores mientras el proceso siga vivo, sin
importar cuántas veces edites el `.env` después.

| ¿Qué hiciste? | ¿Se aplica? |
|---|---|
| Editar el `.env` con el servidor **apagado**, y después arrancarlo | ✅ sí, lo lee al arrancar |
| Editar el `.env` con el servidor **ya corriendo** | ❌ no, hasta que lo reinicies |
| Guardar un cambio en un archivo `.py` con `--reload` activo | ✅ eso sí se recarga solo — pero es otro mecanismo (vigila código, no `.env`) |

> 💡 Por eso al verificar en vivo se vio primero `version: "1.0.0"` en vez de `"1.5.0"`:
> el servidor ya estaba corriendo desde antes de guardar `APP_VERSION=1.5.0` en el
> `.env`. La única forma de que lo tome es **apagar y volver a prender** ese proceso
> puntual (`Ctrl+C` en la terminal donde corre, y volver a correr
> `python3 -m uvicorn app.main:app --reload --port 8001`).

> ⚠️ Ojo con la sintaxis del default en `config.py` — es un **valor normal de Python**,
> no una plantilla: `app_name: str = "Users Service"` es correcto; algo como
> `app_name: str = {APP.NAME}` (con llaves) **no funciona** — Python lo interpreta como
> un `set`/`dict` con la expresión `APP.NAME` adentro, y como `APP` no existe, tira
> `NameError` al importar el archivo y tumba el servidor entero. Pydantic empareja el
> campo `app_name` con la variable `APP_NAME` del `.env` **por nombre, automáticamente**
> — no hace falta (ni existe) una sintaxis especial para "conectarlos".

## 📐 4. Esquemas Pydantic — `schemas.py`

**[`users_service/app/schemas.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/users_service/app/schemas.py)**
```python
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
    )
    email: EmailStr


class UserResponse(UserCreate):
    id: int
```

| Línea | Qué hace |
|---|---|
| `class UserCreate(BaseModel)` | Esquema de **entrada**: lo que el cliente manda para crear un usuario. |
| `name: str = Field(min_length=3, max_length=100)` | `name` obligatorio, entre 3 y 100 caracteres — mismo patrón `Field(...)` que en la [Clase 4](Clase-04.md). |
| `email: EmailStr` | `email` obligatorio, validado como correo electrónico real (ver glosario). |
| `class UserResponse(UserCreate)` | Esquema de **salida**: hereda `name` y `email` de `UserCreate` y les suma `id: int` — así no repite los dos campos que ya validó `UserCreate`. |

**[`products_service/app/schemas.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/products_service/app/schemas.py)** — mismo patrón (`XCreate` + `XResponse(XCreate)` con `id`), aplicado a otro dominio:
```python
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=120,
    )

    price: Decimal = Field(
        gt=0,
        decimal_places=2,
    )

    stock: int = Field(
        default=0,
        ge=0,
    )


class ProductResponse(ProductCreate):
    id: int
```

| Línea | Qué hace |
|---|---|
| `price: Decimal = Field(gt=0, decimal_places=2)` | `Decimal` (no `float`) para **dinero** — evita los errores de redondeo binario de `float` (p. ej. `0.1 + 0.2 != 0.3`). `gt=0` exige precio positivo; `decimal_places=2` redondea/valida a 2 decimales (céntimos). |
| `stock: int = Field(default=0, ge=0)` | Entero con **valor por defecto** `0` (campo opcional al crear) y `ge=0` ("greater or equal") — no admite stock negativo. |

> 🧪 **Tip de entrevista:** ¿por qué `Decimal` y no `float` para precios? `float` usa
> representación binaria (IEEE 754) que no puede expresar exacto la mayoría de decimales
> — arrastra error de redondeo en sumas repetidas. `Decimal` usa representación decimal
> exacta, es el tipo correcto para dinero.

> ⚠️ `EmailStr` necesita el extra `email-validator` instalado aparte de Pydantic — si
> falta, `ImportError: email-validator is not installed` al importar el esquema. Ya
> resuelto en `users_service` (ver [Verificación](#✅-verificacion-—-corri-ambos-servicios-de-verdad));
> `products_service` no lo necesita porque su esquema no usa `EmailStr`.

## 🌐 5. Endpoints — `routers/*.py`

**[`users_service/app/routers/users.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/users_service/app/routers/users.py)** — completo, los 3 endpoints:
```python
from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.schemas import (
    UserCreate,
    UserResponse,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

users: list[dict] = []


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
):
    user = {
        "id": len(users) + 1,
        **data.model_dump(),
    }

    users.append(user)

    return user


@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users():
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
):
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado",
    )
```

| Línea | Qué hace |
|---|---|
| `router = APIRouter(prefix="/users", tags=["Users"])` | Todos los endpoints que se registren en `router` a partir de acá quedan bajo la ruta `/users` (ver glosario). |
| `users: list[dict] = []` | Lista **en memoria** que hace de "base de datos" temporal — se pierde al reiniciar el servicio (no hay persistencia todavía; contrasta con SQLAlchemy visto en [Clase 4](Clase-04.md)). |
| `def create_user(data: UserCreate):` | FastAPI recibe el `body`, lo valida contra `UserCreate` y lo entrega ya convertido en `data`. |
| `user = {"id": len(users) + 1, **data.model_dump()}` | Arma el `dict`: un `id` autoincremental simple (`len(users) + 1` — falla si se borra un usuario del medio) + los campos de `data` desempaquetados. |
| `def list_users(): return users` | `GET /users` — devuelve tal cual la lista en memoria, sin filtrar ni paginar. |
| `def get_user(user_id: int):` | `GET /users/{user_id}` — `user_id` es un **path parameter**: su nombre debe coincidir con el de la ruta (`{user_id}`) para que FastAPI sepa qué inyectar; el tipo `int` valida/convierte el segmento de la URL. |
| `for user in users: if user["id"] == user_id: return user` | Búsqueda lineal (`O(n)`) en la lista en memoria. |
| `raise HTTPException(status_code=404, detail=...)` | Si el `for` no encontró nada, corta y responde `404` — acá se usa finalmente el `HTTPException` importado arriba. |

> ⚠️ `id = len(users) + 1` es un contador ingenuo: con un `DELETE` se pueden repetir ids
> (si borro el usuario 2 de 3, el próximo alta vuelve a calcular `id = 3` y choca). Con
> una base de datos real ([Clase 4](Clase-04.md)) esto lo resuelve la columna
> autoincremental del motor.

**[`products_service/app/routers/products.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/products_service/app/routers/products.py)** — **mismo esqueleto**, cambiando `user`→`product`, más el filtro por stock (Ejercicio 1) y `summary` en español en los 3 endpoints:
```python
router = APIRouter(prefix="/products", tags=["Products"])
products: list[dict] = []

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED,
             summary="Crear producto")
def create_product(data: ProductCreate): ...

@router.get("", response_model=list[ProductResponse], summary="Listar producto")
def list_products(minimum_stock: int | None = None): ...  # filtro opcional, ver Ejercicio 1

@router.get("/{product_id}", response_model=ProductResponse,
            summary="Obtener producto filtrado")
def get_product(product_id: int): ...  # 404 "Producto no encontrado" si no existe
```

### 🏷️ `tags` vs `summary` — no son lo mismo

Los dos son metadatos que se le pasan al decorador (`@router.get(...)`), pero cumplen
roles distintos en la documentación de Swagger:

| | `tags` | `summary` |
|---|---|---|
| Qué hace | Agrupa varios endpoints bajo un mismo encabezado plegable en Swagger | Título corto de **un solo** endpoint, al lado del método HTTP |
| Dónde se define | Una vez en el `APIRouter(...)` — se hereda en **todos** sus endpoints | Por endpoint — cada `@router.get/post(...)` necesita el suyo |
| Si no se define | No hay agrupación (o usa el nombre del router por defecto) | FastAPI genera uno solo a partir del nombre de la función: `list_products` → "List Products" |

```python
router = APIRouter(
    prefix="/products",
    tags=["Products"],        # ← una vez acá, agrupa los 3 endpoints
)

@router.get(
    "",
    response_model=list[ProductResponse],
    summary="Listar producto",  # ← este sí, uno por endpoint
)
def list_products(...): ...
```

> 💡 Sin `summary`, Swagger no queda "vacío" — FastAPI arma un título automático en
> inglés a partir del nombre de la función. `summary="Listar producto"` lo reemplaza por
> un texto elegido a mano, en español.

> 💡 Nota lo simétrico del diseño: `users.py` y `products.py` son **el mismo esqueleto**
> (crear / listar / buscar por id, lista en memoria, 404 si no existe) aplicado a dos
> dominios distintos — así se ve en la práctica qué significa "microservicios
> independientes pero con arquitectura consistente".

## 🚀 6. Arranque de la app — `main.py`

**[`users_service/app/main.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/users_service/app/main.py)**:
```python
from fastapi import FastAPI

from app.config import settings
from app.routers.users import router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Microservicio encargado "
        "de la gestión de usuarios."
    ),
)


@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
    }


app.include_router(
    router,
    prefix="/api/v1",
)
```

`products_service/app/main.py` es idéntico en estructura — solo cambian los imports
(`app.routers.products`) y el texto de `description`.

> ✅ Las líneas 1-9 de `users_service/main.py` (`title`/`version` desde `settings`) no se
> vieron completas en la captura original de esta clase, pero quedaron **confirmadas por
> comportamiento real**: con el servidor corriendo, `GET /openapi.json` devuelve
> `"title": "Users Service"`, `"version": "1.5.0"` (el valor del `.env`, sección 3) y la
> `description` exacta — solo son posibles si el código es tal cual se muestra arriba.

| Línea | Qué hace |
|---|---|
| `app = FastAPI(title=..., version=..., description=...)` | Estos 3 parámetros arman **Swagger/OpenAPI** automáticamente (visto en [Clase 3](Clase-03.md)) — `title`/`version` salen de `settings` (el `config.py` de este mismo servicio, sección 3), no están escritos a mano. |
| `@app.get("/health", tags=["Health"])` | Endpoint de **health check** — patrón típico de microservicios para que algo externo (Docker, un load balancer, Kubernetes) pregunte "¿seguís vivo?" sin tocar la lógica de negocio. |
| `"service": settings.app_name` | La respuesta identifica **cuál servicio** contestó — útil con varios microservicios detrás del mismo gateway. |
| `app.include_router(router, prefix="/api/v1")` | Engancha el `APIRouter` de `routers/*.py` a la app — sus endpoints quedan bajo `/api/v1/...` (el `prefix` del router, sección 5, se **suma** al `/api/v1` de acá). |

> 💡 Con esto, `GET /users/{user_id}` del router en realidad se sirve en
> `GET /api/v1/users/{user_id}` — dos `prefix` que se concatenan (uno en `main.py`, otro
> en el router).

## 🧪 7. Testing — `tests/test.py`

**[`users_service/tests/test.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/users_service/tests/test.py)**:
```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_user():
    response = client.post("/api/v1/users", json={
        "name": "Ana Torres",
        "email": "ana@empresa.com"
    })

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Ana Torres"
```

| Línea | Qué hace |
|---|---|
| `from fastapi.testclient import TestClient` | Importa `TestClient` (ver glosario) — **con mayúsculas exactas**, es una clase, no un módulo. |
| `client = TestClient(app)` | Envuelve la `app` real (la misma de `main.py`, sección 6) en un cliente que simula peticiones sin levantar un servidor. |
| `def test_health(): ...` | Cualquier función que empiece con `test_` es detectada automáticamente por `pytest` — no hace falta registrarla en ningún lado. |
| `assert response.status_code == 200` | `assert` corta la prueba (falla) si la condición es falsa — acá comprueba que `/health` responda `200`. |
| `client.post("/api/v1/users", json={...})` | Simula un `POST` con body JSON — mismo endpoint `create_user` de la sección 5, pero llamado en memoria en vez de por HTTP real. |

> ⚠️ Verificado corriendo `pytest` de verdad — la primera versión tenía 3 bugs reales:
> `testclient` en minúscula en el import (la clase es `TestClient`), un `=` en vez de
> `==` dentro de un `assert` (`SyntaxError`), y una coma faltante entre dos campos del
> `dict` del `POST` (`SyntaxError`). Ya corregidos arriba — con eso, los 2 tests pasan.

**[`products_service/tests/test.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/products_service/tests/test.py)** — mismo patrón, 4 tests (health, crear, el filtro del Ejercicio 1, y el `404`):
```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_product():
    response = client.post("/api/v1/products", json={
        "name": "Teclado mecánico",
        "price": 49.99,
        "stock": 10,
    })

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Teclado mecánico"


def test_list_products_filter_by_minimum_stock():
    client.post("/api/v1/products", json={
        "name": "Mouse",
        "price": 15.00,
        "stock": 5,
    })

    response = client.get("/api/v1/products", params={"minimum_stock": 10})

    assert response.status_code == 200
    for product in response.json():
        assert product["stock"] >= 10


def test_get_product_not_found():
    response = client.get("/api/v1/products/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"
```

| Test | Qué prueba |
|---|---|
| `test_health` | El endpoint de salud responde `200` con `"status": "ok"` (mismo patrón que `users_service`). |
| `test_create_product` | `POST` crea el producto y devuelve `201` con los datos correctos. |
| `test_list_products_filter_by_minimum_stock` | El filtro del **Ejercicio 1** funciona: crea un producto con `stock=5` y confirma que `?minimum_stock=10` lo deja afuera de la respuesta. |
| `test_get_product_not_found` | Un `id` inexistente responde `404` con el mensaje exacto `"Producto no encontrado"`. |

```
python3 -m pytest tests/test.py -v
tests/test.py::test_health PASSED
tests/test.py::test_create_product PASSED
tests/test.py::test_list_products_filter_by_minimum_stock PASSED
tests/test.py::test_get_product_not_found PASSED
4 passed in 0.19s
```

# 💻 PARTE PRÁCTICA

## 📦 Instalar dependencias

Cada microservicio tiene **su propio venv** — no se comparte con los demás servicios ni
con otros ejercicios del curso (mismo principio de la sección 2). Repetir esta secuencia
dentro de la carpeta de **cada** servicio:

```bash
cd <nombre_del_servicio>       # users_service o products_service
python3 -m venv venv
source venv/bin/activate
```

```bash
# users_service — necesita el extra [email] por el EmailStr de su schemas.py
pip install fastapi "uvicorn[standard]" "pydantic[email]" sqlalchemy pydantic-settings

# products_service — no usa EmailStr, no necesita el extra
pip install fastapi "uvicorn[standard]" pydantic sqlalchemy pydantic-settings
```

**Para testing** (sección 7 de la teoría), en cada servicio que tenga su `tests/test.py`:
```bash
pip install pytest httpx
```

> 📎 El historial completo paso a paso (en qué orden se instaló cada paquete durante la
> clase, y los tropiezos en el camino) queda en
> [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md#🧩-microservicios--un-venv-por-servicio-clase-6).
> Los `requirements.txt` de ambos servicios ya están congelados con `pip freeze`
> ([users_service](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/users_service/requirements.txt) ·
> [products_service](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/products_service/requirements.txt)).

## ▶️ Levantar los dos microservicios a la vez

Cada uno en **su propia terminal** (o pestaña), con **su propio venv** activado:

```bash
# Terminal 1 — users_service
cd users_service
source venv/bin/activate
python3 -m uvicorn app.main:app --reload --port 8001
```

```bash
# Terminal 2 — products_service
cd products_service
source venv/bin/activate
python3 -m uvicorn app.main:app --reload --port 8002
```

No se pisan porque cada uno lee su propio `port` desde su `app/config.py` (sección 3).
Documentación interactiva de cada uno en `http://127.0.0.1:8001/docs` y
`http://127.0.0.1:8002/docs`.

## ✅ Verificación — corrí ambos servicios de verdad

Con el venv real de cada servicio, confirmé que el código **funciona de punta a punta**
— encontré un bug, lo arreglé, y probé los endpoints de ambos con `curl`, incluidos los
dos corriendo **en simultáneo**.

**Endpoints — `users_service` (puerto 8001)**

| Prueba | Resultado |
|---|---|
| `GET /health` | `{"status":"ok","service":"Users Service"}` ✅ |
| `POST /api/v1/users` `{"name":"Styp Canto","email":"styp@example.com"}` | `201` → `{"name":"Styp Canto","email":"styp@example.com","id":1}` ✅ |
| `GET /api/v1/users` | `[{"name":"Styp Canto",...,"id":1}]` ✅ |
| `GET /api/v1/users/1` | Devuelve el usuario ✅ |
| `GET /api/v1/users/999` | `404` `{"detail":"Usuario no encontrado"}` ✅ |
| `POST /api/v1/users` con `name` de 1 letra | `422` `"String should have at least 3 characters"` ✅ (`Field(min_length=3)` funcionando) |

**Endpoints — `products_service` (puerto 8002)**

| Prueba | Resultado |
|---|---|
| `GET /health` | `{"status":"ok","service":"Products Service"}` ✅ |
| `POST /api/v1/products` `{"name":"Teclado mecánico","price":49.99,"stock":10}` | `201` → `{"name":"Teclado mecánico","price":"49.99","stock":10,"id":1}` ✅ |
| `GET /api/v1/products` | Lista con el producto creado ✅ |
| `GET /api/v1/products/1` | Devuelve el producto ✅ |
| `GET /api/v1/products/999` | `404` `{"detail":"Producto no encontrado"}` ✅ |
| `POST /api/v1/products` con `price: 0` | `422` `"Input should be greater than 0"` ✅ (`Field(gt=0)` funcionando) |

> 💡 `price` vuelve como **string** (`"49.99"`) en el JSON, no como número — es el
> comportamiento normal de `Decimal` en Pydantic al serializar a JSON (JSON no tiene un
> tipo decimal exacto; devolverlo como string evita perder precisión). El cliente que
> consuma esta API debe parsearlo como decimal, no asumir que es un `float` de JS.

**Los dos servicios corriendo a la vez, en simultáneo (confirmado):**
```bash
curl http://127.0.0.1:8001/health
# {"status":"ok","service":"Users Service"}

curl http://127.0.0.1:8002/health
# {"status":"ok","service":"Products Service"}
```

> ✅ **Confirmado por Styp:** con esto, el proyecto de la Clase 6 corre completo — los dos
> microservicios levantan y responden sin errores.

## ✅ Correr los tests

```bash
cd users_service
source venv/bin/activate
python3 -m pytest tests/test.py -v
```

```
tests/test.py::test_health PASSED
tests/test.py::test_create_user PASSED
2 passed in 0.19s
```

> ⚠️ **Usa `python3 -m pytest`, no `pytest` a secas** — mismo motivo que
> `python3 -m uvicorn` (sección de arriba): `pytest` solo no agrega la carpeta actual
> (`users_service/`) al `sys.path`, así que `from app.main import app` falla con
> `ModuleNotFoundError: No module named 'app'`. Con `-m`, Python sí agrega el directorio
> actual antes de correrlo.

Mismo comando en `products_service` (cada uno con su propio venv, sección de dependencias):
```bash
cd products_service
source venv/bin/activate
python3 -m pytest tests/test.py -v
```
```
tests/test.py::test_health PASSED
tests/test.py::test_create_product PASSED
tests/test.py::test_list_products_filter_by_minimum_stock PASSED
tests/test.py::test_get_product_not_found PASSED
4 passed in 0.19s
```

### 🐞 Errores que aparecieron en el camino

Todos reproducidos y solucionados. Detalle completo en cada link:

| Error | Causa | Detalle |
|---|---|---|
| `parse error near ')'` al poner `source python3 -m venv venv` | `source` mezclado con el comando de **crear** el venv — `source` es solo para **activar** | [ver](../06-Errores/2026-08-20-source-antes-de-python3-venv.md) |
| `zsh: command not found: venvScriptsactivate` (y variantes) | Ruta de **Windows** (`venv\Scripts\activate`) en una terminal macOS/Linux — la correcta es `venv/bin/activate` | [ver](../06-Errores/2026-08-14-activate-sin-source-no-funciona.md#🔁-recurrió-en-clase-6-2026-08-20) |
| `zsh: command not found: uvicorn[standard]` | Faltaba `pip install` adelante — `"uvicorn[standard]"` solo no es un comando, es un argumento | [ver](../06-Errores/2026-08-20-falta-pip-install-uvicorn-standard.md) |
| `No module named uvicorn` al correr `python3 -m uvicorn ...` | El venv no estaba activado en esa terminal — `python3` cae al del sistema, que no tiene `uvicorn` instalado | [ver](../06-Errores/2026-08-11-pip-command-not-found-venv-inactivo.md#🔁-recurrió-en-clase-6-2026-08-20--mismo-root-cause-síntoma-distinto) |
| `ImportError: email-validator is not installed` al importar `users_service` | `schemas.py` usa `EmailStr`, que necesita el extra `pydantic[email]` aparte | [ver](../06-Errores/2026-08-20-importerror-email-validator.md) |
| `ModuleNotFoundError: No module named 'app'` al correr `pytest tests/test.py` | `pytest` a secas no agrega la carpeta actual al `sys.path` — usar `python3 -m pytest` | [ver](../06-Errores/2026-08-20-modulenotfounderror-app-pytest-sin-m.md) |

# 🏋️ EJERCICIOS CON SOLUCIÓN
10 ejercicios, en orden gradual básico → completo. Todos verificados en terminal
(`TestClient`/`curl`, algunos con los dos microservicios corriendo de verdad).

### Ejercicio 1 — Filtrar productos por stock mínimo (ejercicio real de la Clase 6)

Amplía el endpoint `GET /products` de `products_service` para que acepte un parámetro
**opcional** en la URL: `?minimum_stock=10`. Cuando se manda, la respuesta debe traer
**solo** los productos cuyo `stock` sea mayor o igual a ese número. Cuando **no** se
manda el parámetro, el endpoint debe seguir funcionando exactamente igual que antes
(todos los productos, sin filtrar).

Salida esperada, con 3 productos ya creados (`stock` 5, 10 y 20):
```bash
curl "http://127.0.0.1:8002/api/v1/products"
# → los 3 productos

curl "http://127.0.0.1:8002/api/v1/products?minimum_stock=10"
# → solo los 2 con stock >= 10

curl "http://127.0.0.1:8002/api/v1/products?minimum_stock=100"
# → []  (ninguno llega a ese stock)
```

<details><summary>💡 ¿Sabías que…? — query params opcionales + list comprehension</summary>

En FastAPI, cualquier parámetro de una función-endpoint que **no** aparezca entre `{}`
en la ruta del decorador (`@router.get("/{algo}")`) se convierte automáticamente en
**query param** — no hace falta ningún decorador ni import especial para eso. Dándole
un valor por defecto (`= None`) lo volvés opcional: si no viene en la URL, el parámetro
simplemente vale `None` adentro de la función.

Para filtrar una lista de diccionarios según una condición, ya usaste el patrón
`for` + `if` en `get_product` (sección 5 de la teoría). Una **list comprehension** es
la misma idea, escrita en una sola línea — arma una lista nueva recorriendo la
original y quedándose solo con lo que cumple la condición:

```python
# Ejemplo de referencia — mismo patrón, otro dominio (no es la solución)
def filtrar_ordenes(ordenes, monto_minimo=None):
    if monto_minimo is None:
        return ordenes

    return [
        orden
        for orden in ordenes
        if orden["monto"] >= monto_minimo
    ]

ordenes = [{"id": 1, "monto": 30}, {"id": 2, "monto": 80}, {"id": 3, "monto": 150}]
print(filtrar_ordenes(ordenes, monto_minimo=80))
# → [{'id': 2, 'monto': 80}, {'id': 3, 'monto': 150}]
```
</details>

<details><summary>Ver solución</summary>

```python
@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products(
    minimum_stock: int | None = None,
):
    if minimum_stock is None:
        return products

    return [
        product
        for product in products
        if product["stock"] >= minimum_stock
    ]
```

Verificado con `curl` real, creando 3 productos con `stock` 5, 10 y 20:
```bash
curl "http://127.0.0.1:8002/api/v1/products?minimum_stock=10"
# [{"name":"Teclado","price":"49.99","stock":10,"id":2},
#  {"name":"Monitor","price":"199.99","stock":20,"id":3}]
```

Archivo real: [`products_service/app/routers/products.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-06/project/products_service/app/routers/products.py)
</details>

### Ejercicio 2 — Buscar un usuario por email

En `users_service`, agrega un endpoint `GET /users/search?email=...` que devuelva el
usuario con ese email exacto, o `404` si no existe ninguno.

Salida esperada:
```bash
curl "http://127.0.0.1:8001/api/v1/users/search?email=ana@empresa.com"
# → {"name": "Ana Torres", "email": "ana@empresa.com", "id": 1}
```

<details><summary>💡 ¿Sabías que…? — un `for` + `if` que ya usaste, con otro campo</summary>

Ya escribiste este patrón en `get_user` (sección 5), buscando por `id`. Buscar por
`email` es exactamente lo mismo, cambiando qué campo comparás:

```python
# Ejemplo de referencia — buscar un libro por isbn (no es la solución)
def buscar_libro_por_isbn(libros, isbn):
    for libro in libros:
        if libro["isbn"] == isbn:
            return libro
    return None
```

> ⚠️ Ojo con el **orden de las rutas**: `/users/search` tiene que quedar declarada
> **antes** que `/users/{user_id}` en el archivo. Si no, FastAPI intentaría interpretar
> `"search"` como si fuera un `user_id`, y como no es un número, la petición fallaría con
> `422` en vez de llegar a tu función.
</details>

<details><summary>Ver solución</summary>

```python
@router.get("/search", response_model=UserResponse)
def search_user_by_email(email: str):
    for user in users:
        if user["email"] == email:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado",
    )
```
Verificado con `TestClient`: `GET /api/v1/users/search?email=ana@empresa.com` → `200`
con el usuario correcto.
</details>

### Ejercicio 3 — Eliminar un producto (`DELETE`)

Agrega a `products_service` un endpoint `DELETE /products/{product_id}` que borre el
producto de la lista y devuelva `204 No Content` (sin body). Si el `product_id` no
existe, debe responder `404`, igual que `get_product`.

Salida esperada:
```bash
curl -X DELETE -w "\nHTTP:%{http_code}\n" http://127.0.0.1:8002/api/v1/products/1
# → HTTP:204 (sin body)

curl http://127.0.0.1:8002/api/v1/products/1
# → 404 {"detail": "Producto no encontrado"}
```

<details><summary>💡 ¿Sabías que…? — `list.remove()` + el código 204</summary>

`status.HTTP_204_NO_CONTENT` le dice a FastAPI "esta respuesta no lleva body" — por eso
la función no necesita `return` con nada (o hace `return` vacío). Para borrar un
elemento de una lista de diccionarios, buscás el que cumple la condición y lo sacás con
`list.remove(...)`:

```python
# Ejemplo de referencia — borrar una tarea de una lista (no es la solución)
def borrar_tarea(tareas, tarea_id):
    for t in tareas:
        if t["id"] == tarea_id:
            tareas.remove(t)
            return True
    return False
```
</details>

<details><summary>Ver solución</summary>

```python
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado",
    )
```
Verificado con `TestClient`: `DELETE` responde `204`, y un `GET` posterior al mismo id
responde `404`.
</details>

### Ejercicio 4 — Actualizar el nombre de un usuario (`PATCH`)

Agrega `PATCH /users/{user_id}` a `users_service`, que reciba `{"name": "..."}` y
actualice solo ese campo del usuario (el `email` no cambia). `404` si no existe.

Salida esperada:
```bash
curl -X PATCH http://127.0.0.1:8001/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana María Torres"}'
# → {"name": "Ana María Torres", "email": "ana@empresa.com", "id": 1}
```

<details><summary>💡 ¿Sabías que…? — un esquema Pydantic más chico, solo para el update</summary>

No reutilices `UserCreate` para el `PATCH` — pide `email` también, y este endpoint no
lo necesita. Convine crear un esquema **nuevo, más chico**, con solo el campo que se
puede actualizar:

```python
# Ejemplo de referencia — actualizar el puesto de un empleado (no es la solución)
class EmpleadoUpdate(BaseModel):
    puesto: str

def actualizar_puesto(empleados, emp_id, nuevo_puesto):
    for e in empleados:
        if e["id"] == emp_id:
            e["puesto"] = nuevo_puesto
            return e
    return None
```
</details>

<details><summary>Ver solución</summary>

```python
class UserUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=100)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate):
    for user in users:
        if user["id"] == user_id:
            user["name"] = data.name
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado",
    )
```
Verificado con `TestClient`: el `PATCH` cambia solo `name`, el `email` queda intacto.
</details>

### Ejercicio 5 — Evitar emails duplicados al crear un usuario

Modifica `create_user` para que, **antes** de agregar el nuevo usuario, revise si ya
existe alguno con el mismo `email`. Si ya existe, responde `409 Conflict` en vez de
crearlo.

Salida esperada:
```bash
curl -X POST http://127.0.0.1:8001/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Otra Ana", "email": "ana@empresa.com"}'
# → HTTP 409  {"detail": "El email ya está registrado"}
```

<details><summary>💡 ¿Sabías que…? — una validación de negocio no va en `Field(...)`</summary>

`Field(...)` (sección 4) valida **la forma** de un campo (longitud, formato) sin mirar
los demás datos que ya existen. Que un email no se repita es una **regla de negocio**
que depende de comparar contra los datos guardados — eso se valida **adentro de la
función del endpoint**, con un `for` que recorre lo que ya existe, antes de crear:

```python
# Ejemplo de referencia — no repetir código de curso (no es la solución)
def crear_curso(cursos, codigo):
    for c in cursos:
        if c["codigo"] == codigo:
            raise ValueError("Ya existe un curso con ese código")
    nuevo = {"id": len(cursos) + 1, "codigo": codigo}
    cursos.append(nuevo)
    return nuevo
```
</details>

<details><summary>Ver solución</summary>

```python
def create_user(data: UserCreate):
    for user in users:
        if user["email"] == data.email:
            raise HTTPException(
                status_code=409,
                detail="El email ya está registrado",
            )

    user = {
        "id": len(users) + 1,
        **data.model_dump(),
    }
    users.append(user)
    return user
```
Verificado con `TestClient`: crear dos usuarios con el mismo email → el segundo da `409`.
</details>

### Ejercicio 6 — Paginación en `GET /users`

Agrega dos query params opcionales a `list_users`: `skip` (cuántos saltarse, default
`0`) y `limit` (cuántos devolver como máximo, default `10`).

Salida esperada, con 8 usuarios cargados:
```bash
curl "http://127.0.0.1:8001/api/v1/users?skip=5&limit=3"
# → los usuarios 6º, 7º y 8º (3 en total)
```

<details><summary>💡 ¿Sabías que…? — el slicing de listas de Python hace todo el trabajo</summary>

`lista[inicio:fin]` es *slicing*, mecánica base de Python — `lista[5:8]` devuelve del
índice 5 al 7. Para paginar no hace falta un `for` manual, alcanza con calcular bien los
dos números del slice a partir de `skip`/`limit`:

```python
# Ejemplo de referencia — paginar una lista de canciones (no es la solución)
def paginar(items, skip=0, limit=5):
    return items[skip : skip + limit]
```
</details>

<details><summary>Ver solución</summary>

```python
@router.get("", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10):
    return users[skip : skip + limit]
```
Verificado con `TestClient`: con 8 usuarios cargados, `?skip=0&limit=3` devuelve
exactamente 3.
</details>

### Ejercicio 7 — Arreglar el bug del `id` autoincremental

`create_product`/`create_user` usan `len(lista) + 1` para el `id` — ya se marcó como
⚠️ ingenuo en la sección 5: si se borra un elemento del medio (Ejercicio 3), el próximo
alta puede calcular un `id` que **ya existe**. Arréglalo para que sea seguro incluso
después de borrar.

Situación para probar: crear 2 productos (quedan `id` 1 y 2), borrar el `id` 1, crear
uno nuevo. Con el bug, el nuevo producto **repetiría** el `id` 1 (choca con el borrado,
pero convive raro con el 2 restante). Arreglado, el nuevo debe tener `id` 3.

<details><summary>💡 ¿Sabías que…? — `max()` con un generador, y el argumento `default`</summary>

En vez de contar cuántos elementos *hay* (`len`), hay que mirar cuál es el **id más
alto que existió** y sumarle 1 — así nunca se repite aunque se haya borrado algo del
medio. `max()` con una expresión generadora (`r["id"] for r in lista`) recorre y se
queda con el mayor; el argumento `default=0` evita un error si la lista está vacía:

```python
# Ejemplo de referencia — ids de reservas, sin chocar tras un borrado (no es la solución)
reservas = [{"id": 1}, {"id": 3}]  # el id 2 se borró en algún momento
siguiente_id = max((r["id"] for r in reservas), default=0) + 1  # -> 4, no 3
```
</details>

<details><summary>Ver solución</summary>

```python
def create_product(data: ProductCreate):
    next_id = max((p["id"] for p in products), default=0) + 1

    product = {
        "id": next_id,
        **data.model_dump(),
    }
    products.append(product)
    return product
```
Verificado con `TestClient`: crear 2, borrar el `id` 1, crear otro → el nuevo sale con
`id` **3** (no repite el 1 ni choca con el 2 que sigue existiendo). Mismo cambio aplica
igual en `create_user`.
</details>

### Ejercicio 8 — Sumar `debug` a la configuración y usarlo en `main.py`

Agrega un campo `debug: bool = False` a la clase `Settings` (sección 3). Si
`DEBUG=true` en el `.env`, `main.py` debe **ocultar** la documentación Swagger
(`docs_url=None`) — simulando que en producción no se expone `/docs`.

<details><summary>💡 ¿Sabías que…? — `pydantic-settings` convierte texto a `bool` solo</summary>

Un `.env` es siempre **texto plano** (`DEBUG=true`), pero como el campo está tipado
`bool`, `BaseSettings` lo convierte automáticamente a `True`/`False` de Python — no hay
que parsear el string a mano. Mismo mecanismo que ya viste con `port: int` (sección 3),
aplicado a otro tipo:

```python
# Ejemplo de referencia — flag de mantenimiento (no es la solución)
class Settings(BaseSettings):
    maintenance_mode: bool = False
    model_config = SettingsConfigDict(env_file=".env")
# .env con "MAINTENANCE_MODE=true" -> settings.maintenance_mode es True (bool), no "true" (str)
```
</details>

<details><summary>Ver solución</summary>

```python
# config.py
class Settings(BaseSettings):
    app_name: str = "Users Service"
    app_version: str = "1.0.0"
    port: int = 8001
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
```
```python
# main.py
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
)
```
Verificado: con `.env` conteniendo `DEBUG=true`, `settings.debug` sale `True` (tipo
`bool`, no el string `"true"`).
</details>

### Ejercicio 9 — Filtrar productos por rango de precio

Extiende `list_products` (ya tiene `minimum_stock` del Ejercicio 1) para aceptar además
`price_min` y `price_max`, opcionales, combinables entre sí y con `minimum_stock`.

Salida esperada:
```bash
curl "http://127.0.0.1:8002/api/v1/products?price_min=40&price_max=200"
# → solo los productos con 40 <= price <= 200
```

<details><summary>💡 ¿Sabías que…? — encadenar filtros reasignando la misma variable</summary>

Con **un** filtro alcanza una list comprehension (Ejercicio 1). Con **varios**
opcionales y combinables, es más simple ir filtrando la variable de a uno, aplicando
solo los filtros que realmente vinieron en la URL:

```python
# Ejemplo de referencia — filtrar pedidos por rango de monto (no es la solución)
def filtrar_por_rango(pedidos, monto_min=None, monto_max=None):
    resultado = pedidos
    if monto_min is not None:
        resultado = [p for p in resultado if p["monto"] >= monto_min]
    if monto_max is not None:
        resultado = [p for p in resultado if p["monto"] <= monto_max]
    return resultado
```
</details>

<details><summary>Ver solución</summary>

```python
def list_products(
    minimum_stock: int | None = None,
    price_min: Decimal | None = None,
    price_max: Decimal | None = None,
):
    result = products

    if minimum_stock is not None:
        result = [p for p in result if p["stock"] >= minimum_stock]
    if price_min is not None:
        result = [p for p in result if p["price"] >= price_min]
    if price_max is not None:
        result = [p for p in result if p["price"] <= price_max]

    return result
```
Verificado con `TestClient`: con productos de precio 15, 49.99 y 199.99,
`?price_min=40&price_max=200` devuelve solo el de 199.99.
</details>

### Ejercicio 10 — (avanzado) `products_service` valida un usuario en `users_service` por HTTP

El más completo: conecta los dos microservicios de verdad. Agrega un campo `owner_id`
a `ProductCreate`. En `create_product`, **antes** de crear el producto, `products_service`
debe llamar por HTTP a la API de `users_service` (`GET /api/v1/users/{owner_id}`) para
confirmar que ese usuario existe. Si `users_service` responde `404`, `products_service`
debe rechazar la creación con `400`.

Salida esperada (con `users_service` en 8001 y `products_service` en 8002, ambos
corriendo):
```bash
curl -X POST http://127.0.0.1:8002/api/v1/products \
  -d '{"name": "Mouse", "owner_id": 1}'         # 1 existe en users_service → 201

curl -X POST http://127.0.0.1:8002/api/v1/products \
  -d '{"name": "Mouse2", "owner_id": 999}'      # 999 no existe → 400
```

<details><summary>💡 ¿Sabías que…? — esto es "no conocer el modelo interno del otro servicio", en código</summary>

Es la aplicación práctica de la sección 2 ("¿`products_service` debe conocer el modelo
interno de `users_service`?" → no). `products_service` **no** importa nada de
`users_service` ni lee su lista en memoria — solo le hace una petición HTTP a su API
pública, con `httpx` (ya instalado, sección 7), y reacciona según el código de estado
que reciba:

```python
# Ejemplo de referencia — validar que existe una sucursal antes de crear un pedido
import httpx

SUCURSALES_URL = "http://127.0.0.1:9001"

def crear_pedido(sucursal_id: int):
    respuesta = httpx.get(f"{SUCURSALES_URL}/api/v1/sucursales/{sucursal_id}")
    if respuesta.status_code == 404:
        raise ValueError("La sucursal no existe")
    # ... recién acá se crea el pedido
```
</details>

<details><summary>Ver solución</summary>

```python
# products_service/app/schemas.py — sumar el campo
class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    price: Decimal = Field(gt=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    owner_id: int
```
```python
# products_service/app/routers/products.py
import httpx

USERS_SERVICE_URL = "http://127.0.0.1:8001"

def create_product(data: ProductCreate):
    response = httpx.get(f"{USERS_SERVICE_URL}/api/v1/users/{data.owner_id}")

    if response.status_code == 404:
        raise HTTPException(
            status_code=400,
            detail=f"El usuario {data.owner_id} no existe en users_service",
        )

    product = {
        "id": max((p["id"] for p in products), default=0) + 1,
        **data.model_dump(),
    }
    products.append(product)
    return product
```
**Verificado con los dos servicios corriendo de verdad** (puertos 18001/18002 en la
prueba): `owner_id=1` (existe) → `201`; `owner_id=999` (no existe) → `400` con el
mensaje correcto.

> ⚠️ Esta llamada es **síncrona y bloqueante** — mientras `products_service` espera la
> respuesta de `users_service`, esa petición queda parada. Si `users_service` está
> caído o tarda, `create_product` tarda o falla también. Este acoplamiento en tiempo de
> ejecución (distinto del acoplamiento de datos de la sección 2) es exactamente el tipo
> de problema que resuelve el **API Gateway** y los patrones de comunicación de la
> [Clase 7](Clase-07.md).
</details>

## ❓ Preguntas y respuestas (autoevaluación)

**1. ¿Qué hace `EmailStr` en un esquema Pydantic, y qué necesita para funcionar?**
> Valida que el valor tenga formato de correo (`algo@dominio.com`); rechaza el dato
> antes de que llegue al endpoint si no cumple el formato. Necesita el extra
> `email-validator` instalado aparte de Pydantic (`pip install "pydantic[email]"`) — sin
> eso, tira `ImportError` al importar el esquema.

**2. ¿Por qué `UserResponse` hereda de `UserCreate` en vez de repetir sus campos?**
> Para no duplicar `name`/`email` en dos clases — `UserResponse(UserCreate)` hereda esos
> dos campos y solo suma lo que le falta (`id: int`). Mismo mecanismo de herencia de
> clases de Python, aplicado a modelos Pydantic.

**3. ¿Por qué cada microservicio tiene su propio `config.py` en vez de compartir uno solo?**
> Porque cada uno es un proceso independiente con su propio puerto, su propio nombre y su
> propia versión — un archivo compartido no podría tener valores distintos para cada
> servicio a la vez. Es el mismo patrón repetido en cada carpeta, no un archivo único.

**4. Editaste el `.env` con el servidor ya corriendo. ¿El cambio se aplica al instante?**
> No. `Settings()` se crea **una sola vez**, cuando arranca el proceso (al importar
> `config.py`). Un cambio en el `.env` recién se refleja si **reiniciás** el servidor —
> `--reload` vigila cambios en el código Python, no en el `.env`.

**5. ¿Pueden dos microservicios usar la misma tecnología (mismo lenguaje, mismo framework)?**
> Sí, sin problema — de hecho es lo que hacen `users_service` y `products_service` en
> esta clase (los dos en Python/FastAPI). La ventaja de los microservicios no es que
> *tengan* que usar tecnologías distintas, es que *pueden*, si algún día hace falta.

**6. ¿Pueden dos microservicios usar el mismo puerto al mismo tiempo, en la misma máquina?**
> No — un puerto TCP solo admite un proceso escuchando a la vez. Si dos intentan usar el
> mismo, el segundo que arranque falla con `address already in use`. Por eso
> `users_service` usa 8001 y `products_service` usa 8002.

**7. ¿`products_service` debería importar los esquemas o leer la lista `users` interna de `users_service`?**
> No — un servicio no debería conocer más de otro que su **contrato público** (su API).
> Si necesita un dato de usuario, lo pide por HTTP (`GET /api/v1/users/{id}`), nunca
> accediendo a su modelo o sus datos internos directamente.

**8. ¿Todos los microservicios de un proyecto tienen que compartir la misma versión?**
> No — cada uno se versiona por su cuenta. En este proyecto, `users_service` quedó en
> `1.5.0` (por su `.env`) mientras `products_service` sigue en `1.0.0`, al mismo tiempo,
> sin conflicto.

**9. Estás por agregar una regla de negocio nueva sobre productos (por ejemplo, un descuento máximo). ¿En qué microservicio va?**
> En `products_service` — es su Bounded Context. La regla es del dueño del **dato**
> (`price`, en este caso), sin importar qué otro servicio la vaya a usar más adelante.

**10. ¿Por qué a veces hay que correr `python3 -m uvicorn ...` / `python3 -m pytest ...` en vez de `uvicorn ...` / `pytest ...` a secas?**
> Porque el comando suelto puede resolver a un Python o una instalación **distinta** de
> la esperada (el del sistema en vez del venv) o no agregar la carpeta actual al
> `sys.path` — con `-m`, se le pide explícitamente a **ese `python3` puntual** que corra
> el módulo, evitando ambos problemas.

## 📎 Apuntes relacionados
- [Clase 4](Clase-04.md) — `Field(...)`, `BaseSettings`/`SettingsConfigDict`, SQLAlchemy (contraste con la lista en memoria de esta clase)
- [Clase 5](Clase-05.md) — Database per Service, arquitectura de microservicios
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md) — historial completo de comandos de esta clase (venv, `pip install`, levantar el servidor)
- `06-Errores/` — los 5 errores de esta clase, listados en la tabla de arriba

## ➡️ Siguiente
[Clase 7](Clase-07.md) — Comunicación y seguridad en microservicios (API Gateway, JWT) —
tema natural después de tener `users_service` y `products_service` corriendo por separado.
