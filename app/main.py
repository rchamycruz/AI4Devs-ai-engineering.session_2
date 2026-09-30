from fastapi import FastAPI

from app.config import get_settings
from app.routers import estimations

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Genera estimaciones de proyectos de software a partir de transcripciones de reuniones. "
        "Arquitectura CAG: los ejemplos de estimaciones previas se inyectan como contexto estático "
        "en cada llamada al LLM."
    ),
    version="0.1.0",
)

app.include_router(estimations.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok", "provider": settings.llm_provider, "model": settings.active_model}
