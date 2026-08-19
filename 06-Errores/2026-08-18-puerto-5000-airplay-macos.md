---
categoria: "🖥️ Comandos y rutas"
sidebar: "Puerto 5000 ocupado (AirPlay)"
---

# ❌ El puerto 5000 "ya está en uso" en macOS (aunque no corriste nada)

> [Clase 5](../01-Clases/Clase-05.md) · levantando `products-service-flask` con
> `flask --app services/products run` (puerto 5000 por defecto de Flask)

## 🧨 Qué pasó

```bash
flask --app services/products run
```

```
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or
start the server with a different port.
On macOS, try searching for and disabling 'AirPlay Receiver' in System Settings.
```

Lo llamativo: no había ningún servidor propio corriendo todavía. `lsof` lo confirma:

```bash
$ lsof -nP -iTCP:5000 -sTCP:LISTEN
COMMAND   PID USER   FD   TYPE  ...  NAME
ControlCe 726 styp   10u  IPv4  ...  *:5000 (LISTEN)
ControlCe 726 styp   11u  IPv6  ...  *:5000 (LISTEN)
```

## 🔍 Causa

En macOS, **AirPlay Receiver** (el proceso `ControlCenter`) escucha por defecto en el
puerto **5000** — es el mismo puerto que Flask usa por defecto cuando no le pasás
`--port`. El propio mensaje de error de Flask ya lo señala directo (Werkzeug detecta que
es macOS y da la pista de AirPlay), lo cual es una ayuda que no todos los frameworks dan.

> 📝 En la práctica el conflicto es intermitente: a veces `ControlCenter` deja bindear
> igual porque escucha en el wildcard (`*:5000`) y Flask puede pedir específicamente
> `127.0.0.1:5000` — pero no hay que depender de esa suerte. El error real y reproducible
> aparece si además queda un proceso Python previo sin matar en ese puerto (`Address
> already in use` para un PID de `Python`, no de `ControlCe`) — confirmarlo siempre con
> `lsof` antes de asumir cuál de los dos es.

## ✅ Solución

Dos formas, según si necesitás liberar el 5000 o no:

**A. Correr en otro puerto (más simple, no toca configuración del sistema):**
```bash
flask --app services/products run --port 5050
```

**B. Desactivar AirPlay Receiver** (si de verdad querés usar el 5000):
`Ajustes del Sistema → General → AirDrop y Handoff → apagar "Recepción de AirPlay"`.

**Para saber qué proceso tiene el puerto ocupado en cualquier caso** (más general que
esto, sirve para cualquier "Address already in use" en macOS):
```bash
lsof -nP -iTCP:5000 -sTCP:LISTEN
kill -9 <PID>   # solo si es un proceso tuyo (p. ej. un Flask/uvicorn anterior sin matar)
```

> 💡 Por esto `products-service` (la versión FastAPI de este mismo microservicio, en
> `02-Ejercicios/Clase-05/products-service/main.py`) se corrió con `--port 5050` desde
> el principio — evita este choque sin tener que tocar ningún ajuste del sistema.
