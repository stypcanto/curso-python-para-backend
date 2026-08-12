from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Base: la clase de la que heredan todos los modelos (la definimos en db/database.py)
from db.database import Base

if TYPE_CHECKING:
    from models.category import Category
    from models.user import User


class Ticket(Base):
    __tablename__ = "tickets"

    # Agrego configuraciones de mapeo para la columna id
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Defino la columna title como un string de 120 caracteres y no nula
    title: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Media"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Abierto"
    )

    requester_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )

    # Relación: el usuario que reportó este ticket (lado inverso de User.tickets)
    requester: Mapped["User"] = relationship(
        back_populates="tickets"
    )

    # Relación: la categoría de este ticket (lado inverso de Category.tickets)
    category: Mapped["Category"] = relationship(
        back_populates="tickets"
    )
