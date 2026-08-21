---
categoria: "🔁 Compilación y ejecución"
sidebar: "ModuleNotFoundError: 'app' (pytest)"
---

# ❌ ModuleNotFoundError: No module named 'app' al correr `pytest`

> [Clase 6](../01-Clases/Clase-06.md) · corriendo `tests/test.py` de `users_service`

## 🧨 Qué pasó

```bash
pytest tests/test.py
```
```
ModuleNotFoundError: No module named 'app'
tests/test.py:3: in <module>
    from app.main import app
```

## 🔍 Causa

No es el mismo motivo que [[modulenotfounderror-app-prefix]] (ese es sobre el *prefijo*
del import, distinto proyecto/convención). Acá el import `from app.main import app` es
correcto — el problema es **cómo se invoca `pytest`**.

`pytest` (el comando, a secas) **no agrega automáticamente la carpeta desde donde lo
corrés al `sys.path`** cuando no hay un `pyproject.toml`/`pytest.ini`/`conftest.py` que
lo configure. Sin `users_service/` en el `sys.path`, Python no encuentra el paquete
`app` (que vive en `users_service/app/`).

## ✅ Solución

Correr pytest como **módulo de Python** (`-m`), no como comando suelto — mismo principio
que `python3 -m uvicorn` (ver [Clase 6](../01-Clases/Clase-06.md)): con `-m`, Python
agrega el directorio actual al `sys.path` antes de ejecutar.

```bash
python3 -m pytest tests/test.py -v
```
```
tests/test.py::test_health PASSED
tests/test.py::test_create_user PASSED
2 passed in 0.19s
```

> 💡 Regla rápida: para cualquier herramienta que se instale con `pip` y se corra desde
> la raíz de tu proyecto (`pytest`, `uvicorn`, `alembic`...), si te tira
> `ModuleNotFoundError` con tu propio paquete, probá primero con `python3 -m <herramienta>`
> antes de sospechar del import.

## 📎 Relacionado
- [[modulenotfounderror-app-prefix]] (mismo mensaje de error, causa distinta — no confundir)
- [Clase 6](../01-Clases/Clase-06.md)
