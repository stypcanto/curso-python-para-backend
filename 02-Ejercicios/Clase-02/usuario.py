from objeto import Ticket


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Technician(User):
    def __init__(self, name: str, email: str, specialty: str):
        super().__init__(name, email)
        self.specialty = specialty
        
    def attend_ticket(self, ticket: Ticket) -> None:
        ticket.assign(self.name)