---
categoria: "🖥️ Comandos y rutas"
sidebar: "zsh: command not found: pip"
---

# ❌ zsh: command not found: pip

> [Clase 4](../01-Clases/Clase-04.md) · al instalar `pydantic` y `sqlalchemy`

## 🧨 Qué pasó

```bash
❯ pip install pydantic
zsh: command not found: pip
❯ pip install sqlalchemy
zsh: command not found: pip
```

## 🔍 Causa

`pip` **no existe como comando global** en macOS — solo existe *dentro* de un entorno
virtual activado. El error aparece cuando se abre una **terminal/pestaña nueva** y se
te olvida activar el `.venv` en esa sesión (la activación no queda "para siempre", es
por cada terminal que abrís).

## ✅ Solución

```bash
cd 02-Ejercicios/Clase-04/app
source .venv/bin/activate      # el prompt debe mostrar (.venv) al inicio
pip install sqlalchemy         # recién ahí `pip` existe
```

> 💡 Regla rápida: si `python` o `pip` "no existen", lo primero a revisar es si el venv
> está activado en **esa** terminal — mirá si tu prompt empieza con `(.venv)`.

## 📎 Relacionado
- [[python-command-not-found]]
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)

## 🔁 Recurrió en Clase 6 (2026-08-20) — mismo root cause, síntoma distinto

Mismo motivo (venv sin activar), pero esta vez con `python3` — que sí existe como
comando **global** en macOS (a diferencia de `pip`), así que el error no es "command not
found": la terminal encuentra un Python (el del sistema, no el del venv) y falla más dentro,
al no encontrar el paquete instalado **solo dentro del venv**:

```bash
❯ Python -m uvicorn app.main:app --reload --port 8001
zsh: command not found: Python

❯ Python3 -m uvicorn app.main:app --reload --port 8001
/opt/homebrew/opt/python@3.14/bin/python3.14: No module named uvicorn
```

Dos cosas mezcladas:

1. **El venv no estaba activado** en esa terminal — causa real. `python3` (sin activar)
   apunta al Python del sistema (acá, el de Homebrew), que no tiene `uvicorn` instalado
   porque `uvicorn` vive solo en `venv/lib/.../site-packages` de este proyecto.
2. **`Python`/`Python3` con mayúscula inicial** — detalle aparte, no la causa del error.
   El primer intento (`Python`, sin "3") ni siquiera existe como archivo, por eso da
   *command not found*. El segundo (`Python3`) sí "funciona" — porque el volumen de disco
   de macOS es **case-insensitive** por defecto (ver nota de `Presentaciones`/
   `presentaciones` en la memoria del curso): `Python3` encuentra el mismo archivo que
   `python3`, con otra letra. No es un error en sí, pero conviene escribirlo en minúscula
   (`python3`) — es la convención real del binario, y en Linux (case-sensitive de
   verdad) `Python3` con mayúscula sí daría *command not found*.

**Solución — activar el venv antes de correr uvicorn:**
```bash
source venv/bin/activate      # el prompt debe mostrar (venv)
python3 -m uvicorn app.main:app --reload --port 8001
```

> 💡 Confirmado: con el venv activado, `python3 -c "import uvicorn"` resuelve al
> `uvicorn` de `venv/lib/python3.14/site-packages/`, no al del sistema.
