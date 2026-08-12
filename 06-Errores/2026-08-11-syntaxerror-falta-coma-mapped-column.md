---
categoria: "🧠 Lógica y tipos"
sidebar: "SyntaxError: forgot a comma?"
---

# ❌ SyntaxError: invalid syntax. Perhaps you forgot a comma?

> [Clase 4](../01-Clases/Clase-04.md) · en `models/ticket.py`, definiendo `requester_id`

## 🧨 Qué pasó

```python
requester_id: Mapped[int] = mapped_column(
    nullable=False
    ForeignKey("users.id")
)
```

```
File "models/ticket.py", line 38
    nullable=False
             ^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

## 🔍 Causa

Dos argumentos dentro de una llamada a función **siempre** van separados por coma. Acá
faltaba la coma entre `nullable=False` y `ForeignKey("users.id")` — Python lee la línea
siguiente como si fuera continuación de la misma expresión y no sabe qué hacer con ella.

Había un segundo problema en la misma línea: el **orden** de los argumentos. `ForeignKey(
"users.id")` es un argumento **posicional** (sin nombre), `nullable=False` es
**nombrado** (`keyword`). En Python, los argumentos posicionales siempre van **antes**
que los nombrados en una llamada — swapearlos también sería un `SyntaxError`
(`positional argument follows keyword argument`).

## ✅ Solución

```python
requester_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"),   # posicional primero
    nullable=False             # nombrado después, con coma antes
)
```

> 💡 Regla simple: leé la llamada como si fuera una lista — cada elemento separado por
> coma, y los que no tienen "etiqueta" (`nombre=`) van primero.

## 📎 Relacionado
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)
