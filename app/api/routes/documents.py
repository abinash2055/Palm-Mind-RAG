from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_ingestion_service
from app.db.database import get_db
from app.schema.document import DocumentResponse
from app.services.chunker import ChunkingError
from app.services.ingestion import IngestionService
from app.services.parser import UnsupportedFileTypeError

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


@router.post(
    "/ingest",
    response_model=DocumentResponse,
)
async def ingest_document(
    file: Annotated[
        UploadFile,
        File(...),
    ],
    chunking_strategy: Annotated[
        str,
        Form(...),
    ],
    db: Session = Depends(get_db),
    ingestion_service: IngestionService = Depends(
        get_ingestion_service
    ),
) -> DocumentResponse:
    """Upload and ingest a TXT or PDF document."""

    filename = file.filename or ""

    if not filename.lower().endswith(
        (".pdf", ".txt")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    if chunking_strategy not in {
        "fixed",
        "recursive",
    }:
        raise HTTPException(
            status_code=400,
            detail=(
                "chunking_strategy must be "
                "'fixed' or 'recursive'."
            ),
        )

    content = await file.read()

    try:
        document = ingestion_service.ingest(
            db=db,
            filename=filename,
            content=content,
            chunking_strategy=chunking_strategy,
        )

    except (
        UnsupportedFileTypeError,
        ChunkingError,
        ValueError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return DocumentResponse(
        document_id=document.id,
        filename=document.filename,
        file_type=document.file_type,
        chunking_strategy=document.chunking_strategy,
        chunk_count=document.chunk_count,
        status="success",
    )