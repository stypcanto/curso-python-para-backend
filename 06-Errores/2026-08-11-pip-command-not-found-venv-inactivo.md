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
