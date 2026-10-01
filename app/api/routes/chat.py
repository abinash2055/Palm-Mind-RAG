from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_booking_service,
    get_rag_service,
)
from app.db.database import get_db
from app.schema.chat import ChatRequest, ChatResponse, Source
from app.services.booking import BookingService
from app.services.rag import RAGService

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    rag_service: RAGService = Depends(
        get_rag_service
    ),
    booking_service: BookingService = Depends(
        get_booking_service
    ),
) -> ChatResponse:
    """Handle conversational RAG and interview booking."""

    # Add the new user message to temporary conversation
    # context for booking extraction.
    history = rag_service.memory.get_messages(
        request.session_id
    )

    conversation = [
        *history,
        {
            "role": "user",
            "content": request.message,
        },
    ]

    booking = booking_service.extract_details(
        conversation
    )

    has_booking_data = any(
        [
            booking.name,
            booking.email,
            booking.date,
            booking.time,
        ]
    )

    if has_booking_data:
        complete = all(
            [
                booking.name,
                booking.email,
                booking.date,
                booking.time,
            ]
        )

        if complete:
            saved = booking_service.save(
                db,
                booking,
            )

            answer = (
                "Your interview has been booked successfully. "
                f"Name: {saved.name}, "
                f"Email: {saved.email}, "
                f"Date: {saved.date}, "
                f"Time: {saved.time}."
            )

            rag_service.memory.add_message(
                request.session_id,
                "user",
                request.message,
            )

            rag_service.memory.add_message(
                request.session_id,
                "assistant",
                answer,
            )

            return ChatResponse(
                session_id=request.session_id,
                answer=answer,
                sources=[],
            )

    answer, sources = rag_service.answer(
        session_id=request.session_id,
        question=request.message,
    )

    return ChatResponse(
        session_id=request.session_id,
        answer=answer,
        sources=[
            Source(**source)
            for source in sources
        ],
    )