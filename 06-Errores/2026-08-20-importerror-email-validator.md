---
categoria: "⚙️ Configuración"
sidebar: "ImportError: email-validator"
---

# ❌ ImportError: email-validator is not installed

> [Clase 6](../01-Clases/Clase-06.md) · al levantar `users_service` (`schemas.py` usa `EmailStr`)

## 🧨 Qué pasó

Al correr `uvicorn app.main:app` (o simplemente importar la app) con el `requirements.txt`
inicial (`fastapi`, `uvicorn[standard]`, `pydantic`, `sqlalchemy`, `pydantic-settings` —
sin extras):

```
ImportError: email-validator is not installed, run `pip install 'pydantic[email]'`
```

Reproducido en el venv real de `users_service` corriendo:
```bash
python3 -c "from app.main import app"
```

## 🔍 Causa

`schemas.py` usa `EmailStr` (ver [Clase 6, glosario](../01-Clases/Clase-06.md)):
```python
class UserCreate(BaseModel):
    ...
    email: EmailStr
```

`EmailStr` **no viene con Pydantic por defecto** — necesita el paquete extra
`email-validator` instalado aparte. Como el `pip install pydantic` de la clase no incluía
ese extra, Pydantic no puede armar el validador de `email` y falla recién al importar el
esquema (no al instalar, sino al **usarlo**) — por eso el error aparece al arrancar el
servidor, no antes.

## ✅ Solución

```bash
pip install "pydantic[email]"
```

(instala `email-validator` + `dnspython` como dependencias). Después de esto,
`from app.main import app` importa sin errores y los 3 endpoints de `users_service`
responden bien — confirmado corriendo el servidor real:

```bash
uvicorn app.main:app --port 8001
curl http://127.0.0.1:8001/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Styp Canto","email":"styp@example.com"}'
# → {"name":"Styp Canto","email":"styp@example.com","id":1}
```

> 📝 `requirements.txt` de `users_service` ya se actualizó con `pip freeze` después de
> este fix — incluye `email-validator` y `dnspython`. `products_service` no lo necesita
> (su `schemas.py` no usa `EmailStr`).

## 📎 Relacionado
- [Clase 6 — `schemas.py`](../01-Clases/Clase-06.md#pydantic) (glosario de `EmailStr`)
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)
