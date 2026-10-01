from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Document ingestion response."""

    document_id: UUID
    filename: str
    file_type: str
    chunking_strategy: str
    chunk_count: int
    status: str