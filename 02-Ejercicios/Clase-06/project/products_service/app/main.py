from fastapi import FastAPI

from app.config import settings
from app.routers.products import router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Microservicio encargado "
        "del catálogo de productos."
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
