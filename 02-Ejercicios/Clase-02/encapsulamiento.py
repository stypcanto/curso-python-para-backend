from objeto import Ticket
from perro import Perro

ticket_1 = Ticket(1001, "Error de impresión", "Alta")
ticket_1.assign("Técnico Gustavo")
print(ticket_1.get_summary())

print(ticket_1._status)  # imprime "Asignado" porque el ticket fue asignado 

#las palabtad con _ se usan para identifcar que son encapusladas y no se deben usar fuera de la clase, pero no es obligatorio.
