from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=500)
    priority: str = Field(default="Media")

    requester_id: int = Field(gt=0)
    category_id: int = Field(gt=0)


class TicketUpdate(BaseModel):
    priority: str | None = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str 
    priority: str

    requester_id: int
    category_id: int
