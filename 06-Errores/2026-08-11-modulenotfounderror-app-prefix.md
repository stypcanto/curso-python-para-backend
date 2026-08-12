---
categoria: "🖥️ Comandos y rutas"
sidebar: "ModuleNotFoundError: 'app'"
---

# ❌ ModuleNotFoundError: No module named 'app'

> [Clase 4](../01-Clases/Clase-04.md) · en `repositories/ticket_repository.py` y
> `services/ticket_service.py`

## 🧨 Qué pasó

```python
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate
```

```
ModuleNotFoundError: No module named 'app'
```

Pasó (o casi pasa) **3 veces** en la misma clase: en `repositories/ticket_repository.py`,
en `services/ticket_service.py`, y de nuevo con el `migrations/env.py` mostrado en el
material del curso (`from app.db.database import Base`, etc.) — viene de que **ese
material corre el proyecto desde otra carpeta** (ver causa).

## 🔍 Causa

El material de referencia corre el proyecto desde **un nivel más arriba** de `app/`
(fuera de esa carpeta), y ahí sí `app` es un paquete importable (`from app.models...`).
En este proyecto, la convención que se viene usando desde el principio es correr
**desde adentro** de `app/` (ahí vive el `.venv`, ahí se activa), así que acá no existe
ningún paquete llamado `app` — los paquetes son directamente `models`, `schemas`,
`repositories`, `services`, etc.

## ✅ Solución

```python
from models.ticket import Ticket
from schemas.ticket import TicketCreate, TicketUpdate
```

Sin el prefijo `app.` — igual que en `models/user.py`, `models/ticket.py` y el resto
de archivos del proyecto.

> 💡 Regla para no repetirlo: antes de escribir un import entre carpetas propias del
> proyecto, mirate un archivo que ya funcione (ej. `models/ticket.py`) y copiá el mismo
> estilo de import — no el de un tutorial externo, que puede correr el proyecto desde
> otra carpeta.

## 📎 Relacionado
- [[python-command-not-found]]
