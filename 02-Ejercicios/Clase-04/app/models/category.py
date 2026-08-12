from typing import TYPE_CHECKING
if TYPE_CHECKING:
      from models.ticket import Ticket

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Base: la clase de la que heredan todos los modelos (la definimos en db/database.py)
from db.database import Base

class Category(Base):
    __tablename__ = "categories"

    # Agrego configuraciones de mapeo para la columna id
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Defino la columna name como un string de 50 caracteres y no nula)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    # Relación: una Category tiene MUCHOS Tickets (el "category" del ticket)
    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="category"
    )