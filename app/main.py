from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.documents import (
    router as documents_router,
)
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Custom conversational RAG backend "
        "with document ingestion and interview booking."
    ),
)

app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""

    return {
        "status": "ok",
        "service": settings.app_name,
    }