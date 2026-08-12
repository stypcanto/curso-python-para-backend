---
categoria: "🧠 Lógica y tipos"
sidebar: "InvalidRequestError: 'User' no localizado"
---

# ❌ InvalidRequestError: expression 'User' failed to locate a name

> [Clase 4](../01-Clases/Clase-04.md) · al crear el primer `Ticket` de verdad (probando
> el router)

## 🧨 Qué pasó

```python
from routers.tickets import router
# ... arma la app, hace POST /tickets/ ...
```

```
sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[Ticket(tickets)],
expression 'User' failed to locate a name ('User'). If this is a class name, consider
adding this relationship() to the <class 'models.ticket.Ticket'> class after both
dependent classes have been defined.
```

## 🔍 Causa

`models/ticket.py` declara `requester: Mapped["User"] = relationship(...)` con `"User"`
**entre comillas** (referencia diferida — ver
[[pylance-forward-reference-no-definido]]). Esa cadena de texto recién se resuelve la
**primera vez que se usa** un `Ticket` de verdad (al instanciarlo o consultarlo) — no en
el `import`.

El error salió porque el script que probaba el router solo importaba `routers.tickets`
(que en cadena llega hasta `models.ticket`), pero **nunca importaba `models.user` ni
`models.category` directamente**. Como esos módulos nunca se importaron en ningún lado
que realmente corriera, sus clases `User`/`Category` nunca quedaron registradas en
SQLAlchemy, y `"User"` quedó como un nombre sin dueño.

> 📝 El bloque `if TYPE_CHECKING: from models.user import User` **no cuenta** para
> esto — ese import nunca se ejecuta en tiempo real (`TYPE_CHECKING` es `False`), es
> solo para que Pylance entienda los tipos.

## ✅ Solución

Importar los 3 modelos juntos, en algún punto que sí corra siempre (por ejemplo, al
principio de `main.py`, o justo antes de `create_all()`):

```python
from models.user import User
from models.category import Category
from models.ticket import Ticket
```

## 📎 Relacionado
- [[pylance-forward-reference-no-definido]]
