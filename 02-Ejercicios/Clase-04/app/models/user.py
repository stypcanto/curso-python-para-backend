
# TYPE_CHECKING: True solo para Pylance/mypy, False en tiempo de ejecución.
# Así evitamos el import circular (Ticket también va a importar User) pero
# Pylance igual sabe qué es "Ticket" en el Mapped[list["Ticket"]] de abajo.
from typing import TYPE_CHECKING

# String: tipo de columna de texto con largo definido (String(50), String(150)...)
# Mapped/mapped_column: la forma moderna (SQLAlchemy 2.0) de declarar una columna
# relationship: arma la relación entre tablas (acá, User -> sus Tickets)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Base: la clase de la que heredan todos los modelos (la definimos en db/database.py)
from db.database import Base

if TYPE_CHECKING:
    from models.ticket import Ticket


class User(Base):
    __tablename__ = "users"

#Agrego cofngiuraciones de mapeo para la columna id
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    
#Defino la columna name como un string de 50 caracteres y no nula)
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
#Defino la columna email como un string de 150 caracteres, no nula y única
    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

#Relación: un User tiene MUCHOS Tickets (el "requester" del ticket)
    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="requester"
    )