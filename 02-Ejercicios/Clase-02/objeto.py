# Clase Ticket: define la "forma" de un ticket (qué datos tiene y qué puede hacer),
# no un ticket en sí. Cada Ticket(...) que se cree es un objeto separado, con sus
# propios valores guardados en self.


# __init__ es el constructor: se ejecuta automáticamente al crear el objeto
# (Ticket(...)) y arma su estado inicial guardando cada dato en "self".
class Ticket:
    def __init__(self,ticket_id:int, title:str, priority: str):      
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self._status = "pendiente"  # todo ticket nuevo arranca sin atender

# Asigna un técnico al ticket. OJO: acá recién se crea el atributo
# self.technician -- antes de llamar a este método, el objeto NO lo tiene.
    def assign(self,technician: str) -> None:
        self.technician = technician
        self._status = "Asignado"

# Cierra el ticket. No toca self.technician (queda con el último asignado).
    def close(self) -> None:
        self._status = "Cerrado"

 # Arma un resumen en un solo string, leyendo los atributos actuales del
 # objeto. Los 4 f-strings van pegados sin comas entre ellos a propósito:
 # así Python los concatena en un solo str (si tuvieran coma, se armaría
 # una tupla de 4 strings en vez de un único resumen).
    def get_summary(self) -> str:
        return (
            f"{self.ticket_id} - "
            f"{self.title} - "
            f"{self._status} - "
            f"{self.technician}"
        )

# --- Proceso: crear un ticket, asignarlo y pedir su resumen ---

# 1) Se crea el objeto: corre __init__ y guarda ticket_id/title/priority/status.
#    self.technician todavía NO existe en este punto.
ticket_1 = Ticket(1001, "Error de impresión", "Alta")

# 2) Se llama a assign(): recién acá se crea self.technician = "Técnico Gustavo"
#    y self.status pasa de "pendiente" a "Asignado".
ticket_1.assign("Técnico Gustavo")

# 3) Se llama a get_summary(): ya puede leer self.technician porque el paso 2
#    corrió antes -- si se llamara ANTES del assign(), tiraría AttributeError.
#    print() muestra el string que devuelve.
print(ticket_1.get_summary())

@property
def status(self) -> str:
    return self._status

#property es un decorador que permite acceder a un método como si fuera un atributo. 
#En este caso, permite acceder al estado del ticket sin necesidad de llamar al método get_status().

#setters and getters

