from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.ticket import Ticket
from repositories.ticket_repository import (
    TicketRepository,
)
from schemas.ticket import (
    TicketCreate,
    TicketUpdate,
)

class TicketService:
    def __init__(
        self,
        repository: TicketRepository,
    ):
        self.repository = repository
    def list_tickets(
        self,
        db: Session,
    ) -> list[Ticket]:
        return self.repository.get_all(db)
    def get_ticket(
        self,
        db: Session,
        ticket_id: int,
    ) -> Ticket:
        ticket = self.repository.get_by_id(
            db,
            ticket_id,
        )
        if ticket is None:
            raise HTTPException(
                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
                detail="Ticket no encontrado",
            )
        return ticket
    def create_ticket(
        self,
        db: Session,
        data: TicketCreate,
    ) -> Ticket:
        return self.repository.create(
            db,
            data,
        )
    def update_ticket(
        self,
        db: Session,
        ticket_id: int,
        data: TicketUpdate,
    ) -> Ticket:
        ticket = self.get_ticket(
            db,
            ticket_id,
        )
        return self.repository.update(
            db,
            ticket,
            data,
        )
    def delete_ticket(
        self,
        db: Session,
        ticket_id: int,
    ) -> None:
        ticket = self.get_ticket(
            db,
            ticket_id,
        )
        self.repository.delete(
            db,
            ticket,
        )