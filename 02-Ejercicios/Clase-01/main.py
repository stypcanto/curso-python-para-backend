"""Reto de la Clase 1: procesador de solicitudes de soporte.

Recorre una lista de solicitudes, calcula su tiempo máximo de respuesta con
una función definida en un módulo separado (request_utils.py) y maneja las
prioridades no reconocidas con try/except en vez de dejar que el programa
se detenga.
"""

from request_utils import calculate_response_time

support_requests = [
    {"id": 1001, "title": "Error de acceso", "priority": "Alta"},
    {"id": 1002, "title": "Lentitud del sistema", "priority": "Media"},
    {"id": 1003, "title": "Duda de uso", "priority": "Baja"},
    {"id": 1004, "title": "Solicitud rara", "priority": "Urgentisima"},
]

for request in support_requests:
    try:
        hours = calculate_response_time(request["priority"])
        print(f"Solicitud {request['id']} ({request['title']}): responder en {hours}h")
    except ValueError as error:
        print(f"Solicitud {request['id']}: {error}")
