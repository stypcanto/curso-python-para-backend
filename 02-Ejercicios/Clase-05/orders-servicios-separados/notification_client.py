"""
NotificationServiceClient — reemplaza a NotificationService (notification_service.py)
ahora que `notifications` se extrajo a su propio proceso (ver ../notifications-service/).

Misma interfaz pública que la clase local (.send(email, message)) a propósito: para
quien la use desde OrderService, el cambio es invisible — sigue siendo
"self.notifications.send(...)". Lo que cambió es lo que hay ADENTRO del método: antes
un `print()` local, ahora una llamada HTTP a un proceso que puede estar en otra
máquina.
"""

import httpx

NOTIFICATIONS_SERVICE_URL = "http://127.0.0.1:5070"


class NotificationServiceClient:
    def send(self, email: str, message: str):
        response = httpx.post(
            f"{NOTIFICATIONS_SERVICE_URL}/notifications/send",
            json={"email": email, "message": message},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
