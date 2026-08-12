# Con este archivo vamos a poder interactuar con la base de datos y realizar
# operaciones sobre los tickets.

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.ticket import Ticket
from schemas.ticket import TicketCreate, TicketUpdate


class TicketRepository:
    # Trae TODOS los tickets, ordenados por id
    def get_all(self,
                db: Session
                ) -> list[Ticket]:
        statement = select(Ticket).order_by(Ticket.id)
        return list(db.scalars(statement).all())

    # Trae UN ticket por su id (None si no existe)
    def get_by_id(self, 
                  db: Session, 
                  ticket_id: int
                  ) -> Ticket | None:
        return db.get(
            Ticket, ticket_id
            )

    # Crea un ticket nuevo a partir de los datos validados por TicketCreate
    def create(self, 
               db: Session,
               data: TicketCreate
               ) -> Ticket:
        ticket = Ticket(
            **data.model_dump())
        
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    # Actualiza SOLO los campos que vinieron en data (exclude_unset=True)
    def update(self,
               db: Session,
               ticket: Ticket, 
               data: TicketUpdate
               ) -> Ticket:
        changes = data.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(
                ticket, 
                field, 
                value)
        db.commit()
        db.refresh(ticket)
        return ticket

    # Borra un ticket existente
    def delete(self,
               db: Session, 
               ticket: Ticket
               ) -> None:
        db.delete(ticket)
        db.commit()
