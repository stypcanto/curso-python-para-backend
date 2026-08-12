from time import perf_counter

from fastapi import FastAPI, Request

# Importar los 3 modelos ACÁ (antes de que se use cualquier Ticket de
# verdad) — si no, sale InvalidRequestError al crear el primer ticket
from models.user import User
from models.category import Category
from models.ticket import Ticket

from routers.tickets import router as tickets_router

# Las tablas ya NO se crean acá con create_all() — las crea/actualiza
# Alembic (migrations/), corriendo "alembic upgrade head" a mano antes
# de levantar la app. Es la forma versionada de mantener el esquema.


# ---------------------------------------------------------
# CREACIÓN DE LA APLICACIÓN
# ---------------------------------------------------------

app = FastAPI(
    title="HelpDesk API",
    description=(
        "API REST para la gestión de solicitudes "
        "de soporte técnico utilizando FastAPI, "
        "SQLAlchemy y PostgreSQL."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------

@app.middleware("http")
async def add_process_time(
    request: Request,
    call_next,
):
    """
    Mide el tiempo total utilizado para procesar
    cada solicitud HTTP.
    """

    start = perf_counter()

    response = await call_next(request)

    elapsed = perf_counter() - start

    response.headers[
        "X-Process-Time"
    ] = f"{elapsed:.6f}"

    return response


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    """
    Permite verificar que la API se encuentre funcionando.
    """

    return {
        "status": "ok",
        "service": "HelpDesk API",
        "version": "1.0.0",
    }


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

app.include_router(
    tickets_router,
    prefix="/api/v1",
)