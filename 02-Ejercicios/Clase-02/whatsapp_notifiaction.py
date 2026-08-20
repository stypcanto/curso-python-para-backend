from notification_channel import NotificacionChannel

class WhatsAppNotification(NotificacionChannel):
    def send(
        self,
        recipient: str,
        message: str
        ) -> None:
        print(f"Mensaje WhatsApp enviado a {recipient} con el mensaje: {message}")