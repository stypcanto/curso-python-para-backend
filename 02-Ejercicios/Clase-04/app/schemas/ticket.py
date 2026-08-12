from pydantic import BaseModel, ConfigDict, Field


# Lo que el cliente manda para CREAR un ticket (entrada de la API)
class TicketCreate(BaseModel):
    # Título corto del problema — entre 5 y 120 caracteres
    title: str = Field(min_length=5, max_length=120)
    # Detalle completo del problema — entre 10 y 500 caracteres
    description: str = Field(min_length=10, max_length=500)
    # Urgencia del ticket — si no la mandan, queda "Media" por defecto
    priority: str = Field(default="Media")

    # FK: quién reporta el ticket (id de un user que ya existe, > 0)
    requester_id: int = Field(gt=0)
    # FK: a qué categoría pertenece (id de una category que ya existe, > 0)
    category_id: int = Field(gt=0)


# Lo que el cliente manda para ACTUALIZAR un ticket (todo opcional)
class TicketUpdate(BaseModel):
    # Opcional: cambiar solo la prioridad, sin tocar el resto
    priority: str | None = None
    # Opcional: cambiar solo la descripción, sin tocar el resto
    description: str | None = None


# Lo que la API DEVUELVE al cliente (salida de la API)
class TicketResponse(BaseModel):
    # from_attributes=True: permite crear este schema a partir de un objeto
    # ORM (Ticket de SQLAlchemy), no solo de un dict — lo necesita el router
    # cuando devuelve directo lo que trae el repository/service.
    model_config = ConfigDict(from_attributes=True)

    # El id que le asignó Postgres al crear el registro
    id: int
    title: str
    description: str
    priority: str

    # Las mismas FK, ya guardadas en la base de datos
    requester_id: int
    category_id: int
