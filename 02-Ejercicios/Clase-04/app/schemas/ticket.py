from pydantic import BaseModel, ConfigDict, Field


# Lo que el cliente manda para CREAR un ticket (entrada de la API)
class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=500)
    priority: str = Field(default="Media")

    requester_id: int = Field(gt=0)
    category_id: int = Field(gt=0)


# Lo que el cliente manda para ACTUALIZAR un ticket (todo opcional)
class TicketUpdate(BaseModel):
    priority: str | None = None
    description: str | None = None


# Lo que la API DEVUELVE al cliente (salida de la API)
class TicketResponse(BaseModel):
    # from_attributes=True: permite crear este schema a partir de un objeto
    # ORM (Ticket de SQLAlchemy), no solo de un dict — lo necesita el router
    # cuando devuelve directo lo que trae el repository/service.
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: str

    requester_id: int
    category_id: int

