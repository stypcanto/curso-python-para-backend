---
sidebar: "🖥️ Comandos"
---

# 🖥️ Comandos — Python para Backend

> Comandos de terminal, Python, pip, entornos virtuales, etc. que voy usando en el curso.

Comandos que **cambian según el sistema operativo** (crear/activar el venv). Styp usa
macOS — esa es la columna que realmente corre en su terminal:

| Qué hace | 🍎 macOS/Linux (el que usa Styp) | 🪟 Windows (referencia) |
|---|---|---|
| Crear el entorno virtual | `python3 -m venv .venv` | `python -m venv .venv` |
| Activarlo | `source .venv/bin/activate` | `.\.venv\Scripts\activate` |
| Ver la versión de Python | `python3 --version` | `python --version` |

> 📝 En macOS el binario se llama **`python3`**, no `python` a secas (no viene instalado
> por defecto) — ver [[python-command-not-found]]. En Windows sí existe `python` sin el
> "3". Una vez con el venv **activado**, en ambos sistemas ya se puede usar `python` (a
> secas) y `pip` sin el "3" — el venv se encarga de apuntar al binario correcto.

> 📝 **¿Por qué `source` y no correr `.venv/bin/activate` directo?** `activate` es un
> script que modifica variables de entorno (`PATH`, `VIRTUAL_ENV`) para que la terminal
> use el Python del venv. Si lo corrés normal (`./activate` o `.venv/bin/activate` sin
> más), zsh abre un **subshell** para ejecutarlo: el subshell activa el venv y se cierra
> al toque, sin que tu terminal actual se entere del cambio (por eso nunca aparece
> `(.venv)` en el prompt). `source` (o su alias `.`) le dice al shell "ejecutá este
> script **en mí mismo**, no en un proceso aparte" — así los cambios quedan en tu sesión.
>
> ⚠️ Otro tropiezo típico: si hiciste `cd` **dentro** de la carpeta `.venv` (en vez de
> quedarte en la carpeta del proyecto/ejercicio), `source .venv/bin/activate` ya no
> encuentra la ruta — `.venv` no está dentro de sí misma. Verificá con `pwd` que estás
> **un nivel arriba** de `.venv` antes de activar — ver
> [[2026-08-14-activate-sin-source-no-funciona]].

El resto de comandos de `pip` son **iguales en cualquier sistema operativo** (una vez con
el venv activado):

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `pip --version` | Muestra la versión de pip **del entorno virtual activo** (falla con "command not found" si el venv no está activado — ver [[pip-command-not-found-venv-inactivo]]) | `pip --version` |
| `pip install <paquete>` | Instala una librería en el venv activo | `pip install fastapi "uvicorn[standard]"` |
| `python3 -m pip install <paquete>` | Igual que `pip install`, pero a prueba de errores: le pide a **ese `python3` puntual** que use su propio `pip` (`-m` = ejecutar un módulo), en vez de confiar en cuál `pip` encuentre el `PATH` primero | `python3 -m pip install alembic` |
| `pip show <paquete>` | Muestra la versión instalada de una librería (para no reinstalar de más) | `pip show fastapi` |
| `pip freeze > requirements.txt` | Congela todas las dependencias instaladas y sus versiones exactas en un archivo | `pip freeze > requirements.txt` |
| `pip install -r requirements.txt` | Instala todas las dependencias listadas en el archivo (lo que corre alguien que clona el repo) | `pip install -r requirements.txt` |
| `python3 archivo.py` | Ejecuta un script de Python | `python3 main.py` |

> 📝 **No todo lo que se importa se instala con `pip`.** Módulos como `calendar`, `os`,
> `json`, `datetime`, `re`, `logging` son parte de la **librería estándar** — vienen
> incluidos con Python, se usan con `import` directo, sin `pip install` de por medio.
> `pip install python3-calendar` da `ERROR: Could not find a version that satisfies the
> requirement` porque ese nombre (`python3-algo`) es la convención de paquetes de
> **apt/Debian/Ubuntu** (`sudo apt install python3-algo`), no de PyPI/`pip` — son dos
> ecosistemas de paquetes distintos.
> ```python
> import calendar
> print(calendar.month(2026, 8))   # no requiere instalar nada
> ```

## 🧩 Microservicios — un venv por servicio (Clase 6)

Desde la Clase 6 cada microservicio (`users_service`, `products_service`, ...) vive en su
propia carpeta con su **propio venv** — no se comparte con los demás servicios ni con
otros ejercicios del curso (ver [[curso-python-backend]] → "Servicio independiente").
Repetir esta secuencia dentro de la carpeta de **cada** servicio:

```bash
cd <nombre_del_servicio>       # p.ej. users_service, products_service
python3 -m venv venv           # 1) crear el entorno (sin source)
source venv/bin/activate       # 2) activarlo (con source)
```

**Dependencias instaladas en `users_service`** (mismo comando sirve para cualquier otro
servicio nuevo — ajustando paquetes según lo que use):
```bash
pip install fastapi "uvicorn[standard]" pydantic sqlalchemy pydantic-settings
```

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `pip install fastapi` | Framework de API — ya visto en [Clase 3](../01-Clases/Clase-03.md) | `pip install fastapi` |
| `pip install "uvicorn[standard]"` | Servidor ASGI que corre la app + extras de rendimiento (`uvloop`, `websockets`, etc.). **Las comillas son obligatorias** en zsh: sin ellas, `[standard]` se interpreta como patrón glob — ver [[2026-08-20-falta-pip-install-uvicorn-standard]] | `pip install fastapi "uvicorn[standard]"` |
| `pip install pydantic-settings` | Lee configuración (`Settings`) desde un `.env` — ver [Clase 4](../01-Clases/Clase-04.md) y [Clase 6](../01-Clases/Clase-06.md) | `pip install pydantic-settings` |
| `pip install pytest httpx` | `pytest` (framework de testing) + `httpx` (cliente HTTP moderno, recomendado por FastAPI para testear endpoints) — para llenar la carpeta `tests/` de cada servicio ([Clase 6](../01-Clases/Clase-06.md)) | `pip install pytest httpx` |

> ⚠️ Errores típicos al armar el venv de un servicio nuevo — ya documentados:
> - `source python3 -m venv venv` → `source` no va con el comando de **crear**, solo con
>   el de **activar** — ver [[2026-08-20-source-antes-de-python3-venv]].
> - `venv\Scripts\activate` (sintaxis de Windows) en zsh → usar `venv/bin/activate` — ver
>   [[2026-08-14-activate-sin-source-no-funciona]].
> - `"uvicorn[standard]"` sin `pip install` adelante → no es un comando, es un argumento —
>   ver [[2026-08-20-falta-pip-install-uvicorn-standard]].
> - `ImportError: email-validator is not installed` al levantar el servidor (si el
>   `schemas.py` del servicio usa `EmailStr`) → falta el extra `pydantic[email]` — ver
>   [[2026-08-20-importerror-email-validator]].

### ▶️ Levantar un microservicio (con el venv activado)

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `uvicorn app.main:app --port <puerto>` | Arranca el servidor ASGI, apuntando a la variable `app` de `app/main.py` | `uvicorn app.main:app --port 8001` |
| `uvicorn app.main:app --port <puerto> --reload` | Igual, pero **reinicia solo** al guardar un cambio en el código — útil mientras se desarrolla | `uvicorn app.main:app --port 8001 --reload` |
| `python3 -m uvicorn app.main:app --reload --port <puerto>` | Mismo resultado que el de arriba, pero pidiéndoselo a **ese `python3` puntual** (`-m`) en vez de confiar en qué `uvicorn` encuentre el `PATH` — mismo motivo que `python3 -m pip install` más arriba. Así lo corrió el profe (con `python` a secas, por estar en Windows) | `python3 -m uvicorn app.main:app --reload --port 8001` |

Cada microservicio usa **su propio puerto** (definido en su `app/config.py` — ver
[Clase 6](../01-Clases/Clase-06.md)), así los dos corren al mismo tiempo sin chocar:
```bash
# terminal 1 — dentro de users_service, venv activado
uvicorn app.main:app --port 8001 --reload

# terminal 2 — dentro de products_service, venv activado
uvicorn app.main:app --port 8002 --reload
```
Con el servidor corriendo, la documentación interactiva (Swagger, vista en
[Clase 3](../01-Clases/Clase-03.md)) queda en `http://127.0.0.1:<puerto>/docs`.

## 🐳 Docker

> Desde la Clase 4 corremos PostgreSQL en un contenedor en vez de instalarlo directo en
> el Mac — estos son los comandos base para manejarlo.

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `docker --version` | Muestra la versión de Docker instalada | `docker --version` |
| `docker ps` | Lista los contenedores **corriendo** ahora mismo | `docker ps` |
| `docker ps -a` | Lista **todos** los contenedores, también los detenidos (`-a` = *all*) | `docker ps -a` |
| `docker images` | Lista las imágenes descargadas en tu Mac | `docker images` |
| `docker run <imagen>` | Crea y arranca un contenedor nuevo a partir de una imagen | ver ejemplo completo abajo |
| `docker stop <nombre\|id>` | Detiene un contenedor corriendo (sin borrarlo) | `docker stop n8n-local` |
| `docker start <nombre\|id>` | Vuelve a arrancar un contenedor ya creado (que quedó detenido) | `docker start bd_test_backend` |
| `docker logs <nombre\|id>` | Muestra la salida/errores de un contenedor — el primer lugar donde mirar si algo no arranca | `docker logs bd_test_backend` |
| `docker rm <nombre\|id>` | Borra un contenedor detenido (no lo corras sobre uno que quieras conservar) | `docker rm mi_contenedor_viejo` |

**Ejemplo real usado en la Clase 4** — levantar Postgres:
```bash
docker run -d \
  --name bd_test_backend \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=curso_backend \
  -p 5432:5432 \
  postgres:16-alpine
```

| Flag | Significado |
|---|---|
| `-d` | *detached* — corre el contenedor "de fondo", sin bloquear la terminal |
| `--name <nombre>` | Le pone un nombre fácil de recordar (si no, Docker le asigna uno random tipo `stupefied_rosalind`) |
| `-e VARIABLE=valor` | Define una **variable de entorno** dentro del contenedor (acá, usuario/password/db de Postgres) |
| `-p <host>:<contenedor>` | Mapea un puerto: "lo que llegue a `localhost:5432` de mi Mac, redirigilo al puerto `5432` de adentro del contenedor" |
| `postgres:16-alpine` | La imagen a usar, con su tag de versión (`16-alpine` = Postgres 16 sobre Alpine Linux, una base liviana) |

> ⚠️ **Error típico si te olvidás el `-e POSTGRES_PASSWORD`:** el contenedor arranca y se
> cae solo (`docker ps -a` lo muestra como `Exited (1)`), con este mensaje en
> `docker logs`: *"Database is uninitialized and superuser password is not specified"*.
> Postgres exige una password para el usuario superadministrador antes de inicializar.

> 🧪 Tip de entrevista: ¿diferencia entre `docker stop` y `docker rm`? `stop` **pausa**
> el contenedor (los datos quedan, se puede volver a arrancar con `docker start`); `rm`
> lo **borra** — si el contenedor no usaba un volumen externo, los datos de adentro se
> pierden para siempre.

### 🐘 `psql` dentro del contenedor — consultar/insertar sin salir de la terminal

`docker exec` corre un comando **adentro** de un contenedor que ya está corriendo (no
crea uno nuevo, a diferencia de `docker run`). Sirve para meterse a la base de Postgres
del curso sin instalar `psql` en el Mac:

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `docker exec -it <contenedor> psql -U <user> -d <db>` | Abre una **sesión interactiva** de `psql` — queda ahí escribiendo SQL hasta que salís con `\q` | `docker exec -it bd_test_backend psql -U postgres -d curso_backend` |
| `docker exec <contenedor> psql -U <user> -d <db> -c "<SQL>"` | Corre **una sola consulta** y vuelve directo a tu terminal — sin quedar "adentro" | `docker exec bd_test_backend psql -U postgres -d curso_backend -c "SELECT COUNT(*) FROM tickets;"` |

> ⚠️ **`-it` vs. sin `-it`:** `-it` (*interactive* + *tty*) es para cuando vos vas a
> tipear en la sesión de `psql`. Si el comando lo corre un script/otro proceso (no una
> persona escribiendo), sacá el `-it` — con él puesto sin una terminal real detrás tira
> `the input device is not a TTY`.

**Ejemplos reales usados en la Clase 4** — ver tablas, contar filas, insertar datos de
prueba (útil cuando un `POST /tickets/` da `500` por una FK a un `user`/`category` que
todavía no existe — ver [[500-foreign-key-inexistente-sin-datos-previos]]):
```bash
# Ver qué tablas existen
docker exec bd_test_backend psql -U postgres -d curso_backend -c "\dt"

# Contar filas de una tabla
docker exec bd_test_backend psql -U postgres -d curso_backend -c "SELECT COUNT(*) FROM tickets;"

# Insertar datos de prueba (varias -c seguidas = varias sentencias, en orden)
docker exec bd_test_backend psql -U postgres -d curso_backend -c \
  "INSERT INTO users (name, email) VALUES ('Styp Canto', 'styp@example.com');" \
  -c "INSERT INTO categories (name) VALUES ('Infraestructura');"
```
