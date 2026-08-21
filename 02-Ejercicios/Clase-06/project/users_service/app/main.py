from fastapi import FastAPI

from app.config import settings
from app.routers.users import router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Microservicio encargado "
        "de la gestión de usuarios."
    ),
)


@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
    }


app.include_router(
    router,
    prefix="/api/v1",
)
