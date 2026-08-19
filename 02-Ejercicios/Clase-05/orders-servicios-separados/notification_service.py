class NotificationService:
    def send(
        self,
        email: str,
        message: str,
    ):
        print(
            f"Enviando a {email}: "
            f"{message}"
        )
