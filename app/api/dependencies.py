from functools import lru_cache

from app.services.booking import BookingService
from app.services.ingestion import IngestionService
from app.services.rag import RAGService


@lru_cache
def get_ingestion_service() -> IngestionService:
    return IngestionService()


@lru_cache
def get_rag_service() -> RAGService:
    return RAGService()


@lru_cache
def get_booking_service() -> BookingService:
    return BookingService()