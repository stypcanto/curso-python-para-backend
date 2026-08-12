---
categoria: "⚙️ Configuración"
sidebar: "Pylance: reportUndefinedVariable (FK)"
---

# ❌ "Ticket" no está definido (Pylance) en una relación de SQLAlchemy

> [Clase 4](../01-Clases/Clase-04.md) · en `models/user.py`, definiendo la relación `tickets`

## 🧨 Qué pasó

```python
tickets: Mapped[list["Ticket"]] = relationship(
    back_populates="requester"
)
```

```
"Ticket" no está definido  Pylance(reportUndefinedVariable)
```

## 🔍 Causa

**No es un error real de Python** (el import funciona en terminal) — es Pylance
avisando que no sabe qué es `"Ticket"` dentro del `Mapped[list["Ticket"]]`.

Ese nombre está **entre comillas a propósito**: es una referencia diferida, un patrón
normal de SQLAlchemy para relaciones. Se usa porque `user.py` y `ticket.py` se
necesitan mutuamente (`User` tiene `tickets`, `Ticket` tiene `requester`) — si
`user.py` importara `Ticket` de forma normal (sin comillas) arriba del archivo, se
arma un **import circular** y Python no arranca.

## ✅ Solución

Importar la clase **solo para el chequeo de tipos**, con `TYPE_CHECKING` (nunca se
ejecuta en tiempo real, así que no genera el import circular):

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.ticket import Ticket


class User(Base):
    ...
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="requester")
```

`TYPE_CHECKING` es una constante que **siempre vale `False`** cuando el programa corre
de verdad — ese `import` nunca se ejecuta. Pero las herramientas de análisis estático
(Pylance, mypy) sí lo leen, así que entienden qué es `"Ticket"` y el aviso desaparece.

> 💡 Se repite en cualquier par de modelos que se referencian entre sí: `Category` ↔
> `Ticket` tiene exactamente el mismo caso.

## 📎 Relacionado
- [[pylance-no-resuelve-import-pydantic]] (otro aviso de Pylance que tampoco es error real)
- [00-Notas/05-Estructura-Proyecto-FastAPI.md](../00-Notas/05-Estructura-Proyecto-FastAPI.md)
