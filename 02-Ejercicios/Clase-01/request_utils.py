"""Funciones reutilizables para procesar solicitudes de soporte."""


def calculate_response_time(priority: str) -> int:
    """Devuelve el tiempo máximo de respuesta (en horas) según la prioridad.

    Lanza ValueError si la prioridad no es una de las reconocidas, para que
    quien llame a la función decida cómo manejar el caso (try/except).
    """
    if priority == "Alta":
        return 2
    if priority == "Media":
        return 8
    if priority == "Baja":
        return 24
    raise ValueError(f"Prioridad desconocida: {priority}")
