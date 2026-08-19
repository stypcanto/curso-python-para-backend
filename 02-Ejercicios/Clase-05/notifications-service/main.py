"""
notifications-service — la primera pieza extraída físicamente de
orders-servicios-separados/ a su propio proceso.

Se eligió `notifications` para extraer primero (no `products` ni `inventory`) porque es
la que menos dependía de las demás: no lee ni escribe `USERS`/`PRODUCTS`, solo recibe un
email y un mensaje. Es la extracción de menor riesgo — el mismo criterio que en Clase-05
(sección 2) se explicó para decidir qué módulo sacar primero de un monolito modular.

Corre sola, en su propio puerto — nadie más necesita conocer su código, solo su URL.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="notifications-service",
    description="Microservicio independiente: envío de notificaciones.",
    version="1.0.0",
)


class NotificationRequest(BaseModel):
    email: str
    message: str


@app.get("/")
def home():
    return {"service": "notifications", "status": "ok"}


@app.post("/notifications/send")
def send_notification(payload: NotificationRequest):
    # En un sistema real esto dispararía un email/push de verdad — acá se deja el
    # mismo `print` que tenía la versión local, para que el cambio que importa quede
    # claro: NO es la lógica de negocio, es dónde vive el proceso que la ejecuta.
    print(f"Enviando a {payload.email}: {payload.message}")
    return {"status": "sent", "email": payload.email}
