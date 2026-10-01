from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat message."""

    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class Source(BaseModel):
    """Retrieved source information."""

    document_id: str | None
    filename: str | None
    score: float


class ChatResponse(BaseModel):
    """Chat response."""

    session_id: str
    answer: str
    sources: list[Source]