---
categoria: "🔁 Compilación y ejecución"
sidebar: "ImportError: create_engine"
---

# ❌ ImportError: cannot import name 'create_engine' from 'sqlalchemy.orm'

> [Clase 4](../01-Clases/Clase-04.md) · en `db/database.py`

## 🧨 Qué pasó

```python
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.orm import create_engine
```

```
ImportError: cannot import name 'create_engine' from 'sqlalchemy.orm'
Did you mean: 'create_mock_engine'?
```

## 🔍 Causa

SQLAlchemy separa sus piezas en submódulos según qué hacen. `create_engine` (el que
arma la conexión a la base de datos) vive en el paquete **principal** `sqlalchemy`, no
en `sqlalchemy.orm` (que trae lo relacionado a mapear clases ↔ tablas: `DeclarativeBase`,
`sessionmaker`, `relationship`, `Mapped`, `mapped_column`...).

## ✅ Solución

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
```

> 💡 Regla práctica para no confundirse: si es sobre **cómo se conecta** a la base de
> datos (`create_engine`, `URL`), va en `sqlalchemy`. Si es sobre **cómo se mapean**
> clases Python a tablas (`DeclarativeBase`, `Mapped`, `relationship`, `sessionmaker`),
> va en `sqlalchemy.orm`.

## 📎 Relacionado
- [00-Notas/05-Estructura-Proyecto-FastAPI.md](../00-Notas/05-Estructura-Proyecto-FastAPI.md)
