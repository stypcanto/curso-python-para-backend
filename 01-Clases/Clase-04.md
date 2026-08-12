---
sidebar: "Clase 4 · Integración Base de Datos"
---

# 📙 Clase 4 — Integración a base de datos y arquitectura de persistencia de datos

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
- *(profundización propia)* Probar los endpoints con Postman/Bruno en vez de solo Swagger

# 📖 PARTE TEÓRICA

## 📚 1. Definiciones clave

Antes de entrar capa por capa, un **glosario** de los términos que se usan a lo largo de
esta clase, agrupados por tema. Cada fila enlaza a la sección donde ese concepto se ve
en profundidad (código real, diagramas, verificado en terminal) — acá va solo la
definición corta, para no repetirla cada vez que aparece.

### 🐍 Mecánica de Python: `import` y `nombre: tipo = valor`

Estas dos construcciones aparecen en **todos** los archivos de esta clase — conviene
tenerlas claras antes de leer cualquier código de acá en adelante.

**El `import`** — `from pydantic import BaseModel, ConfigDict, Field` se lee "de la
librería `pydantic`, traé estas 3 piezas". Después de esa línea, esos 3 nombres quedan
disponibles para usar en el resto del archivo, como si estuvieran escritos ahí mismo. Es
el mismo patrón `from módulo import función` de la Clase 1
(`from request_utils import calculate_response_time`) — la única diferencia es de dónde
viene lo importado: `pydantic`/`sqlalchemy`/`alembic` son **librerías instaladas**
(`pip install ...`), mientras que `models.ticket` o `core.config` son **archivos propios
del proyecto**. La sintaxis del `import` es la misma en los dos casos.

**Declarar una variable/campo con tipo** — `title: str = Field(min_length=5,
max_length=120)` tiene 3 partes:
```
   title    :   str    =   Field(min_length=5, max_length=120)
   ↑            ↑           ↑
   nombre       tipo        valor asignado — acá no es un dato fijo
   del campo    (type       como "Media", sino el RESULTADO de llamar
                 hint)      a la función Field(...), que devuelve un
                            objeto con las reglas de validación
```
Es la misma sintaxis `nombre: tipo = valor` que ya se usó en funciones tipadas (Clase 1,
`estimated_hours: float`) y en `dataclass` (Clase 2). Reaparece con otra cara en
`id: Mapped[int] = mapped_column(primary_key=True)` (sección 9) — mismas 3 partes,
distinta función del lado derecho.

**`Generator` y `yield`** — `def get_db() -> Generator[Session, None, None]:` con
`yield db` adentro es una **función generadora**: en vez de terminar y devolver un
único valor (`return`), *pausa* en el `yield`, entrega ese valor a quien la llamó, y
quien la llamó decide cuándo "reanudarla" (acá lo hace FastAPI, al terminar la
petición). Es lo que permite que `get_db()` abra la sesión, la "preste" mientras dura
la petición, y recién después siga ejecutando el `finally` que la cierra — ver sección
9. `Generator` (de `collections.abc`) es solo el *type hint* que describe esa forma.

### 🐳 Herramientas externas (no son librerías de Python)

| Término | Qué es | Se profundiza en |
|---|---|---|
| **Docker** | Herramienta para correr programas dentro de **contenedores**: un entorno aislado y reproducible que empaqueta la app (acá, Postgres) con todo lo que necesita para funcionar, sin instalarla directo en el sistema operativo. | sección 6 |
| **Contenedor** | Una instancia en ejecución de una **imagen** de Docker (`postgres:16-alpine`) — como una mini-máquina virtual liviana, aislada del resto del Mac. | sección 6 |
| **Driver (`psycopg2-binary`)** | El traductor de bajo nivel que sabe hablar el protocolo real de Postgres — SQLAlchemy es agnóstico al motor, pero necesita un driver específico por cada uno (`psycopg2` para Postgres, `pymysql` para MySQL...). | sección 7 |
| **Postman / Bruno** | Clientes API: guardan peticiones HTTP en **colecciones** reutilizables (con variables como `{{base_url}}`) para probar una API sin escribir `curl` cada vez. Bruno es la alternativa *open source* que guarda la colección como archivos de texto versionables en git. | sección 15 |

### 🏛️ Persistencia y arquitectura

| Término | Qué es | Se profundiza en |
|---|---|---|
| **Persistencia de datos** | Capacidad de un dato de sobrevivir a la ejecución del programa que lo creó — que siga existiendo después de cerrar la terminal o reiniciar el servidor. | sección 2 |
| **ACID / Transacción** | Las 4 garantías que da una base de datos relacional sobre cada operación: Atomicidad, Consistencia, Isolamiento, Durabilidad. | sección 2 |
| **ORM** (*Object-Relational Mapping*) | La capa que traduce información entre dos mundos que hablan distinto: clases/objetos de Python ↔ tablas/filas de la base de datos. | sección 3 |
| **Capa de servicios** | La capa que aplica las reglas de negocio (qué hacer, en qué orden) — no sabe nada de HTTP ni de SQL. | sección 11 |
| **Repository Pattern** | Patrón de diseño que separa la lógica de acceso a datos (leer/guardar) del resto de la app, detrás de una interfaz simple (`get_all`, `create`, ...). | sección 10 |
| **Inyección de dependencias** | En vez de que una clase/función cree lo que necesita, se lo pasan de afuera (`repository: TicketRepository` en el `__init__`) — facilita testear con versiones falsas (*mocks*). | secciones 10 y 12 |
| **Migración (de esquema)** | Un cambio versionado a la estructura de la base de datos (crear una tabla, agregar una columna) — se aplica y se puede revertir, como un commit de git. | sección 14 |

### 🗄️ SQLAlchemy (ORM)

| Término | Qué es | Se profundiza en |
|---|---|---|
| **`engine`** | El objeto de SQLAlchemy que representa la conexión "física" a Postgres — sabe *cómo* hablarle a la base (usuario, password, host, puerto), pero no ejecuta consultas por sí solo. | sección 9 |
| **`Session` / `SessionLocal`** | La "conversación" activa con la base de datos — por ella pasan todas las consultas, inserciones y `commit()`. Se abre una por petición (`get_db()`) y se cierra al terminar. | sección 9 |
| **`pool_pre_ping`** | Antes de reusar una conexión reciclada del *pool*, SQLAlchemy le manda un ping para confirmar que sigue viva — evita fallar con una conexión muerta. | sección 9 |
| **`Base` / `DeclarativeBase`** | La clase de la que heredan todos los modelos (`class User(Base)`) — es lo que conecta una clase Python con una tabla real. | sección 9 |
| **`Mapped[...]` / `mapped_column(...)`** | Sintaxis moderna (SQLAlchemy 2.0) para declarar una columna: `Mapped[int]` es el tipo, `mapped_column(...)` las reglas (`primary_key`, `nullable`, etc.) — mismo patrón `nombre: tipo = valor` de arriba. | sección 9 |
| **`relationship(...)` / `back_populates`** | Comodidad de Python para navegar una relación como atributo (`ticket.requester.name`) en vez de escribir el `JOIN` a mano; `back_populates` conecta las dos puntas de esa relación. | sección 9 |
| **`ForeignKey(...)`** | Le dice a Postgres que una columna solo puede tener un valor que exista en otra tabla — la FK real, a nivel de base de datos. | sección 9 |
| **`statement` (`select(...)`)** | Un objeto Python que *describe* una consulta sin ejecutarla todavía (evaluación diferida/*lazy*) — recién se convierte en SQL real cuando una `Session` lo ejecuta. | sección 10 |
| **Dialecto (*dialect*)** | El "traductor" específico de un motor (`postgresql`, `mysql`, `sqlite`...) que SQLAlchemy usa para compilar un `statement` al SQL real de ese motor. | sección 4 |
| **`TYPE_CHECKING`** | Bloque que solo se ejecuta para el editor/type-checker, nunca en tiempo real — evita imports circulares entre modelos que se referencian entre sí. | sección 9 |

### ✅ Pydantic (validación)

| Término | Qué es | Se profundiza en |
|---|---|---|
| **Pydantic** | La librería de Python que valida datos a partir de type hints: declarás la forma que *debería* tener un dato y ella revisa que lo que llega cumpla esa forma (o avisa el error, como el `422` de la [Clase 3](Clase-03.md)). | sección 8 |
| **`BaseModel`** | La clase base de Pydantic. Toda clase que **hereda** de ella (herencia, [Clase 2](Clase-02.md)) se convierte en un "molde validado". | sección 8 |
| **`Field(...)`** | Función de Pydantic para sumarle reglas extra a **un campo puntual** (mínimo/máximo de caracteres, valor por defecto, mayor a 0...). | sección 8 |
| **`ConfigDict`** | Configuración **general de todo el modelo** (no de un campo) — por ejemplo, que acepte leer datos directo de un objeto ORM (`from_attributes=True`). | sección 8 |
| **`str`** | Tipo básico de Python ([Clase 1](Clase-01.md)) — texto. Como *type hint* le dice a Pydantic "este campo tiene que ser texto". | Clase 1 |
| **`pydantic-settings` / `BaseSettings`** | Paquete aparte de Pydantic pensado para configuración: lee variables desde un archivo `.env` y las valida igual que un `BaseModel` normal. | sección 9 |

### 🐘 Alembic (migraciones)

| Término | Qué es | Se profundiza en |
|---|---|---|
| **Alembic** | "git, pero para el esquema de la base de datos" — cada cambio de estructura queda guardado como un archivo de migración encadenado al anterior. | sección 14 |
| **`target_metadata` / `Base.metadata`** | El catálogo en memoria de lo que el esquema *debería* ser, según los modelos Python ya importados — lo que Alembic compara contra la base real. | sección 14 |
| **`alembic revision --autogenerate`** | Compara `target_metadata` contra la base real y **escribe** (en Python, no en SQL) el archivo de migración con la diferencia. | sección 14 |
| **`alembic upgrade head` / `downgrade`** | Aplica (o revierte) las migraciones pendientes contra la base real — acá es donde el SQL de verdad se ejecuta. | sección 14 |
| **`alembic_version`** | Tabla que crea el propio Alembic (no un modelo del proyecto) — guarda el id de la última migración aplicada. | sección 14 |

### 🌐 FastAPI (capa API)

*(ya se vio en profundidad en la [Clase 3](Clase-03.md) — acá solo referencia rápida)*

| Término | Qué es | Se profundiza en |
|---|---|---|
| **`APIRouter`** | Agrupa un conjunto de endpoints relacionados (acá, todos los de `/tickets`) para incluirlos en la app con `app.include_router(...)`. | sección 12 |
| **`Depends(...)`** | Le dice a FastAPI que resuelva algo **antes** de correr el endpoint (abrir una sesión de BD, armar un servicio) — inyección de dependencias a nivel de framework. | sección 12 |
| **`response_model`** | El schema Pydantic que define la forma de lo que devuelve un endpoint — FastAPI convierte el resultado real a esa forma. | Clase 3 / sección 12 |
| **`HTTPException`** | Excepción que FastAPI convierte automáticamente en una respuesta HTTP de error, con el código de estado correcto (`404`, `400`, ...). | Clase 3 / sección 11 |
| **Middleware** | Código que envuelve **cada** petición, corriendo antes y después del endpoint (medir tiempos, agregar headers) — se define una vez y aplica a toda la app. | Clase 3 / sección 13 |
| **`app.include_router(...)`** | La línea que "monta" un `APIRouter` entero (con todos sus endpoints) sobre la `app`, sumando el prefijo que se le pase acá al del propio router. | sección 13 |


## 💾 2. ¿Qué es la persistencia de datos?

**Persistencia de datos** es la capacidad de un dato de sobrevivir a la ejecución del
programa que lo creó — que siga existiendo después de cerrar la terminal, apagar el
servidor o reiniciar la app.

```python
tickets_en_memoria = []
tickets_en_memoria.append("Ticket 1001")
print(tickets_en_memoria)
```
```
$ python3 memoria.py
['Ticket 1001']
$ python3 memoria.py    # segunda corrida: no recuerda nada de la anterior
['Ticket 1001']
```

Todo lo trabajado en listas/diccionarios desde la Clase 1 vive en **RAM**: rápido de
leer y escribir, pero **volátil** — desaparece apenas termina el proceso. Para que un
dato persista, tiene que quedar escrito en algún medio que sobreviva al proceso: un
archivo en disco, o una base de datos.

| Medio | Sobrevive al cierre del programa | Estructura / consultas | Concurrencia (varios procesos a la vez) |
|---|---|---|---|
| Variable en RAM | ❌ No | La que le dé el código | No aplica — vive en un solo proceso |
| Archivo (`.txt`, `.json`) | ✅ Sí | Ninguna — hay que parsear todo a mano | Riesgo de corromper el archivo si dos procesos escriben a la vez |
| Base de datos relacional (PostgreSQL) | ✅ Sí | Tablas, tipos, relaciones, índices — impuestos por el motor | Maneja el acceso concurrente de forma segura (transacciones) |

> 💡 Esta es la razón de fondo de toda la clase: un servidor backend puede reiniciarse,
> escalar a varias instancias o recibir miles de peticiones a la vez — los datos de
> negocio (tickets, usuarios, categorías) no pueden vivir solo en una lista de Python,
> necesitan un medio persistente y compartido. **PostgreSQL** es ese medio; el **ORM**
> (sección siguiente) es la capa que lo hace manejable desde Python.

> 🔗 Fuente: [Persistencia (informática) — Wikipedia](https://es.wikipedia.org/wiki/Persistencia_(inform%C3%A1tica))

### 🗺️ Diagrama: arquitectura de persistencia de datos (Python + ORM + Alembic)

![Diagrama de arquitectura: Cliente → API FastAPI → Capa de Servicios → Capa de Persistencia (ORM SQLAlchemy + Migraciones Alembic) → Base de datos PostgreSQL, con las características de la persistencia (ACID, sesiones, integridad, consultas, auditoría, backups, migraciones)](/clase-04-arquitectura-persistencia-datos.png)

El diagrama de arriba es el mapa completo de esta clase: cada caja es una capa por la
que pasa un dato hasta quedar persistido, y cada una tiene su propia responsabilidad.

| Capa | Qué hace | Piezas | Dónde se ve en esta clase |
|---|---|---|---|
| **Cliente** | Consume la API (web, móvil) — no es parte del backend, pero es quien dispara todo | Web / Móvil (React, HTML, etc.) | Fuera del alcance de este curso de backend |
| **API (FastAPI)** | Recibe la petición HTTP, la valida y arma la respuesta | Rutas (endpoints), validaciones, autenticación/autorización, serialización (Pydantic), respuestas | [Clase 3](Clase-03.md) (teoría de FastAPI) + [sección 12 — Router](#🌐-12-router-routers-tickets-py) de esta clase |
| **Capa de servicios** | Traduce la petición en reglas de negocio — no sabe nada de HTTP ni de SQL | Reglas de negocio, cálculo de indicadores, orquestación, gestión de sesiones de trabajo | [sección 11 — Capa de servicios: `TicketService`](#🧠-11-capa-de-servicios-ticketservice) |
| **Capa de persistencia → ORM (SQLAlchemy)** | Traduce objetos Python ↔ filas de la base de datos | Modelos (entidades), relaciones, sesión (`Session`), consultas (`select`), *Unit of Work*, eventos ORM | [sección 3 — ¿Qué es un ORM?](#🗄️-3-¿que-es-un-orm) + [sección 9 — Modelos SQLAlchemy](#🗄️-9-modelos-sqlalchemy-orm-user-category-ticket) + [sección 10 — Repository Pattern](#🧩-10-repository-pattern-ticketrepository) |
| **Capa de persistencia → Migraciones (Alembic)** | Versiona los *cambios* al esquema de la base de datos | Entorno de migraciones (`env.py`), versionado de esquema, scripts de migración, historial, upgrade/downgrade | [sección 14 — Crear las tablas con Alembic](#🐘-14-crear-las-tablas-con-alembic-migraciones-versionadas) |
| **Base de datos** | El almacenamiento persistente final | PostgreSQL — datos persistentes | [sección 6 — PostgreSQL corriendo en Docker](#🐘-6-postgresql-corriendo-en-docker) |

**Características de la persistencia** (franja inferior del diagrama) — lo que un motor
como PostgreSQL garantiza y un archivo suelto no:

| Característica | Definición |
|---|---|
| **Transacciones (ACID)** | 4 garantías sobre cada operación: **A**tomicidad (todo o nada — si algo falla a mitad de camino, se deshace por completo), **C**onsistencia (nunca deja la base en un estado inválido), **I**solamiento (una transacción no ve los cambios a medias de otra que corre al mismo tiempo), **D**urabilidad (una vez confirmado con `commit()`, sobrevive incluso a una caída del servidor). |
| **Manejo de sesiones y conexiones** | La `Session`/`SessionLocal` de SQLAlchemy (`get_db()`) reutiliza conexiones de un *pool* en vez de abrir una nueva por cada consulta — ver `db/database.py`. |
| **Integridad y consistencia** | Las `ForeignKeyConstraint`, `UniqueConstraint` y `nullable=False` de los modelos (sección 9) las impone la base — no hace falta validarlas a mano en Python. |
| **Consultas optimizadas** | Índices y planificador de consultas de Postgres — por eso "ORM no significa dejar de saber SQL" (sección 4). |
| **Auditoría y trazabilidad** | Poder saber *qué* cambió, *cuándo* y *quién* lo hizo — típicamente con columnas `created_at`/`updated_at` o una tabla de logs (no cubierto todavía en este proyecto). |
| **Backups y recuperación** | Copias de la base para poder restaurarla ante un desastre — responsabilidad de PostgreSQL/infraestructura, no del código de la app. |
| **Migraciones controladas** | Lo que hace Alembic (sección 14): cada cambio de esquema queda versionado y es reversible, en vez de editar la base a mano. |

> 🔗 Fuente: [¿Qué es ACID en bases de datos? — KeepCoding](https://keepcoding.io/blog/que-es-acid-bases-datos/)

## 🗄️ 3. ¿Qué es un ORM?

**ORM (Object-Relational Mapping / Mapeo Objeto-Relacional)**: la capa que **traduce
información entre dos mundos que hablan distinto**:

- El mundo de **Python** (clases, objetos, atributos).
- El mundo de la **base de datos relacional** (tablas, filas, columnas).

La idea central es **modelar información como tablas, pero manipularla como objetos**:

### 🗺️ Diagrama: cómo el ORM traduce Python a SQL

![Diagrama de flujo: código Python (class Ticket / ticket = Ticket(...)) traducido por el ORM SQLAlchemy a SQL real (CREATE TABLE / INSERT INTO) en PostgreSQL](/clase-04-orm-flujo.png)

| Mundo Python (objetos) | Mundo SQL (tablas) |
|---|---|
| Clase (`class Ticket`) | Tabla (`tickets`) |
| Atributo (`ticket.priority`) | Columna (`priority`) |
| Instancia/objeto (`ticket = Ticket(...)`) | Fila/registro (`INSERT INTO ...`) |
| `ticket.priority = "Cerrado"` | `UPDATE tickets SET priority = 'Cerrado'` |

> 💡 En resumen: el ORM te deja **modelar tus datos como clases de Python** y él se
> encarga de generar el SQL correspondiente (INSERT/SELECT/UPDATE/DELETE) por debajo.

### 🗺️ Diagrama: modelo de datos del sistema de tickets

![Diagrama entidad-relación: users, categories y tickets con sus claves primarias, foráneas y relaciones 1:N](/clase-04-er-tickets.png)

Tres entidades y sus relaciones (mismo dominio de los ejemplos SQL de arriba), con los
nombres reales que quedaron en el código (`02-Ejercicios/Clase-04/app/models/`). Los
nombres de tabla van en **plural** (`users`, `categories`, `tickets`) — la convención
estándar en SQLAlchemy/Django/Rails para dejar claro que una tabla contiene *muchas*
filas de ese tipo; la clase Python/entidad conceptual sí va en singular (`User`,
`Category`, `Ticket`).

| Entidad (tabla) | Campos | Rol |
|---|---|---|
| `users` | `id`, `name`, `email` | Quién reporta el ticket |
| `categories` | `id`, `name` | Cómo se clasifica el ticket |
| `tickets` | `id`, `title`, `description`, `priority`, `status`, `requester_id`, `category_id` | El registro central; conecta con las otras dos (las 2 relaciones **1:N** del diagrama) |

> 💡 El `JOIN` de la sección siguiente (`... ON t.category_id = c.id`) es exactamente la
> flecha `category_id → categories.id` del diagrama. El ORM modela esa misma relación
> como clases que se referencian entre sí (`Ticket.category`), en vez de escribir el
> `JOIN` a mano — se ve en la Parte Práctica.

> 📌 Convención: el campo de la FK se nombra `<entidad>_id` (`requester_id`,
> `category_id`) — así se lee directo qué tabla referencia.

## 🐘 4. SQL esencial — lo que SQLAlchemy hará por nosotros

> Aunque usemos ORM, **comprender SQL es imprescindible** para depurar, optimizar y
> tomar decisiones informadas.

Las 4 operaciones base que después el ORM va a generar por nosotros:

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

> ⚠️ **ORM no significa dejar de saber SQL.** Ahorra escribir el SQL a mano en el día a
> día, pero cuando algo va lento, una consulta no trae lo esperado, o hay que optimizar
> un `JOIN` complejo, hace falta entender qué SQL está generando por debajo.

**¿Con qué técnica genera ese SQL?** SQLAlchemy no arma el texto SQL a mano
concatenando strings — usa un **compilador de expresiones** (*SQL Expression
Language*): la consulta se arma primero como un objeto Python abstracto
(`select(Ticket).where(...)`, `op.create_table(...)` — ver [sección 14](#🐘-14-crear-las-tablas-con-alembic-migraciones-versionadas)),
y recién al ejecutarla un **compilador específico del motor** (el *dialect*: `postgresql`,
`mysql`, `sqlite`...) lo traduce al SQL real de ese motor. Por eso el mismo código Python
puede apuntar a Postgres, MySQL o SQLite sin tocar una sola consulta — solo cambia la
URL de conexión y el dialecto que SQLAlchemy elige solo a partir de ella.

**¿Es exclusivo de Python?** No — el patrón ORM (traducir objetos ↔ tablas) existe en
prácticamente todos los lenguajes de backend, cada uno con su propia librería:

| Lenguaje | ORM más usado |
|---|---|
| Python | SQLAlchemy, Django ORM |
| Java / Kotlin | Hibernate (JPA) |
| C# / .NET | Entity Framework |
| Ruby | Active Record (Ruby on Rails) |
| JavaScript / TypeScript | Prisma, TypeORM, Sequelize |
| PHP | Doctrine, Eloquent (Laravel) |

> 🧪 Tip de entrevista: si todos los ORM resuelven lo mismo (Python/Java/JS ↔ SQL), ¿qué
> cambia entre ellos? Sobre todo el **estilo de API** (*Active Record*, donde el propio
> modelo sabe guardarse a sí mismo, vs *Data Mapper*, como SQLAlchemy — el patrón que
> ya se ve en el [Repository Pattern](#🧩-10-repository-pattern-ticketrepository) de esta
> clase, donde el modelo no sabe nada de cómo persistirse) y qué tan explícito o
> "mágico" es cada uno — pero el problema de fondo es el mismo en cualquier lenguaje.

## 🏗️ 5. Arquitectura del proyecto (estructura de carpetas)

Estructura por capas del proyecto, en uso de acá en adelante para FastAPI + SQLAlchemy +
Alembic:

```
app/
├── core/            # settings, variables de entorno
├── db/              # engine, sesión, Base de SQLAlchemy
├── models/          # tablas (User, Category, Ticket)
├── repositories/    # Repository Pattern (acceso a datos)
├── routers/         # endpoints de FastAPI
├── schemas/         # esquemas Pydantic (validación)
├── services/        # lógica de negocio
├── migrations/      # historial de Alembic
└── requirements.txt # dependencias del proyecto
```

Ya quedó creada igual en `02-Ejercicios/Clase-04/app/` (sin `__init__.py` — Python 3.3+
no los exige, ver el callout en "Errores de esta clase" más abajo).

### 🗺️ Diagrama: la estructura de carpetas, diferenciada por capa

![Diagrama de arquitectura: la carpeta app/ con sus 9 subcarpetas/archivos agrupados y diferenciados por color según su capa — Capa API (routers/, schemas/) en índigo, Capa de negocio (services/) en morado, Capa de datos (core/, db/, models/, repositories/) en verde, Herramientas (migrations/, requirements.txt) en celeste/gris](/clase-04-estructura-carpetas.png)

Mismo contenido que el árbol ASCII de arriba, pero agrupado y **diferenciado por
color** según la capa a la que pertenece cada carpeta — a diferencia del diagrama
siguiente (que muestra el *flujo* de una petición), este es un mapa estático de
"qué hay adentro de `app/` y a qué grupo pertenece cada cosa".

### 🗺️ Diagrama: cómo se conectan las capas (con el código real)

![Diagrama de arquitectura por capas: Cliente HTTP → routers/ (pendiente) → schemas/ticket.py → services/ (pendiente) → repositories/TicketRepository → models/ → db/database.py → PostgreSQL, con core/config.py alimentando la configuración](/clase-04-arquitectura-capas.png)

Con los nombres reales de `02-Ejercicios/Clase-04/app/` (no genéricos): `routers/` y
`services/` aparecen con **borde punteado** porque todavía no se escribieron — el resto
(`schemas/ticket.py`, `repositories/ticket_repository.py`, `models/`,
`core/config.py`, `db/database.py`) ya está escrito y verificado contra
`curso-postgres`.

> 📎 Versión genérica de este mismo flujo (reutilizable en cualquier proyecto FastAPI,
> sin nombres de esta clase en particular) en
> [00-Notas/05-Estructura-Proyecto-FastAPI.md](../00-Notas/05-Estructura-Proyecto-FastAPI.md).

> 📎 Detalle de qué va en cada carpeta y el flujo de una petición (router → schema →
> service → repository → model → db), en la nota temática:
> [00-Notas/05-Estructura-Proyecto-FastAPI.md](../00-Notas/05-Estructura-Proyecto-FastAPI.md)

# 💻 PARTE PRÁCTICA

Carpeta de trabajo: `02-Ejercicios/Clase-04/app/`

## 🐘 6. PostgreSQL corriendo en Docker

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

## 🐍 7. Entorno virtual y dependencias

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

## 📄 8. Primer schema: `schemas/ticket.py`

Primer archivo de código de la clase — los schemas de Pydantic (capa `schemas/`, ver la
sección teórica "🏗️ Arquitectura del proyecto" arriba) para validar los datos de un
ticket:

> 📌 **`schemas/` no es la conexión a la base de datos** — son cosas distintas. Un
> `schema` define la **forma de los datos que entran y salen por HTTP** (Pydantic),
> pura validación en Python; la conexión real (`engine`, `Session`) vive en
> `db/database.py` (sección 9). Se empieza acá y no por `db/`/`models/` porque un
> schema no depende de nada más — se escribe y se prueba sin Postgres corriendo (mismo
> patrón `BaseModel`/`Field` ya visto en la [Clase 3](Clase-03.md)), mientras que la
> conexión real recién se puede verificar con la base levantada. Es ir de afuera hacia
> adentro: primero qué forma tienen los datos en el contrato de la API, después cómo se
> guardan.

```python
# 02-Ejercicios/Clase-04/app/schemas/ticket.py
from pydantic import BaseModel, ConfigDict, Field


# Lo que el CLIENTE manda para crear un ticket (entrada de la API)
class TicketCreate(BaseModel):
    # Título corto del problema — entre 5 y 120 caracteres
    title: str = Field(min_length=5, max_length=120)
    # Detalle completo del problema — entre 10 y 500 caracteres
    description: str = Field(min_length=10, max_length=500)
    # Urgencia del ticket — si no la mandan, queda "Media" por defecto
    priority: str = Field(default="Media")

    # FK: quién reporta el ticket (id de un user que ya existe, > 0)
    requester_id: int = Field(gt=0)
    # FK: a qué categoría pertenece (id de una category que ya existe, > 0)
    category_id: int = Field(gt=0)


# Lo que el CLIENTE manda para actualizar un ticket (todo opcional)
class TicketUpdate(BaseModel):
    # Opcional: cambiar solo la prioridad, sin tocar el resto
    priority: str | None = None
    # Opcional: cambiar solo la descripción, sin tocar el resto
    description: str | None = None


# Lo que la API le DEVUELVE al cliente (salida de la API)
class TicketResponse(BaseModel):
    # El id que le asignó Postgres al crear el registro
    id: int
    title: str
    description: str
    priority: str

    # Las mismas FK, ya guardadas en la base de datos
    requester_id: int
    category_id: int
```

> 📌 Definiciones de `Pydantic`/`BaseModel`/`Field`/`ConfigDict`/`str`, y la mecánica de
> `import` y `nombre: tipo = valor`, están en el
> [glosario de la sección 1](#📚-1-definiciones-clave) — acá va directo el detalle
> línea por línea aplicado a este archivo puntual:

**Línea por línea:**

| Línea | Qué hace |
|---|---|
| `from pydantic import BaseModel, ConfigDict, Field` | Importa 3 piezas de Pydantic: `BaseModel` (clase base que activa toda la validación automática), `Field` (agrega reglas extra a un campo puntual) y `ConfigDict` (configura el comportamiento general del modelo — importado pero **todavía sin usar** en este archivo, ver callout de abajo). |
| `class TicketCreate(BaseModel):` | Declara el primer schema **heredando de `BaseModel`** — esa herencia (Clase 2) es lo que le da a `TicketCreate` toda la validación de Pydantic gratis. |
| `title: str = Field(min_length=5, max_length=120)` | Campo **obligatorio** de tipo `str`; `Field(...)` agrega reglas extra al tipo: mínimo 5 caracteres, máximo 120. |
| `description: str = Field(min_length=10, max_length=500)` | Igual que `title`, pero exige entre 10 y 500 caracteres. |
| `priority: str = Field(default="Media")` | Campo `str` con **valor por defecto**: si el cliente no lo manda, Pydantic completa `"Media"` solo. |
| `requester_id: int = Field(gt=0)` | Entero obligatorio; `gt=0` ("*greater than* 0") exige que sea mayor a cero — evita un id inválido como `0` o negativo. Es la FK hacia `user.id` del diagrama de la teoría. |
| `category_id: int = Field(gt=0)` | Misma regla que `requester_id`, para la FK hacia `category.id`. |
| `class TicketUpdate(BaseModel):` | Segundo schema — pensado para **actualizaciones parciales** (no crear un ticket nuevo, sino modificar uno existente). |
| `priority: str \| None = None` | Único campo del schema, y **opcional**: `str \| None` (sintaxis moderna de la Clase 1) dice "texto o nada", y `= None` es el valor por defecto si no se manda. Así se puede actualizar solo la prioridad sin tener que reenviar `title`/`description`. |
| `class TicketResponse(BaseModel):` | Tercer schema — la forma en la que la API **le devuelve** el ticket al cliente. |
| `id: int` | Recién en la respuesta aparece `id`: no lo manda el cliente al crear (lo genera la base de datos), pero sí viaja de vuelta para que el cliente sepa qué id le tocó. |
| `title: str` / `description: str` / `priority: str` | Se repiten los mismos 3 campos que en `TicketCreate`, pero **sin** `Field(min_length=..., ...)` — ya no hace falta revalidar longitud: esos datos ya pasaron esa validación cuando se creó el ticket. |
| `requester_id: int` / `category_id: int` | Se devuelven tal cual, también sin `gt=0` — mismo motivo: ya se validaron al entrar. |

> 📝 `ConfigDict` está importado pero no se usa todavía en ninguna de las 3 clases — no es
> un error, probablemente quedó preparado para más adelante, cuando
> `TicketResponse` necesite leer datos directo de un objeto ORM de SQLAlchemy (no de un
> `dict`). Ahí se usa así: `model_config = ConfigDict(from_attributes=True)` — sin eso,
> Pydantic v2 no sabe convertir un objeto `Ticket` del ORM en un `TicketResponse`.

> 🧪 **Tip de entrevista:** *¿Por qué separar Create/Update/Response en 3 clases en vez
> de una sola?* (repasá la tabla "Línea por línea" de arriba: cada una valida un
> **contrato distinto** de la API). Meterlos en un solo schema obligaría a hacer todos
> los campos opcionales, perdiendo validaciones — ej. `title` dejaría de ser
> obligatorio al crear.

> 💡 `gt=0` en `requester_id`/`category_id` evita un id inválido como `0` o negativo —
> son las FK del diagrama ER de la teoría.

## 🗄️ 9. Modelos SQLAlchemy (ORM): `User`, `Category`, `Ticket`

Las 3 tablas del diagrama de la teoría, ya como clases Python en `models/`. Usan el
estilo **moderno de SQLAlchemy 2.0** (`Mapped[...]` + `mapped_column(...)`, tipado con
anotaciones de Python) en vez del `Column(...)` clásico de tutoriales viejos.

**`core/config.py`** — lee la URL de conexión desde un archivo `.env` (nunca hardcodeada
en el código, ni subida a git):
```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
```

`02-Ejercicios/Clase-04/app/.env` (excluido de git en `.gitignore`):
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/curso_backend
```

**`db/database.py`** — el motor, la sesión y el `Base` del que heredan todos los modelos:
```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

> 💡 **`get_db()`** es una función *generadora* (usa `yield` en vez de `return`) pensada
> para ser una **dependencia de FastAPI**: abre una sesión, la "presta" al endpoint que
> la pida (`yield db`), y pase lo que pase — éxito o excepción — el `finally` la cierra
> siempre. Evita el error clásico de dejar conexiones abiertas colgadas.

> 💡 **`pool_pre_ping=True`**: antes de usar una conexión reciclada del pool, SQLAlchemy
> le manda un ping rápido para confirmar que sigue viva. Sin esto, si Postgres se
> reinicia o la conexión se cae por inactividad, el primer query después falla con un
> error de conexión perdida en vez de reconectar sola.

> 🐳 **`Base = declarative_base()` vs `class Base(DeclarativeBase): pass`** — ambas
> formas existen en SQLAlchemy 2.0 y funcionan igual; la segunda (la que quedó acá) es
> la más nueva, pensada específicamente para combinar con el estilo tipado
> `Mapped[...]` que usan `models/user.py`, `category.py` y `ticket.py`.

**`models/user.py`**:
```python
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from models.ticket import Ticket


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="requester")
```

**`models/category.py`**:
```python
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from models.ticket import Ticket


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="category")
```

**`models/ticket.py`** — la tabla central, con las 2 FK del diagrama:
```python
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from models.category import Category
    from models.user import User


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="Media")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Abierto")

    requester_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    requester: Mapped["User"] = relationship(back_populates="tickets")
    category: Mapped["Category"] = relationship(back_populates="tickets")
```

> 💡 **`ForeignKey("users.id")`** es el mismo `requester_id (FK → user.id)` del diagrama
> de la teoría, ya en código: le dice a Postgres "esta columna solo puede tener un valor
> que exista en `users.id`". **`relationship(...)`** es distinto — es una comodidad de
> Python: le permite a SQLAlchemy hacer `ticket.requester.name` en vez de tener que
> escribir el `JOIN` a mano cada vez.

> 💡 **`back_populates`** conecta las dos puntas de una relación: `Ticket.requester`
> ↔ `User.tickets` son **la misma relación vista desde cada lado**. Si cambian un
> `ticket.requester`, `user.tickets` se entera solo (y viceversa) — por eso el nombre
> que le pasás a `back_populates` tiene que ser **exactamente** el nombre del atributo
> del otro lado.

> 💡 **`if TYPE_CHECKING:`** — el motivo de este bloque en los 3 archivos: `User` y
> `Ticket` (y `Category` y `Ticket`) se referencian entre sí. Si se importaran directo
> (sin `TYPE_CHECKING`) se arma un **import circular** y Python no arranca. Con
> `TYPE_CHECKING` (que en tiempo real siempre vale `False`) el editor entiende los tipos
> sin que el import se ejecute de verdad — ver el error completo abajo.

Verificado con `configure_mappers()` de SQLAlchemy (chequea que todas las relaciones
declaradas encuentren su otra punta):
```bash
python3 -c "
from models.user import User
from models.category import Category
from models.ticket import Ticket
from sqlalchemy.orm import configure_mappers
configure_mappers()
print('OK')
"
```

## 🧩 10. Repository Pattern: `TicketRepository`

**Modelos vs. Repositorio — dos capas con roles distintos:**

| Capa | Qué es | Analogía |
|---|---|---|
| `models/` (`Ticket`, `User`, `Category`) | La **representación** de la base de datos — define la *forma* de cada tabla (qué columnas tiene, cómo se relaciona con otras) | El plano de una casa |
| `repositories/` (`TicketRepository`) | La capa que **interactúa constantemente** con la base de datos — la que de verdad abre la sesión, ejecuta las consultas, guarda, actualiza, borra | El albañil que construye/repara con ese plano |

Los modelos son **pasivos**: describen la estructura pero no hacen nada por sí solos. El
repositorio es **activo**: cada vez que la app necesita leer o escribir tickets, pasa
por acá.

> 💡 `db: Session` (abajo) no tiene nada que ver con cómo se llame el archivo de
> conexión (`db/database.py` vs. otro nombre como `db/session.py`) — `Session` sale
> siempre de la librería `sqlalchemy.orm`. Ver "Import de librería vs. nombre de tu
> archivo" en [00-Notas/02-Conceptos.md](../00-Notas/02-Conceptos.md).

```python
# 02-Ejercicios/Clase-04/app/repositories/ticket_repository.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.ticket import Ticket
from schemas.ticket import TicketCreate, TicketUpdate


class TicketRepository:
    # Trae TODOS los tickets, ordenados por id
    def get_all(self, db: Session) -> list[Ticket]:
        statement = select(Ticket).order_by(Ticket.id)
        return list(db.scalars(statement).all())

    # Trae UN ticket por su id (None si no existe)
    def get_by_id(self, db: Session, ticket_id: int) -> Ticket | None:
        return db.get(Ticket, ticket_id)

    # Crea un ticket nuevo a partir de los datos validados por TicketCreate
    def create(self, db: Session, data: TicketCreate) -> Ticket:
        ticket = Ticket(**data.model_dump())
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    # Actualiza SOLO los campos que vinieron en data (exclude_unset=True)
    def update(self, db: Session, ticket: Ticket, data: TicketUpdate) -> Ticket:
        changes = data.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(ticket, field, value)
        db.commit()
        db.refresh(ticket)
        return ticket

    # Borra un ticket existente
    def delete(self, db: Session, ticket: Ticket) -> None:
        db.delete(ticket)
        db.commit()
```

**Qué es `statement`:** `select(Ticket).order_by(Ticket.id)` **no consulta la base de
datos todavía** — arma un objeto Python que *describe* la consulta ("traeme todos los
`Ticket`, ordenados por `id`"), como armar el pedido antes de mandarlo a la cocina. Recién
cuando ese `statement` se le pasa a `db.scalars(statement)` (o `db.execute(...)`), la
sesión lo traduce a SQL real y lo manda a Postgres — **ahí** ocurre la ejecución.

### 🗺️ Diagrama: `statement` vs. ejecución real

![Diagrama de flujo: select(Ticket).order_by(Ticket.id) es la receta que no ejecuta nada, db.scalars(statement) la ejecuta, y recién ahí corre SELECT * FROM tickets ORDER BY id en PostgreSQL](/clase-04-statement-diferido.png)

> 💡 Por eso se puede armar un `statement` en varios pasos (agregarle `.where(...)`,
> `.limit(...)`, etc. antes de ejecutarlo) — no dispara ningún query hasta que una
> `Session` lo ejecuta de verdad. Esto se llama **evaluación diferida** (*lazy*).

Los otros 3 métodos usan `Session` directo, sin pasar por `select()`:
- `db.get(Ticket, ticket_id)` — atajo para buscar por clave primaria (más simple que un `select().where()`).
- `db.add(ticket)` + `db.commit()` — agrega el objeto nuevo a la sesión y confirma el cambio en la base de datos.
- `db.refresh(ticket)` — vuelve a leer el objeto desde la base de datos (para traer, por ejemplo, el `id` que Postgres generó automáticamente al hacer el `INSERT`).
- `db.delete(ticket)` + `db.commit()` — marca el objeto para borrar y confirma.

> 🧪 **Tip de entrevista:** *¿Por qué el repositorio recibe la `Session` como parámetro
> (`db: Session`) en vez de crear la suya propia?* Se llama **inyección de
> dependencias**: quien llama al método (más adelante, un endpoint de `routers/` vía
> `Depends(get_db)`) decide qué sesión usar. Facilita testear el repositorio con una
> sesión de prueba, sin tocar la base de datos real.

## 🧠 11. Capa de servicios: `TicketService`

**Repositorio vs. Servicio — no hacen lo mismo:** `TicketRepository` solo sabe **leer y
escribir** en la base de datos (CRUD puro, sin opinión). `TicketService` es la capa de
arriba: aplica las **reglas del negocio** (qué hacer si el ticket no existe, qué pasa
antes/después de guardar) y es lo que un futuro `router` va a llamar — nunca llama al
repositorio directo.

```python
# 02-Ejercicios/Clase-04/app/services/ticket_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.ticket import Ticket
from repositories.ticket_repository import TicketRepository
from schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def list_tickets(self, db: Session) -> list[Ticket]:
        return self.repository.get_all(db)

    def get_ticket(self, db: Session, ticket_id: int) -> Ticket:
        ticket = self.repository.get_by_id(db, ticket_id)
        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket no encontrado",
            )
        return ticket

    def create_ticket(self, db: Session, data: TicketCreate) -> Ticket:
        return self.repository.create(db, data)

    def update_ticket(self, db: Session, ticket_id: int, data: TicketUpdate) -> Ticket:
        ticket = self.get_ticket(db, ticket_id)
        return self.repository.update(db, ticket, data)

    def delete_ticket(self, db: Session, ticket_id: int) -> None:
        ticket = self.get_ticket(db, ticket_id)
        self.repository.delete(db, ticket)
```

**Qué agrega esta capa que el repositorio no tiene:**

| Método | Qué hace el repositorio | Qué le agrega el service |
|---|---|---|
| `get_ticket` | `get_by_id` devuelve `Ticket \| None` (puede ser `None`) | Si es `None`, lanza `HTTPException(404, "Ticket no encontrado")` — el resto de la app nunca tiene que volver a chequear "¿existe?" a mano |
| `update_ticket` / `delete_ticket` | Reciben el objeto `Ticket` ya encontrado | Primero llaman a `self.get_ticket(...)` — si no existe, ya cortan ahí con el 404, antes de intentar `update`/`delete` |

> 💡 **`self.repository = repository`** en el `__init__`: el service **recibe** el
> repositorio de afuera (otra vez inyección de dependencias, igual que `db: Session` en
> el repositorio) — no hace `self.repository = TicketRepository()` adentro. Así, para
> testear el service, se le puede pasar un repositorio falso (*mock*) sin tocar la base
> de datos real.

> ⚠️ **Error real de esta clase:** los imports decían `from app.models.ticket import
> Ticket` (con el prefijo `app.`) y tiraban `ModuleNotFoundError: No module named
> 'app'` — mismo error que ya había aparecido en `repositories/ticket_repository.py`.
> En este proyecto no hay ningún paquete llamado `app` (se corre desde adentro de esa
> carpeta), así que el import correcto es `from models.ticket import Ticket`, sin
> prefijo. Detalle completo en la tabla de errores, abajo.

## 🌐 12. Router: `routers/tickets.py`

Última capa — los endpoints HTTP reales. El `router` llama al `service` (nunca directo
al `repository`, respetando el orden de capas del diagrama de arriba):

```python
# 02-Ejercicios/Clase-04/app/routers/tickets.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from repositories.ticket_repository import TicketRepository
from schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def get_ticket_service() -> TicketService:
    return TicketService(repository=TicketRepository())


@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.list_tickets(db)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.get_ticket(db, ticket_id)


@router.post("/", response_model=TicketResponse, status_code=201)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.create_ticket(db, data)


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.update_ticket(db, ticket_id, data)


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    service.delete_ticket(db, ticket_id)
```

> 📌 **La ruta completa no es `/tickets` — es `/api/v1/tickets`.** El `prefix="/tickets"`
> de acá es del `router` solo; `main.py` lo monta con un prefijo **adicional**:
> ```python
> app.include_router(tickets_router, prefix="/api/v1")
> ```
> Los dos prefijos se **concatenan**: `/api/v1` (de `main.py`) + `/tickets` (de este
> `router`) = `/api/v1/tickets`. Es la convención de **versionado de APIs** ya vista en
> la [Clase 3](Clase-03.md) — reservar `/api/v1/...` desde el día 1 deja lugar para un
> `/api/v2/...` el día que haya un cambio que rompa compatibilidad, sin tocar `/v1`.

> 💡 **`Depends(get_db)` y `Depends(get_ticket_service)`**: FastAPI resuelve estas
> dependencias **antes** de correr la función del endpoint — abre la sesión de BD y
> arma el `TicketService` automáticamente, sin que cada función tenga que hacerlo a
> mano. Es la misma inyección de dependencias del repository y el service, un nivel
> más arriba.

> 💡 **`response_model=TicketResponse`**: FastAPI toma lo que devuelve la función (un
> objeto `Ticket` del ORM) y lo convierte al schema de salida. Para que esa conversión
> funcione hubo que agregarle a `TicketResponse` (en `schemas/ticket.py`):
> `model_config = ConfigDict(from_attributes=True)` — sin eso, Pydantic no sabe leer
> atributos de un objeto ORM (solo sabía leer de un `dict`).

## 🚀 13. `main.py`: cómo se arma la aplicación final

Hasta acá cada capa se armó por separado: `schemas/`, `models/`, `repositories/`,
`services/`, `routers/`. **`main.py` es donde todo eso se junta en UNA sola aplicación
en ejecución** — es literalmente el archivo que corre `uvicorn main:app` (el `app` de
`main:app` es la variable que se crea acá, sección 12/`--reload`).

```python
# 02-Ejercicios/Clase-04/app/main.py
from time import perf_counter  # para medir cuánto tarda cada petición (middleware)

from fastapi import FastAPI, Request

# Importar los 3 modelos ACÁ (antes de que se use cualquier Ticket de
# verdad) — si no, sale InvalidRequestError al crear el primer ticket
from models.user import User
from models.category import Category
from models.ticket import Ticket

# El router YA TRAE sus 5 endpoints armados (routers/tickets.py) — acá
# solo se importa para montarlo más abajo con app.include_router(...)
from routers.tickets import router as tickets_router

# Las tablas ya NO se crean acá con create_all() — las crea/actualiza
# Alembic (migrations/), corriendo "alembic upgrade head" a mano antes
# de levantar la app. Es la forma versionada de mantener el esquema.


# ---------------------------------------------------------
# CREACIÓN DE LA APLICACIÓN
# ---------------------------------------------------------

# Esta ÚNICA instancia es la "app" — el objeto al que se le cuelgan
# middleware, endpoints propios (/health) y routers enteros (Tickets).
# title/description/version alimentan directo el Swagger de /docs.
app = FastAPI(
    title="HelpDesk API",
    description=(
        "API REST para la gestión de solicitudes "
        "de soporte técnico utilizando FastAPI, "
        "SQLAlchemy y PostgreSQL."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------

@app.middleware("http")
async def add_process_time(
    request: Request,
    call_next,  # la función que sigue la cadena — el endpoint real
):
    """
    Mide el tiempo total utilizado para procesar
    cada solicitud HTTP.
    """

    start = perf_counter()  # arranca el cronómetro ANTES del endpoint

    response = await call_next(request)  # acá corre el endpoint (health/tickets)

    elapsed = perf_counter() - start  # cuánto tardó, en segundos

    response.headers[
        "X-Process-Time"
    ] = f"{elapsed:.6f}"  # se agrega a TODAS las respuestas, sin excepción

    return response


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

# Endpoint DIRECTO sobre "app" (no viene de un router) — por eso su URL
# final es solo /health, sin el prefijo /api/v1 que sí lleva Tickets.
@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    """
    Permite verificar que la API se encuentre funcionando.
    """

    return {
        "status": "ok",
        "service": "El API backend de HelpDesk esta operativo",
        "version": "1.0.0",
    }


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

# La línea que "genera" los 5 endpoints finales: toma TODAS las rutas ya
# definidas en tickets_router (con su propio prefix="/tickets") y las
# cuelga de "app" bajo /api/v1 -> URL real = /api/v1/tickets/...
app.include_router(
    tickets_router,
    prefix="/api/v1",
)
```

### 🧱 Bloque por bloque

| Bloque | Qué hace | Por qué está ahí |
|---|---|---|
| **Imports** | Trae `FastAPI`/`Request` (el framework), los 3 modelos (`User`, `Category`, `Ticket`) y el `router` de tickets. | Los modelos se importan acá aunque `main.py` nunca los use directo — es el mismo motivo que en `migrations/env.py` (sección 14): si la clase nunca se ejecuta, no queda registrada en `Base.metadata`. |
| **Creación de la aplicación** | `app = FastAPI(...)` — una sola vez, en todo el archivo. | Todo lo demás (middleware, endpoints, routers) se cuelga de esta misma variable `app`. |
| **Middleware** | `add_process_time` — corre **alrededor de cada petición**, sin excepción (Clase 3, sección de middleware). | Mide cuánto tarda la API en responder, sin tener que agregar ese código en cada endpoint por separado. |
| **Health check** | `@app.get("/health")` — un endpoint mínimo que solo confirma "estoy viva". | Estándar en cualquier API real: permite que un balanceador de carga o un monitoreo verifique que el servicio responde, sin depender de la base de datos. |
| **Routers** | `app.include_router(tickets_router, prefix="/api/v1")` — una sola línea. | Es la que **conecta** los 5 endpoints ya definidos en `routers/tickets.py` (sección 12) con la aplicación real. |

### 🛣️ Cómo se generan los endpoints finales — la cadena de prefijos

Ningún endpoint se "define" en `main.py` (salvo `/health`) — los de tickets ya estaban
completos en `routers/tickets.py`. Lo que hace `main.py` es **montarlos**, y en ese
montaje se concatenan dos prefijos distintos:

```
routers/tickets.py                         main.py
──────────────────                         ───────
router = APIRouter(prefix="/tickets")  +   app.include_router(tickets_router,
                                                                prefix="/api/v1")
@router.get("/")            ──────────────────────────────►  GET  /api/v1/tickets/
@router.get("/{ticket_id}") ──────────────────────────────►  GET  /api/v1/tickets/{ticket_id}
@router.post("/")           ──────────────────────────────►  POST /api/v1/tickets/
@router.patch("/{ticket_id}")──────────────────────────────►  PATCH /api/v1/tickets/{ticket_id}
@router.delete("/{ticket_id}")───────────────────────────────►  DELETE /api/v1/tickets/{ticket_id}

@app.get("/health")  (definido DIRECTO en main.py, sin router) ───►  GET /health
```

| Endpoint final | De dónde sale la ruta | De dónde sale el prefijo |
|---|---|---|
| `GET /health` | `@app.get("/health")` en `main.py` | Ninguno — está colgado directo de `app`, nunca pasa por un `router` |
| `GET /api/v1/tickets/` | `@router.get("/")` en `routers/tickets.py` | `/tickets` (del `router`) + `/api/v1` (de `include_router` en `main.py`) |
| `GET /api/v1/tickets/{id}` | `@router.get("/{ticket_id}")` | Igual que arriba |
| `POST /api/v1/tickets/` | `@router.post("/")` | Igual que arriba |
| `PATCH /api/v1/tickets/{id}` | `@router.patch("/{ticket_id}")` | Igual que arriba |
| `DELETE /api/v1/tickets/{id}` | `@router.delete("/{ticket_id}")` | Igual que arriba |

> 💡 Por eso `/health` **no** lleva `/api/v1` — nunca pasó por `include_router`, así que
> nunca recibió ese prefijo. Es una decisión real de diseño: los endpoints de
> infraestructura (*health checks*, métricas) suelen quedar fuera del versionado de la
> API de negocio, porque no son parte del "contrato" que consumen los clientes.

### ✅ Verificado: `/health` responde con el middleware activo

```bash
curl -s -D - http://127.0.0.1:8000/health -o /dev/null
```
```
HTTP/1.1 200 OK
x-process-time: 0.002160
content-type: application/json
```
```bash
curl -s http://127.0.0.1:8000/health
```
```json
{"status":"ok","service":"El API backend de HelpDesk esta operativo","version":"1.0.0"}
```

> 💡 El header `x-process-time` (minúsculas — HTTP no distingue mayúsculas en los
> nombres de header) confirma que el `add_process_time` de arriba corrió — está
> presente en **esta** respuesta y en las 6 de la sección siguiente (Postman/Bruno),
> aunque ninguna de esas capturas lo mencione explícitamente: siempre está.

> 🧪 **Tip de entrevista:** *¿en qué orden corren el middleware y el endpoint?* El
> middleware envuelve al endpoint por los dos lados: todo lo que está **antes** de
> `call_next(request)` corre antes que el endpoint (acá, arrancar el cronómetro), y
> todo lo que está **después** corre una vez que el endpoint ya respondió (agregar el
> header) — mismo mecanismo explicado en la [Clase 3](Clase-03.md).

## 🐘 14. Crear las tablas con Alembic (migraciones versionadas)

### 🧭 ¿Qué es Alembic?

**Alembic es "git, pero para el esquema de la base de datos".** Cada cambio de
estructura (crear una tabla, agregar una columna, cambiar un tipo) queda guardado como
un **archivo de migración** propio, encadenado al anterior — igual que un commit. Eso
permite:

- **Aplicar** los cambios en orden (`alembic upgrade head`), en cualquier máquina (tu
  Mac, un servidor de producción) y que termine con el mismo esquema.
- **Revertir** un cambio puntual (`alembic downgrade -1`) sin tener que borrar la base
  entera y reconstruirla.
- **Saber qué versión** de esquema tiene una base en un momento dado — lo guarda en la
  tabla `alembic_version` (una fila con el id de la última migración aplicada).

| | `Base.metadata.create_all()` | Alembic |
|---|---|---|
| Qué hace | Crea las tablas que falten, de una sola vez | Aplica cambios **de a uno**, en orden, con historial |
| Si cambiás una columna después | No se entera — hay que borrar y recrear la tabla a mano | Generás una migración nueva (`alembic revision --autogenerate`) que aplica solo ese cambio |
| Para qué sirve | Prototipar rápido en desarrollo | Proyectos reales, con datos que no se pueden perder |

Primer intento: `Base.metadata.create_all(bind=engine)` directo en `main.py`, para que
las tablas se creen solas al arrancar. **Funciona**, pero se reemplaza por **Alembic** —
la forma correcta para un proyecto real, porque versiona cada cambio de esquema por
separado (se puede aplicar o revertir de a uno, con historial), en vez
de crear todo de una sola vez sin dejar rastro.

**Instalación y arranque** (carpeta `migrations/`, no `alembic/` — coincide con la que
ya estaba planeada desde el principio de esta clase):
```bash
pip install alembic
alembic init migrations
```

**`migrations/env.py`** — hay que editarlo a mano después del `init` (por defecto no
sabe nada de nuestros modelos ni de nuestro `.env`). Completo, con comentarios en
español explicando cada parte:

```python
# 02-Ejercicios/Clase-04/app/migrations/env.py
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Nuestros modelos: hace falta importar los 3 (mismo motivo que en
# main.py) para que Base.metadata sepa que existen las 3 tablas.
from core.config import settings
from db.database import Base
from models.user import User
from models.category import Category
from models.ticket import Ticket

# Este es el objeto de configuración de Alembic — da acceso a los
# valores del archivo alembic.ini que se está usando.
config = context.config

# Usa la misma DATABASE_URL del .env (core/config.py) en vez de la que
# viene hardcodeada en alembic.ini — una sola fuente de verdad. Así no
# hay que mantener la URL de conexión escrita en dos lugares distintos.
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpreta el archivo de configuración para el logging de Python.
# Esta línea deja armados los loggers (root, sqlalchemy, alembic).
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── target_metadata: el corazón de "autogenerate" ──────────────────
#
# target_metadata = Base.metadata
#
# Base.metadata es un objeto MetaData de SQLAlchemy — un catálogo que
# se va llenando solo, a medida que cada class Modelo(Base) se
# ejecuta (User, Category, Ticket). Ahí queda registrado el nombre de
# cada tabla, sus columnas, tipos y FK.
#
# Al asignarlo acá como target_metadata, le decimos a Alembic:
# "esto es lo que el esquema DEBERÍA ser". Cuando corrés
# `alembic revision --autogenerate`, Alembic compara ese "debería
# ser" (target_metadata) contra lo que la base de datos REALMENTE
# tiene en este momento, y genera automáticamente el script de
# migración con la diferencia (crear una tabla, agregar una columna,
# etc.) — sin este import, Alembic no tendría con qué comparar y
# `--autogenerate` no generaría nada.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Corre las migraciones en modo 'offline'.

    Acá se configura el contexto solo con una URL (sin abrir una
    conexión/Engine real) — sirve para generar el SQL de la migración
    como texto, sin necesitar el driver de la base de datos instalado.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Corre las migraciones en modo 'online' (el que usamos acá).

    Este es el modo real: abre una conexión (Engine) de verdad contra
    Postgres y aplica la migración en una transacción.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


# Alembic decide solo qué modo usar según cómo se lo invoque
# (`alembic upgrade head` corre siempre en modo online).
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

> ⚠️ **Ojo con copiar el `env.py` de otra persona/entorno:** si el material del curso (u
> otro tutorial) tiene su proyecto armado con `app` como paquete real, esa versión va a decir
> `from app.db.database import Base`, `from app.models.user import User`, etc. Pegar
> eso tal cual en este proyecto tira `ModuleNotFoundError: No module named 'app'` —
> mismo error que ya vimos en `repositories/`, `services/` y acá también. Usá siempre
> `from db.database import Base` / `from models.user import User` (sin `app.`), como
> en el resto de archivos de este proyecto.

**Generar y aplicar la primera migración:**
```bash
# Compara los modelos (target_metadata) contra la base real y genera
# el script de migración con la diferencia (acá: crear las 3 tablas)
alembic revision --autogenerate -m "crea tablas users, categories y tickets"

# Aplica esa migración de verdad contra Postgres
alembic upgrade head
```

Verificado contra `curso-postgres`: además de `users`/`categories`/`tickets`, Alembic
crea una tabla propia, **`alembic_version`**, que guarda **cuál** migración está
aplicada — así sabe si hay que aplicar algo nuevo o no la próxima vez.

> ⚠️ **Mismo motivo que con `create_all()`:** hay que importar los 3 modelos en
> `env.py` (no alcanza con el `TYPE_CHECKING` de los modelos) — si no,
> `target_metadata` no sabe que `users`/`categories`/`tickets` deberían existir, y
> `--autogenerate` no genera nada.

> 🧪 **Tip de entrevista:** *¿Qué pasa si dos personas del equipo cambian el esquema al
> mismo tiempo?* Cada `alembic revision` queda encadenada a la anterior (como commits
> de git) — si dos migraciones parten del mismo punto, Alembic detecta el conflicto
> (dos "heads") y hay que resolverlo a mano, igual que un merge conflict.

`main.py` ya **no** llama a `create_all()` — las tablas se crean/actualizan corriendo
`alembic upgrade head` antes de levantar el server.

### 🔍 Cómo se genera el `CREATE TABLE` sin escribir SQL (los 3 momentos)

Es la parte que más parece magia la primera vez: **nadie tipea `CREATE TABLE tickets
(...)` en ningún lado**, y sin embargo la tabla aparece en Postgres. En realidad pasan
**3 momentos separados**, cada uno con una responsabilidad distinta:

```
① MODELOS (Python, en memoria)      ② AUTOGENERATE (compara y ESCRIBE código)      ③ UPGRADE (EJECUTA de verdad)
──────────────────────────────      ────────────────────────────────────────      ──────────────────────────────
models/ticket.py                    alembic revision --autogenerate               alembic upgrade head
class Ticket(Base):                          │                                              │
    id: Mapped[int] = ...           Compara Base.metadata (①)                     env.py abre una conexión
    title: Mapped[str] = ...        vs. lo que Postgres tiene                      REAL (engine_from_config)
    ...                             REALMENTE en este momento                      y corre el archivo de ②
        │                                    │                                              │
        ▼                                    ▼                                              ▼
Se registra SOLO en              Escribe migrations/versions/*.py             Alembic traduce cada
Base.metadata (db/database.py)   con Python — op.create_table(...)            op.create_table(...) al
NINGÚN SQL corrió todavía         AÚN NINGÚN SQL corrió                        SQL real del dialecto de
                                                                                Postgres, y LO EJECUTA
```

| Momento | Comando/archivo | Qué produce | ¿Toca la base de datos? |
|---|---|---|---|
| ① Los modelos se registran | Se importan `User`, `Category`, `Ticket` (en `main.py` y `migrations/env.py`) | `Base.metadata` queda "lleno" con el esquema que *debería* existir — es puro Python en RAM | ❌ No — nada se conecta ni se ejecuta todavía |
| ② `alembic revision --autogenerate` | Compara `target_metadata` (①) contra la base real, y **escribe** `migrations/versions/520cf642f30a_...py` | Un archivo de **Python**, con llamadas `op.create_table(...)`, `op.add_column(...)`, etc. — no es SQL, es la API de Alembic | ✅ Se conecta **para leer/inspeccionar** el esquema actual, pero no modifica nada |
| ③ `alembic upgrade head` | Ejecuta el archivo de ② dentro de una transacción real | Alembic **traduce** cada `op.create_table(...)` al SQL específico de Postgres (`CREATE TABLE ...`) y lo manda por la conexión | ✅ Sí — acá es donde la tabla se crea de verdad |

```python
# Esto es lo que quedó escrito en el paso ② (migrations/versions/520cf642f30a_...py)
# — Python, no SQL:
op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('priority', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('requester_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
    sa.ForeignKeyConstraint(['requester_id'], ['users.id']),
    sa.PrimaryKeyConstraint('id'),
)
```

> 💡 Recién en el paso ③, cuando `run_migrations_online()` (línea `context.run_migrations()`
> de `env.py`) procesa esa llamada, Alembic la convierte en algo como
> `CREATE TABLE tickets (id SERIAL NOT NULL, title VARCHAR(120) NOT NULL, ...,
> PRIMARY KEY (id), FOREIGN KEY(category_id) REFERENCES categories (id), ...)` y lo
> ejecuta. Ese texto de SQL **no vive escrito en ningún archivo del proyecto** — se arma
> en memoria, en el momento, a partir de `op.create_table(...)` + el dialecto de Postgres.

> 📌 Es exactamente la misma idea de "ORM = traductor Python↔SQL" de la
> [sección 3 de esta clase](#🗄️-3-¿que-es-un-orm) (`class Ticket` → `CREATE TABLE`,
> `Ticket(...)` → `INSERT`), aplicada esta vez al **esquema** (la estructura de las
> tablas) en vez de a los **datos** (las filas). Mismo traductor, dos capas distintas.

> 🧪 **Tip de entrevista:** *¿Por qué el paso ② no modifica la base de datos si ya se
> conecta a ella?* Porque solo hace `SELECT` de metadatos internos de Postgres (qué
> tablas/columnas existen) para poder comparar — es una consulta de **lectura**, nunca
> un `CREATE`/`ALTER`. La escritura real queda reservada exclusivamente al paso ③.

### ✅ Checklist: agregar una tabla (o columna) nueva más adelante

1. Escribir el modelo (`class Comment(Base): ...` en `models/comment.py`, por ejemplo).
2. **Importarlo en `migrations/env.py` y en `main.py`** (mismo motivo siempre:
   `Base.metadata` solo sabe que una tabla existe si su clase se ejecutó — sin el
   `import`, Alembic no se entera de que hay algo nuevo).
3. Generar la migración: `alembic revision --autogenerate -m "crea tabla comments"`.
4. Revisar el archivo que se generó en `migrations/versions/` (autogenerate no es
   perfecto — a veces hay que ajustar algo a mano antes de aplicar).
5. Aplicarla: `alembic upgrade head`.

> 💡 Es el mismo checklist para **cualquier** cambio de esquema, no solo tablas nuevas
> — agregar una columna, cambiar un tipo, agregar un índice: siempre modelo editado +
> importado → `--autogenerate` → revisar → `upgrade head`.

### 🌐 Swagger UI (`/docs`) — no hace falta configurar nada

Corré el proyecto:
```bash
cd 02-Ejercicios/Clase-04/app
source .venv/bin/activate
alembic upgrade head        # crea/actualiza las tablas
uvicorn main:app --reload   # levanta la API
```

### 🔍 Qué dice la terminal cuando corre bien

**`alembic upgrade head`:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

| Línea | Qué significa |
|---|---|
| `Context impl PostgresqlImpl` | Alembic miró la `DATABASE_URL` y detectó que es Postgres — carga el dialecto SQL específico de ese motor |
| `Will assume transactional DDL` | Postgres permite meter `CREATE TABLE`/`ALTER TABLE` **dentro de una transacción** — si la migración falla a mitad de camino, hace `ROLLBACK` y no queda nada a medio aplicar (todo o nada) |

> 📌 Si no dice "creó tal tabla" es porque ya estaban creadas de antes —
> `alembic upgrade head` es **idempotente**: si ya estás en la última migración
> (`head`), no hace nada, solo confirma que no hay pendientes.

Para confirmar que las tablas están de verdad, sin fiarse solo de lo que imprime la
terminal, se consulta Postgres directo:
```bash
docker exec -it curso-postgres psql -U postgres -d curso_backend -c "\dt"
```
```
             List of relations
 Schema |      Name       | Type  |  Owner
--------+------------------+-------+----------
 public | alembic_version  | table | postgres
 public | categories       | table | postgres
 public | tickets          | table | postgres
 public | users            | table | postgres
```
> 💡 `alembic_version` es la tabla que crea el propio Alembic (no un modelo del
> proyecto) — guarda una sola fila con el id de la última migración aplicada, para
> saber la próxima vez si hay algo pendiente o no.

**`uvicorn main:app --reload`:**
```
INFO:     Will watch for changes in these directories: ['.../app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [97042] using WatchFiles
INFO:     Started server process [97045]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

| Línea | Qué significa |
|---|---|
| `Will watch for changes in...` | Por el `--reload`: uvicorn vigila todos los `.py` de esa carpeta con la librería `WatchFiles` |
| `Uvicorn running on http://127.0.0.1:8000` | Tu API ya escucha peticiones — `127.0.0.1` es tu propia Mac (`localhost`), puerto `8000` |
| `Started reloader process [97042]` | Con `--reload`, uvicorn arranca **2 procesos**, no 1: este es el "supervisor" — solo vigila archivos, no atiende peticiones |
| `Started server process [97045]` | Este sí corre tu app de verdad (`main:app`) y responde las peticiones. Cuando guardás un cambio, el reloader mata este proceso y lo levanta de nuevo con el código actualizado — no hace falta reiniciar a mano |
| `Waiting for application startup` | FastAPI ejecuta sus eventos de arranque registrados (acá, ninguno propio más allá del middleware) |
| `Application startup complete` | Terminó de arrancar — recién ahí la API empieza a aceptar peticiones de verdad |

> 💡 **`main:app`** — mismo patrón que `alembic.ini`: `main` es el archivo `main.py`,
> `:app` es la variable `app = FastAPI(...)` que vive adentro. Uvicorn importa ese
> módulo y usa esa variable como la aplicación a correr.

> 📌 **¿Dónde se define el puerto `8000`?** En ningún archivo del proyecto — ni
> `main.py`, ni `core/config.py`, ni `.env` fijan un puerto. Como el comando no lleva
> `--port`, uvicorn usa **su propio valor por defecto** (confirmado con
> `uvicorn --help` en el `.venv` del proyecto): `--host 127.0.0.1` y `--port 8000`. Para
> usar otro: `uvicorn main:app --reload --port 8001`; para exponerlo a otras máquinas de
> la red (no solo tu Mac): sumar `--host 0.0.0.0`.

Y andá a `http://127.0.0.1:8000/docs` — ahí aparece **Swagger UI**, con los 5
endpoints de tickets, cada uno con su formulario para probarlo sin `curl` ni Postman.
**Nadie lo configuró a mano** — FastAPI lo arma solo, leyendo lo que ya escribiste:

| De dónde sale cada cosa en `/docs` | En el código |
|---|---|
| El título "HelpDesk API" y la descripción | `FastAPI(title=..., description=..., version=...)` en `main.py` |
| Cada endpoint listado (`GET /api/v1/tickets/`, `POST /api/v1/tickets/`, ...) | Los `@router.get(...)`, `@router.post(...)` de `routers/tickets.py` |
| Los campos del formulario para "Try it out" (`title`, `priority`, ...) | Los campos de `TicketCreate`/`TicketUpdate` en `schemas/ticket.py` |
| La forma de la respuesta que muestra como ejemplo | `response_model=TicketResponse` de cada endpoint |
| El grupo "Tickets" en el menú | `tags=["Tickets"]` del `APIRouter(...)` |

> 💡 Por qué funciona sin configurarlo: FastAPI genera automáticamente un documento
> **OpenAPI** (`/openapi.json` — un JSON que describe toda tu API: rutas, parámetros,
> schemas) a partir de tus type hints y tus modelos Pydantic. Swagger UI es solo una
> página que **lee ese JSON** y dibuja la interfaz — por eso cualquier cambio en el
> código (agregar un campo, cambiar un tipo) se refleja solo en `/docs`, sin tocar nada
> de documentación a mano.

Los 5 endpoints ya están **verificados end-to-end** contra Postgres real (6 casos de
prueba — `GET /api/v1/tickets/{id}` se probó dos veces: con un id que existe y con uno
que no, para confirmar también el `404`):

| Endpoint | Resultado |
|---|---|
| `POST /api/v1/tickets/` | `201` — crea el ticket |
| `GET /api/v1/tickets/` | `200` — lista todos |
| `GET /api/v1/tickets/{id}` | `200` — trae uno |
| `GET /api/v1/tickets/99999` (no existe) | `404 {"detail": "Ticket no encontrado"}` |
| `PATCH /api/v1/tickets/{id}` | `200` — actualiza solo `priority` |
| `DELETE /api/v1/tickets/{id}` | `204` |

## 🧪 15. Probar los endpoints con Postman o Bruno

Swagger UI (sección anterior) alcanza para probar rápido, pero **Postman** y **Bruno**
son clientes API dedicados: guardan las peticiones en una **colección** reutilizable
(no hay que reescribir el body cada vez), permiten variables (`{{base_url}}`) y
encadenar peticiones (usar el `id` que devolvió un `POST` en el siguiente `GET`).

### 🆚 Postman vs. Bruno — cuál usar

| | Postman | Bruno |
|---|---|---|
| Qué es | El cliente API más usado — cuenta con GUI, cloud, equipos | Alternativa **open source** (MIT), más nueva |
| Dónde guarda la colección | En la nube (workspace de Postman) | **Archivos de texto plano** (`.bru`) en tu propio disco |
| Se puede subir a git | No directo (formato propio en la nube) | **Sí** — es la razón por la que muchos devs lo eligen: la colección versiona junto al código, como cualquier `.py` |
| Cuenta obligatoria | Sí, para sincronizar | No — funciona 100% local y offline |
| Para este curso | Sirve igual, más conocido | Encaja mejor con el espíritu del repo (todo versionado en git) |

> 🔗 Fuente: [Bruno vs Postman 2026 — QASkills](https://qaskills.sh/blog/bruno-vs-postman-api-testing-2026)

### ⚙️ Configuración común a los dos: la variable `base_url`

> 📌 **Qué es Postman, con precisión:** una aplicación de escritorio (también hay
> versión web) que funciona como **cliente HTTP con memoria** — arma la misma petición
> que haría `curl` (método, URL, headers, body), pero la **guarda** organizada en
> *Collections* (carpetas de peticiones relacionadas, como la `REST API basics: CRUD,
> test & variables` de las capturas) y en *Environments* (juegos de variables, como
> `{{base_url}}`, que cambian según dónde corra la API — local, staging, producción —
> sin tocar las peticiones guardadas).

En vez de escribir `http://127.0.0.1:8000/api/v1` en cada petición, se crea **una
variable de entorno** (`base_url`) y las peticiones usan `{{base_url}}/tickets`. Si el
día de mañana cambia el puerto o se despliega en un servidor real, se edita **un solo
lugar** en vez de cada petición guardada.

| Cliente | Dónde se crea | Cómo se usa en una petición |
|---|---|---|
| Postman | ⚙️ *Environments* → *New Environment* → variable `base_url` = `http://127.0.0.1:8000/api/v1` | URL de la petición: `{{base_url}}/tickets` |
| Bruno | Ícono de engranaje de la colección → *Variables* → `base_url` = `http://127.0.0.1:8000/api/v1` | Igual sintaxis: `{{base_url}}/tickets` |

#### 🖱️ Cómo se hizo en Postman (capturas propias)

**1) Crear el Environment** — botón `+` de la barra lateral → `Environment` (no
`Collection`, que es para agrupar peticiones, ni `HTTP`, que es para una petición
suelta). Se lo nombró `Clase4`:

![Postman: menú "+" de la barra lateral con la opción Environment resaltada, y a la izquierda la colección "REST API basics" con la petición GET Get data, y el Environment "Clase4" ya creado](/clase-04-postman-nuevo-environment.png)

**2) Cargar la variable `base_url`** — adentro del Environment `Clase4`, en la tabla
`Variable` / `Value`:

![Postman: editor del Environment "Clase4" con la variable base_url cargada, valor http://127.0.0.1:8000/api/v1](/clase-04-postman-environment-variables.png)

> ✅ `base_url` = `http://127.0.0.1:8000/api/v1` — exactamente la URL base verificada
> con `curl` en la sección anterior (sección 13, `main.py`). De acá en adelante,
> **cualquier** petición de la colección puede usar `{{base_url}}/tickets` en vez de
> repetir la URL completa.

![Postman: fila de la variable base_url con el checkbox a la izquierda marcado (activo)](/clase-04-postman-variable-checkbox-activo.png)

> ⚠️ El **checkbox** a la izquierda de cada variable (✅ en la captura) es un segundo
> interruptor, aparte de tener el Environment seleccionado como activo: una variable
> con el checkbox **destildado** queda guardada en la tabla pero Postman la trata como
> si no existiera — mismo síntoma que el de abajo (`{{base_url}}` sin resolver), es un
> segundo lugar donde revisar si algo no funciona.

> ⚠️ Con el Environment creado pero sin seleccionarlo activo (dropdown arriba a la
> derecha de Postman, al lado del ícono del ojo), `{{base_url}}` en una petición queda
> **sin resolver** — Postman manda literal el texto `{{base_url}}/tickets` y la API
> responde error, no la URL real.

> 💡 **Bruno queda pendiente** — mismo procedimiento (crear el equivalente a un
> Environment y cargar `base_url`), se agregan las capturas cuando estén.

### 📋 Los 5 endpoints — probados de verdad contra `curso-postgres`

Cada fila está **verificada con `curl` real** contra el servidor corriendo (no
inventada) — el mismo request/response que vas a ver en Postman/Bruno:

**1) `POST {{base_url}}/tickets/` — crear un ticket**
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/tickets/ \
  -H "Content-Type: application/json" \
  -d '{"title":"No carga el dashboard","description":"El dashboard principal no carga desde ayer","priority":"Alta","requester_id":1,"category_id":1}'
```
```
201 Created
{"id":3,"title":"No carga el dashboard","description":"El dashboard principal no carga desde ayer","priority":"Alta","requester_id":1,"category_id":1}
```

**2) `GET {{base_url}}/tickets/` — listar todos**
```bash
curl -s http://127.0.0.1:8000/api/v1/tickets/
```
```
200 OK
[{"id":1,"title":"Falla de VPN", ...}, {"id":2,"title":"Lentitud del wifi", ...}, {"id":3,"title":"No carga el dashboard", ...}]
```

**3) `GET {{base_url}}/tickets/3` — traer uno por id**
```bash
curl -s http://127.0.0.1:8000/api/v1/tickets/3
```
```
200 OK
{"id":3,"title":"No carga el dashboard","description":"El dashboard principal no carga desde ayer","priority":"Alta","requester_id":1,"category_id":1}
```

**4) `GET {{base_url}}/tickets/99999` — id que no existe**
```bash
curl -s http://127.0.0.1:8000/api/v1/tickets/99999
```
```
404 Not Found
{"detail":"Ticket no encontrado"}
```

**5) `PATCH {{base_url}}/tickets/3` — actualizar solo `priority`**
```bash
curl -s -X PATCH http://127.0.0.1:8000/api/v1/tickets/3 \
  -H "Content-Type: application/json" \
  -d '{"priority":"Cerrado"}'
```
```
200 OK
{"id":3,"title":"No carga el dashboard","description":"El dashboard principal no carga desde ayer","priority":"Cerrado","requester_id":1,"category_id":1}
```
> 💡 Solo cambió `priority` — `title`/`description` quedaron intactos, porque
> `TicketUpdate` (sección 8) tiene todos los campos opcionales y el repositorio
> (sección 10) actualiza únicamente lo que vino en el body (`exclude_unset=True`).

**6) `DELETE {{base_url}}/tickets/3` — borrar**
```bash
curl -s -X DELETE http://127.0.0.1:8000/api/v1/tickets/3
```
```
204 No Content
(sin body)
```

### 🖱️ Armar la petición en Postman/Bruno (en vez de `curl`)

Cada `curl` de arriba se arma en la GUI así — mismos 4 datos en los dos clientes:

| Dato del `curl` | Dónde va en Postman/Bruno |
|---|---|
| `-X POST` / `-X PATCH` / `-X DELETE` (o nada = `GET`) | El selector de **método** al lado de la URL |
| La URL (`http://127.0.0.1:8000/api/v1/tickets/...`) | La barra de **URL** — usando `{{base_url}}/tickets/...` |
| `-H "Content-Type: application/json"` | Pestaña **Headers** (Postman/Bruno lo agregan solos al elegir body tipo JSON) |
| `-d '{...}'` | Pestaña **Body** → tipo `JSON` (Postman) / `Json` (Bruno) → pegar el mismo objeto |

> ⚠️ Error común: mandar el body como texto plano sin marcar el tipo `JSON` en la
> pestaña Body — ahí FastAPI no lo reconoce como JSON válido y responde `422`, aunque el
> texto tenga la forma correcta.

> 🧪 **Tip de entrevista:** *¿por qué versionar la colección de Postman/Bruno junto con
> el código?* Así cualquiera que clona el repo (o un futuro yo) tiene **de una** las
> peticiones ya armadas y probadas, sin tener que reconstruirlas leyendo `routers/` —
> mismo espíritu que documentar los 5 endpoints acá, en la nota de la clase.

## 🐞 Errores de esta clase (con solución)

Documentados en detalle en `06-Errores/`:

| Error | Causa | Nota |
|---|---|---|
| `zsh: command not found: python` | En macOS es `python3`, no `python` | [ver](../06-Errores/2026-08-11-python-command-not-found.md) |
| `zsh: command not found: pip` | El `.venv` no estaba activado en esa terminal | [ver](../06-Errores/2026-08-11-pip-command-not-found-venv-inactivo.md) |
| Pylance: *"No se ha podido resolver la importación pydantic"* | VS Code usaba otro intérprete de Python, no el `.venv` del proyecto | [ver](../06-Errores/2026-08-11-pylance-no-resuelve-import-pydantic.md) |
| Pylance: *"Ticket no está definido"* en una `relationship` | Referencia diferida (`"Ticket"` entre comillas) sin el `TYPE_CHECKING` que le explique a Pylance qué es | [ver](../06-Errores/2026-08-11-pylance-forward-reference-no-definido.md) |
| `SyntaxError: Perhaps you forgot a comma?` en `mapped_column(...)` | Faltaba coma entre argumentos + orden invertido (posicional después del nombrado) | [ver](../06-Errores/2026-08-11-syntaxerror-falta-coma-mapped-column.md) |
| `ImportError: cannot import name 'create_engine' from 'sqlalchemy.orm'` | `create_engine` vive en `sqlalchemy`, no en `sqlalchemy.orm` | [ver](../06-Errores/2026-08-11-importerror-create-engine-sqlalchemy-orm.md) |
| `Settings()` no encuentra `database_url` | Faltaba instalar `pydantic-settings` (paquete aparte de `pydantic`) y crear el `.env` | [ver](../06-Errores/2026-08-11-pydantic-settings-y-env-faltantes.md) |
| `ModuleNotFoundError: No module named 'app'` | Imports con prefijo `app.` (`from app.models...`) que no existe en este proyecto — se corre desde adentro de `app/` | [ver](../06-Errores/2026-08-11-modulenotfounderror-app-prefix.md) |
| `InvalidRequestError: expression 'User' failed to locate a name` | `User`/`Category` nunca se habían importado de verdad (el `TYPE_CHECKING` no cuenta) antes de crear un `Ticket` | [ver](../06-Errores/2026-08-11-invalidrequesterror-relationship-no-resuelve.md) |
| `500 Internal Server Error` en `POST /tickets/` (Postman) | `requester_id`/`category_id` apuntaban a un `user`/`category` que no existía — tablas vacías recién migradas, y nadie captura el `IntegrityError` de la FK | [ver](../06-Errores/2026-08-12-500-foreign-key-inexistente-sin-datos-previos.md) |

> 📝 **Sobre `__init__.py` y `__pycache__`:** terminamos borrando **todos** los
> `__init__.py` del proyecto (`core/`, `db/`, `models/`, `repositories/`, `routers/`,
> `schemas/`, `services/`) — se verificó que los imports siguen funcionando igual sin
> ellos, porque Python 3.3+ ya no los exige ("paquetes de espacio de nombres
> implícitos"). `__pycache__/` es distinto: lo genera Python **solo**, automáticamente,
> cada vez que corrés el proyecto — se puede borrar, pero vuelve a aparecer solo; ya
> está excluido de git en `.gitignore`, así que nunca ensucia el repo aunque reaparezca
> en el explorador de archivos.

## 🏋️ Ejercicios con solución

> Reutilizan el laboratorio real de esta clase (`02-Ejercicios/Clase-04/app/`: modelos
> `User`/`Category`/`Ticket`, `TicketRepository`, `TicketService`, `routers/tickets.py`)
> — cada solución se verificó corriendo de verdad contra `curso-postgres`.

### Ejercicio 1 — Schema de Pydantic para `Category`

`schemas/ticket.py` ya tiene `TicketCreate`/`TicketResponse`. Escribí el mismo patrón
pero para categorías: un schema `CategoryCreate` con un único campo `name` (obligatorio,
entre 3 y 100 caracteres) y un schema `CategoryResponse` que devuelva `id` y `name`,
preparado para leer directo de un objeto ORM (no solo de un `dict`).

<details><summary>💡 ¿Sabías que…? — Field(min_length=...) y ConfigDict(from_attributes=True)</summary>

`Field(min_length=..., max_length=...)` valida la longitud de un `str` sin escribir un
`if` a mano — si no se cumple, Pydantic responde error 422 solo. Y `model_config =
ConfigDict(from_attributes=True)` es lo que le permite a un schema de respuesta leer
atributos de un objeto ORM (`producto.nombre`), no solo claves de un `dict`
(`producto["nombre"]`) — sin eso, Pydantic v2 no sabe convertir un objeto SQLAlchemy.

```python
# Ejemplo de referencia — otro dominio, misma idea
from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    sku: str = Field(min_length=4, max_length=20)

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sku: str
```
</details>

<details><summary>Ver solución</summary>

```python
from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
```
</details>

### Ejercicio 2 — Campo opcional en un modelo SQLAlchemy

Al modelo `Ticket` (`models/ticket.py`) le falta un campo para registrar **cuándo se
cerró** el ticket. Agregale una columna `closed_at`, de tipo fecha/hora, que **puede
quedar vacía** (un ticket recién creado todavía no se cerró) — sin usar `Field` de
Pydantic, esto es SQLAlchemy puro, en el modelo.

<details><summary>💡 ¿Sabías que…? — Mapped[X | None] y default=None</summary>

En el estilo tipado de SQLAlchemy 2.0, un campo que puede ser `NULL` en la base de
datos se anota como `Mapped[tipo | None]` (el mismo `str | None` que ya viste en
`TicketUpdate`, aplicado ahora a una columna real). `default=None` es el valor que toma
en Python antes de guardarse; `nullable=True` es lo que le dice a **Postgres** que
acepte `NULL` en esa columna — son dos cosas relacionadas pero distintas (una es de
Python/SQLAlchemy, la otra es la restricción real en la base).

```python
# Ejemplo de referencia — otro campo opcional, distinto dominio
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    hired_on: Mapped[date] = mapped_column(Date, nullable=False)
    left_on: Mapped[date | None] = mapped_column(Date, nullable=True, default=None)
```
</details>

<details><summary>Ver solución</summary>

```python
from datetime import datetime
from sqlalchemy import DateTime

# ... en la clase Ticket, junto al resto de columnas:
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )
```
</details>

### Ejercicio 3 — Filtrar tickets por prioridad con `select().where()`

Escribí una función `get_by_priority(db, priority)` que devuelva **solo** los tickets
que tengan la prioridad exacta que se le pasa (ej. `"Alta"`), usando `select()` — el
mismo estilo que ya usa `TicketRepository.get_all`, pero con un filtro.

<details><summary>💡 ¿Sabías que…? — .where() se encadena igual que .order_by()</summary>

`select(Modelo)` devuelve un objeto `Select` que se puede seguir encadenando con más
métodos (`.where(...)`, `.order_by(...)`, `.limit(...)`) antes de ejecutarlo — ninguno
dispara la consulta por sí solo (evaluación diferida, ya visto con `statement`). Recién
`db.scalars(...)` lo ejecuta de verdad.

```python
# Ejemplo de referencia — filtrar por otro campo, distinto dominio
def get_active_employees(db: Session) -> list[Employee]:
    statement = select(Employee).where(Employee.left_on.is_(None))
    return list(db.scalars(statement).all())
```
</details>

<details><summary>Ver solución</summary>

```python
def get_by_priority(self, db: Session, priority: str) -> list[Ticket]:
    statement = select(Ticket).where(Ticket.priority == priority)
    return list(db.scalars(statement).all())
```
</details>

### Ejercicio 4 — `CategoryRepository`

`repositories/ticket_repository.py` ya existe. Escribí `CategoryRepository` con el
mismo patrón: `get_all` (todas las categorías, ordenadas por id), `get_by_id`, `create`
(recibe solo el `name`) y `delete`.

<details><summary>💡 ¿Sabías que…? — el repository no sabe nada de HTTP ni de reglas de negocio</summary>

El repository es **CRUD puro**: abre/usa la sesión, ejecuta la consulta, devuelve el
objeto. No valida nada de negocio (eso es trabajo del `service`, ejercicio 6) ni sabe
qué es un `HTTPException` (eso es trabajo del `router`). Cuanto más "aburrido" y
predecible sea un repository, mejor diseñado está.

```python
# Ejemplo de referencia — mismo patrón, otro dominio
class ProductRepository:
    def get_all(self, db: Session) -> list[Product]:
        return list(db.scalars(select(Product).order_by(Product.id)).all())

    def create(self, db: Session, sku: str) -> Product:
        product = Product(sku=sku)
        db.add(product); db.commit(); db.refresh(product)
        return product
```
</details>

<details><summary>Ver solución</summary>

```python
class CategoryRepository:
    def get_all(self, db: Session) -> list[Category]:
        statement = select(Category).order_by(Category.id)
        return list(db.scalars(statement).all())

    def get_by_id(self, db: Session, category_id: int) -> Category | None:
        return db.get(Category, category_id)

    def create(self, db: Session, name: str) -> Category:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def delete(self, db: Session, category: Category) -> None:
        db.delete(category)
        db.commit()
```
</details>

### Ejercicio 5 — Tickets junto con el nombre de su categoría (`JOIN`)

Escribí una función que traiga, para cada ticket, su `title` **y** el `name` de la
categoría a la que pertenece — en una sola consulta, con `JOIN`, sin usar la
`relationship()` (`ticket.category.name`); esta vez a mano, con `select(...).join(...)`.

<details><summary>💡 ¿Sabías que…? — seleccionar columnas puntuales, no el objeto entero</summary>

`select(Ticket)` trae objetos `Ticket` completos. `select(Ticket.title, Category.name)`
trae solo esas 2 columnas, como tuplas — más liviano cuando no hace falta el objeto
entero. `.join(Otro, condición)` es exactamente el `ON` del `JOIN` de SQL, escrito en
Python.

```python
# Ejemplo de referencia — otro JOIN, distinto dominio
statement = (
    select(Order.id, Customer.name)
    .join(Customer, Order.customer_id == Customer.id)
)
```
</details>

<details><summary>Ver solución</summary>

```python
def tickets_con_categoria(db: Session) -> list[tuple[str, str]]:
    statement = (
        select(Ticket.title, Category.name)
        .join(Category, Ticket.category_id == Category.id)
        .order_by(Ticket.id)
    )
    return list(db.execute(statement).all())
```
</details>

### Ejercicio 6 — `CategoryService` que evita nombres duplicados

Antes de crear una categoría, el `service` tiene que revisar si ya existe una con ese
mismo `name` — si existe, corta con un error (código HTTP 409, "Conflict") en vez de
guardar un duplicado.

<details><summary>💡 ¿Sabías que…? — 409 es el código correcto para un duplicado</summary>

`404` es "no encontrado", `422` es "la validación de los campos falló" (eso ya lo hace
Pydantic solo). Para "esto ya existe y no se puede repetir" el código HTTP correcto es
**409 Conflict** — distinto tipo de problema, distinto código, para que el cliente de
la API pueda reaccionar distinto ante cada uno.

```python
# Ejemplo de referencia — misma idea, otro dominio
class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(self, db: Session, sku: str) -> Product:
        if self.repository.get_by_sku(db, sku) is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, f"SKU {sku!r} ya existe")
        return self.repository.create(db, sku)
```
</details>

<details><summary>Ver solución</summary>

```python
# En CategoryRepository, agregar:
def get_by_name(self, db: Session, name: str) -> Category | None:
    statement = select(Category).where(Category.name == name)
    return db.scalars(statement).first()

# CategoryService:
class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create_category(self, db: Session, name: str) -> Category:
        existente = self.repository.get_by_name(db, name)
        if existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría llamada {name!r}",
            )
        return self.repository.create(db, name)
```
</details>

### Ejercicio 7 — Router de categorías

Montá un `APIRouter` con prefijo `/categories` y 2 endpoints: `GET /categories/` (lista
todas) y `POST /categories/` (crea una) — mismo patrón que `routers/tickets.py`, con
`Depends(get_db)` para la sesión.

<details><summary>💡 ¿Sabías que…? — response_model filtra lo que se devuelve, aunque el objeto tenga más</summary>

Si el `Category` del ORM tuviera, hipotéticamente, un campo interno que no querés
exponer, `response_model=CategoryResponse` lo filtraría solo — FastAPI arma la
respuesta a partir de los campos que **el schema** declara, no de todos los que tiene
el objeto que le pasaste.

```python
# Ejemplo de referencia — mismo patrón, otro dominio
router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return ProductRepository().get_all(db)
```
</details>

<details><summary>Ver solución</summary>

```python
router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_repository() -> CategoryRepository:
    return CategoryRepository()

@router.get("/", response_model=list[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    repo: CategoryRepository = Depends(get_category_repository),
):
    return repo.get_all(db)

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    repo: CategoryRepository = Depends(get_category_repository),
):
    return repo.create(db, data.name)
```
</details>

### Ejercicio 8 — Migración de Alembic para `closed_at`

Con el campo del ejercicio 2 ya agregado al modelo, generá la migración con
`--autogenerate` y aplicala contra Postgres. Indicá los 2 comandos, en orden.

<details><summary>💡 ¿Sabías que…? — autogenerate compara, no adivina</summary>

`--autogenerate` no "inventa" el cambio — compara `target_metadata` (lo que los
modelos dicen que debería existir) contra lo que Postgres tiene ahora mismo, columna
por columna, y escribe el script con la diferencia exacta. Si el modelo no se
modificó, no genera nada nuevo.

```bash
# Ejemplo de referencia — mismo comando, otro cambio (agregar una columna a users)
alembic revision --autogenerate -m "agrega phone a users"
alembic upgrade head
```
</details>

<details><summary>Ver solución</summary>

```bash
alembic revision --autogenerate -m "agrega closed_at a tickets"
alembic upgrade head
```

Verificado: `alembic revision --autogenerate` detectó `Detected added column
'tickets.closed_at'` solo, y `alembic upgrade head` la aplicó de verdad contra
`curso-postgres` (columna confirmada con `\d tickets` en `psql`, después revertida con
`alembic downgrade -1` para no dejarla en el proyecto real).
</details>

### Ejercicio 9 — Filtrar tickets por prioridad desde la URL (query param)

Modificá `GET /tickets/` para que acepte un parámetro opcional en la URL,
`?priority=Alta`, y devuelva solo los tickets de esa prioridad — si no se manda el
parámetro, devuelve todos, como hasta ahora.

<details><summary>💡 ¿Sabías que…? — un parámetro con default es automáticamente un query param</summary>

En FastAPI, un parámetro de la función que **no** aparece en la ruta (`"/tickets2/"`,
sin `{algo}`) y tiene un valor por defecto se toma solo como *query parameter* — no
hace falta ningún decorador extra. `priority: str | None = None` ya alcanza para que
FastAPI lo lea de `?priority=...`.

```python
# Ejemplo de referencia — mismo patrón, otro campo
@router.get("/", response_model=list[ProductResponse])
def list_products(category: str | None = None, db: Session = Depends(get_db)):
    statement = select(Product)
    if category is not None:
        statement = statement.where(Product.category == category)
    return list(db.scalars(statement).all())
```
</details>

<details><summary>Ver solución</summary>

```python
@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    priority: str | None = None,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    statement = select(Ticket)
    if priority is not None:
        statement = statement.where(Ticket.priority == priority)
    return list(db.scalars(statement.order_by(Ticket.id)).all())
```
</details>

### Ejercicio 10 — Flujo completo: crear, actualizar y confirmar un ticket

Usando `TestClient` (sin abrir el navegador), escribí un script que: 1) cree un ticket
nuevo con `POST`, 2) le cambie la `priority` con `PATCH`, 3) lo vuelva a pedir con `GET`
y confirme que el cambio quedó guardado de verdad.

<details><summary>💡 ¿Sabías que…? — TestClient no necesita uvicorn corriendo</summary>

`TestClient(app)` simula peticiones HTTP directo contra tu app de FastAPI, en el mismo
proceso de Python — no hace falta tener `uvicorn main:app` corriendo aparte. Es lo que
se usa para escribir tests automatizados de una API.

```python
# Ejemplo de referencia — mismo patrón, otro flujo
client = TestClient(app)
r1 = client.post("/products/", json={"sku": "ABC-123"})
r2 = client.get(f"/products/{r1.json()['id']}")
assert r2.json()["sku"] == "ABC-123"
```
</details>

<details><summary>Ver solución</summary>

```python
from fastapi.testclient import TestClient

client = TestClient(app)

# 1. Crear
r1 = client.post("/tickets/", json={
    "title": "Impresora atascada",
    "description": "La impresora del piso 2 no imprime",
    "requester_id": 1,
    "category_id": 1,
})
ticket_id = r1.json()["id"]

# 2. Actualizar
r2 = client.patch(f"/tickets/{ticket_id}", json={"priority": "Baja"})

# 3. Confirmar
r3 = client.get(f"/tickets/{ticket_id}")
assert r3.json()["priority"] == "Baja"
```

Verificado end-to-end contra `curso-postgres`: `POST` → `201`, `PATCH` → `200` con
`priority: "Baja"`, `GET` final confirma el mismo valor guardado.
</details>

## ❓ Preguntas y respuestas (autoevaluación)

**1. ¿Qué es la persistencia de datos, y por qué una lista de Python no alcanza?**
> Es la capacidad de un dato de sobrevivir a la ejecución del programa que lo creó. Una
> variable en RAM desaparece apenas termina el proceso; un backend real necesita que
> los datos sigan existiendo después de reiniciar el servidor o entre distintas
> instancias — para eso hace falta un medio persistente y compartido, como PostgreSQL.

**2. ¿Qué es un ORM, en una frase?**
> La capa que traduce entre dos mundos: clases/objetos de Python y tablas/filas de una
> base de datos relacional — permite modelar los datos como clases y manipularlos como
> objetos, mientras el ORM genera el SQL correspondiente por debajo.

**3. ¿Por qué `schemas/ticket.py` tiene 3 clases (`TicketCreate`, `TicketUpdate`,
`TicketResponse`) en vez de una sola?**
> Porque cada una valida un contrato distinto de la API: `Create` es lo que el cliente
> manda al crear (sin `id`), `Update` tiene todos los campos opcionales (actualización
> parcial), y `Response` es lo que la API devuelve (sí trae `id`, sin las validaciones
> de longitud que ya se aplicaron al crear).

**4. ¿Cuál es la diferencia entre `ForeignKey(...)` y `relationship(...)` en un modelo?**
> `ForeignKey` es una restricción real que impone Postgres a nivel de base de datos
> (esta columna solo puede apuntar a una fila que exista en la otra tabla).
> `relationship()` es una comodidad de Python/SQLAlchemy: le permite navegar el objeto
> relacionado (`ticket.requester.name`) sin escribir el `JOIN` a mano.

**5. ¿Por qué los modelos usan `if TYPE_CHECKING:` para importar entre sí?**
> Porque `User` y `Ticket` (y `Category` y `Ticket`) se referencian mutuamente — si se
> importaran de forma normal se armaría un import circular y Python no arrancaría.
> `TYPE_CHECKING` vale `False` en tiempo real (ese import nunca se ejecuta), pero
> Pylance/mypy sí lo leen para entender los tipos.

**6. ¿Para qué sirve el Repository Pattern si ya existe el ORM?**
> Para aislar el resto de la app (`services/`, `routers/`) de los detalles de
> SQLAlchemy — si mañana cambia el ORM o el motor de base de datos, solo hay que tocar
> `repositories/`, el resto del código no se entera.

**7. ¿Qué diferencia hay entre `TicketRepository` y `TicketService`?**
> El repository es CRUD puro (lee/escribe, sin opinión). El service es la capa de
> arriba: aplica reglas de negocio (por ejemplo, lanzar un `404` si el ticket no
> existe) y es lo único que el router debería llamar directamente.

**8. ¿Cuándo se ejecuta de verdad un `statement` de SQLAlchemy?**
> `select(Ticket).where(...)` solo arma un objeto que describe la consulta — no toca la
> base de datos. Recién cuando ese `statement` se le pasa a `db.scalars(...)` o
> `db.execute(...)`, la sesión lo traduce a SQL real y lo ejecuta contra Postgres
> (evaluación diferida).

**9. ¿Por qué usar Alembic en vez de `Base.metadata.create_all()`?**
> `create_all()` crea las tablas que falten de una sola vez, sin historial — si después
> cambia una columna, no se entera. Alembic versiona cada cambio de esquema por
> separado (como commits de git): se puede aplicar (`upgrade`) o revertir
> (`downgrade`) de a uno, y siempre se sabe en qué versión de esquema está la base.

**10. ¿Por qué aparece Swagger UI en `/docs` sin haberlo configurado?**
> FastAPI genera automáticamente un documento OpenAPI (`/openapi.json`) a partir de los
> type hints y los modelos Pydantic del proyecto — Swagger UI es solo una página que lee
> ese JSON y dibuja la interfaz. Por eso cualquier cambio en el código se refleja solo
> en `/docs`, sin tocar documentación a mano.

## 📎 Apuntes relacionados

- [00-Notas/02-Conceptos.md](../00-Notas/02-Conceptos.md) — concepto "Import de
  librería vs. nombre de tu archivo" (por qué `Session` no depende de cómo se llame
  `db/database.py`).
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md) — comandos de `pip`, Docker y
  `python3 -m pip install`, usados en toda esta clase.
- [00-Notas/05-Estructura-Proyecto-FastAPI.md](../00-Notas/05-Estructura-Proyecto-FastAPI.md)
  — versión genérica y reutilizable de la arquitectura por capas de esta clase.
- `06-Errores/` — los 9 errores documentados en esta clase (`python`/`pip` no
  encontrados, imports con `app.`, Pylance con referencias diferidas, `SyntaxError`,
  `ImportError` de `create_engine`, `pydantic-settings`/`.env` faltantes,
  `InvalidRequestError` de relaciones no resueltas).
- [Clase 3](Clase-03.md) — teoría de FastAPI, Pydantic y Swagger/OpenAPI, base para la
  capa API de esta clase.
- [Clase 1 — mutabilidad y aliasing](Clase-01.md#🧬-9-mutabilidad-y-aliasing-el-bug-mas-comun-en-backend)
  — mismo concepto de identidad de objetos que aparece con `self` y las instancias de
  `TicketRepository`.

## ➡️ Siguiente
[Clase 5](Clase-05.md)
