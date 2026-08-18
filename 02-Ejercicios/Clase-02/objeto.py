class Ticket:
    def __init__(self,ticket_id:int, title:str, priority: str):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "pendiente"
    
    def assign(self,technician: str) -> None:
        self.technician = technician
        self.status = "Asignado"

    def close(self) -> None:
        self.status = "Cerrado"
    
    def get_summary(self) -> str:
        return (
            f"{self.ticket_id} - "
            f"{self.title} - "
            f"{self.status} - "
            f"{self.technician}"
        )
ticket_1 = Ticket(1001, "Error de impresión", "Alta")
ticket_1.assign("Técnico 1")
print(ticket_1.get_summary())
