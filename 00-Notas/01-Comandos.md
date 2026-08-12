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

El resto de comandos de `pip` son **iguales en cualquier sistema operativo** (una vez con
el venv activado):

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `pip --version` | Muestra la versión de pip **del entorno virtual activo** (falla con "command not found" si el venv no está activado — ver [[pip-command-not-found-venv-inactivo]]) | `pip --version` |
| `pip install <paquete>` | Instala una librería en el venv activo | `pip install fastapi "uvicorn[standard]"` |
| `pip show <paquete>` | Muestra la versión instalada de una librería (para no reinstalar de más) | `pip show fastapi` |
| `pip freeze > requirements.txt` | Congela todas las dependencias instaladas y sus versiones exactas en un archivo | `pip freeze > requirements.txt` |
| `pip install -r requirements.txt` | Instala todas las dependencias listadas en el archivo (lo que corre alguien que clona el repo) | `pip install -r requirements.txt` |
| `python3 archivo.py` | Ejecuta un script de Python | `python3 main.py` |

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
| `docker start <nombre\|id>` | Vuelve a arrancar un contenedor ya creado (que quedó detenido) | `docker start curso-postgres` |
| `docker logs <nombre\|id>` | Muestra la salida/errores de un contenedor — el primer lugar donde mirar si algo no arranca | `docker logs curso-postgres` |
| `docker rm <nombre\|id>` | Borra un contenedor detenido (no lo corras sobre uno que quieras conservar) | `docker rm mi_contenedor_viejo` |

**Ejemplo real usado en la Clase 4** — levantar Postgres:
```bash
docker run -d \
  --name curso-postgres \
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
