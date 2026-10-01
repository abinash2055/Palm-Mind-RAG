from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Document
from app.services.chunker import get_chunker
from app.services.embeddings import EmbeddingService
from app.services.parser import extract_text
from app.services.vector_store import VectorStore


class IngestionService:
    """Document ingestion pipeline."""

    def __init__(self) -> None:
        self.embeddings = EmbeddingService()
        self.vector_store = VectorStore()

    def ingest(
        self,
        db: Session,
        filename: str,
        content: bytes,
        chunking_strategy: str,
    ) -> Document:
        """Extract, chunk, embed and store a document."""

        text = extract_text(
            filename=filename,
            content=content,
        )

        if not text.strip():
            raise ValueError(
                "Document contains no extractable text."
            )

        chunker = get_chunker(
            chunking_strategy
        )

        chunks = chunker(
            text,
            chunk_size=1000,
            overlap=200,
        )

        if not chunks:
            raise ValueError(
                "No chunks were generated."
            )

        embeddings = [
            self.embeddings.embed(chunk)
            for chunk in chunks
        ]

        document = Document(
            filename=filename,
            file_type=filename.rsplit(".", 1)[-1].lower(),
            chunking_strategy=chunking_strategy,
            chunk_count=len(chunks),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            document_id=str(document.id),
            filename=filename,
        )

        return document