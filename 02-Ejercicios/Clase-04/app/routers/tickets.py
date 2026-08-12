from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from repositories.ticket_repository import TicketRepository
from schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


# El service necesita un repository — se arma acá y FastAPI lo inyecta
# en cada endpoint con Depends(), igual que la sesión de base de datos.
def get_ticket_service() -> TicketService:
    return TicketService(repository=TicketRepository())


@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.list_tickets(db)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.get_ticket(db, ticket_id)


@router.post("/", response_model=TicketResponse, status_code=201)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.create_ticket(db, data)


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    return service.update_ticket(db, ticket_id, data)


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    service: TicketService = Depends(get_ticket_service),
):
    service.delete_ticket(db, ticket_id)
