#self crea a mi mismo
class Ticket:
    def __init__(self, ticket_id: int, title: str, priority: str): #Crea un constructor conla palabra init
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "pendiente"

ticket_1 = Ticket(1001, "Error al inicial sesión", "Alta")
print(ticket_1.ticket_id)
print(ticket_1.title)
print(ticket_1.priority)
print(ticket_1.status)

# def define un método
class Perro:
    def __init__(self, peso: float, talla: float, familia: str):
        self.peso = peso
        self.talla = talla
        self.familia = familia
    


perro_golden = Perro(15.5, 2.20, "Golden")
perro_salchicha = Perro(2.2, 1.2, "Salchicha")
perro_san_bernardo = Perro(15.3, 2604, "San Bernardo")

print(perro_golden.peso,perro_golden.familia)
print(perro_salchicha.peso,perro_salchicha.familia)
print(perro_san_bernardo.peso,perro_san_bernardo.familia)