---
categoria: "⚙️ Configuración"
sidebar: "pydantic-settings + .env faltantes"
---

# ❌ Settings() no encuentra `database_url` (falta el paquete y el `.env`)

> [Clase 4](../01-Clases/Clase-04.md) · en `core/config.py` + `db/database.py`

## 🧨 Qué pasó

```python
# core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
```

Dos errores encadenados al importar esto:
1. `ModuleNotFoundError: No module named 'pydantic_settings'`
2. Después de instalarlo, un error de validación de Pydantic: `database_url` es
   obligatorio y no lo encuentra en ningún lado.

## 🔍 Causa

**1) Paquete separado:** desde Pydantic v2, `BaseSettings` (leer configuración desde
variables de entorno) **se sacó del paquete `pydantic`** y pasó a vivir en un paquete
aparte, `pydantic-settings`. Instalar `pydantic` no lo incluye — hay que instalarlo por
separado.

**2) Archivo `.env` inexistente:** `SettingsConfigDict(env_file=".env")` le dice a
`Settings` "buscá los valores en un archivo `.env`" — pero ese archivo todavía no
existía en `02-Ejercicios/Clase-04/app/`. Sin él, `database_url` (que es obligatorio,
sin valor por defecto) no tiene de dónde salir.

Además, en `db/database.py`, `settings` se usaba (`settings.database_url`) sin
**importarlo** — `core/config.py` lo define, pero cada archivo que lo necesita tiene
que traerlo con su propio `import`.

## ✅ Solución

```bash
pip install pydantic-settings
```

Crear `02-Ejercicios/Clase-04/app/.env` (nunca se sube a git — agregado a
`.gitignore`):
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/curso_backend
```

Y en `db/database.py`, importar `settings` antes de usarlo:
```python
from core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
```

> 💡 `pydantic-settings` matchea `DATABASE_URL` (mayúsculas, en el `.env`) con
> `database_url` (minúsculas, en la clase `Settings`) automáticamente — por defecto no
> distingue mayúsculas/minúsculas entre el nombre de la variable de entorno y el campo.

> 🧪 **Tip de entrevista:** *¿Por qué no hardcodear la URL de la base de datos en el
> código?* Porque cambia entre entornos (tu Mac en desarrollo, un servidor en
> producción) y puede contener credenciales — el `.env` mantiene esos valores fuera del
> código fuente (y fuera de git).

## 📎 Relacionado
- [[pip-command-not-found-venv-inactivo]]
