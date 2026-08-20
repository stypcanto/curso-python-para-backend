from notification_channel import NotificacionChannel

class EmailNotification(NotificacionChannel):
    def send(
        self,
        recipient:str,
        message: str
        ) -> None:
        print(f"Correo enviado a {recipient} con el mensaje: {message}")
        

