from time import perf_counter  # para medir cuánto tarda cada petición (middleware)

from fastapi import FastAPI, Request

# Importar los 3 modelos ACÁ (antes de que se use cualquier Ticket de
# verdad) — si no, sale InvalidRequestError al crear el primer ticket
from models.user import User
from models.category import Category
from models.ticket import Ticket

# El router YA TRAE sus 5 endpoints armados (routers/tickets.py) — acá
# solo se importa para montarlo más abajo con app.include_router(...)
from routers.tickets import router as tickets_router

# Las tablas ya NO se crean acá con create_all() — las crea/actualiza
# Alembic (migrations/), corriendo "alembic upgrade head" a mano antes
# de levantar la app. Es la forma versionada de mantener el esquema.


# ---------------------------------------------------------
# CREACIÓN DE LA APLICACIÓN
# ---------------------------------------------------------

# Esta ÚNICA instancia es la "app" — el objeto al que se le cuelgan
# middleware, endpoints propios (/health) y routers enteros (Tickets).
# title/description/version alimentan directo el Swagger de /docs.
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
    call_next,  # la función que sigue la cadena — el endpoint real
):
    """
    Mide el tiempo total utilizado para procesar
    cada solicitud HTTP.
    """

    start = perf_counter()  # arranca el cronómetro ANTES del endpoint

    response = await call_next(request)  # acá corre el endpoint (health/tickets)

    elapsed = perf_counter() - start  # cuánto tardó, en segundos

    response.headers[
        "X-Process-Time"
    ] = f"{elapsed:.6f}"  # se agrega a TODAS las respuestas, sin excepción

    return response


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

# Endpoint DIRECTO sobre "app" (no viene de un router) — por eso su URL
# final es solo /health, sin el prefijo /api/v1 que sí lleva Tickets.
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
        "service": "El API backend de HelpDesk esta operativo",
        "version": "1.0.0",
    }


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

# La línea que "genera" los 5 endpoints finales: toma TODAS las rutas ya
# definidas en tickets_router (con su propio prefix="/tickets") y las
# cuelga de "app" bajo /api/v1 -> URL real = /api/v1/tickets/...
app.include_router(
    tickets_router,
    prefix="/api/v1",
)