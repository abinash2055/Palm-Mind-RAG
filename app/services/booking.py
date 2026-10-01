import json
from datetime import datetime
from uuid import UUID

from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Booking
from app.schema.booking import BookingDetails


class BookingService:
    """LLM-assisted interview booking service."""

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def extract_details(
        self,
        conversation: list[dict[str, str]],
    ) -> BookingDetails:
        """Extract booking information from conversation."""

        prompt = """
Extract interview booking information from the conversation.

Required fields:
- name
- email
- date
- time

Return ONLY valid JSON:

{
  "name": null,
  "email": null,
  "date": null,
  "time": null
}

Do not invent missing values.
"""

        response = self.client.responses.create(
            model=settings.openai_chat_model,
            input=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps(conversation),
                },
            ],
        )

        data = json.loads(
            response.output_text
        )

        return BookingDetails.model_validate(data)

    def save(
        self,
        db: Session,
        details: BookingDetails,
    ) -> Booking:
        """Save a completed booking."""

        if not all(
            [
                details.name,
                details.email,
                details.date,
                details.time,
            ]
        ):
            raise ValueError(
                "Incomplete booking details."
            )

        booking = Booking(
            name=details.name,
            email=str(details.email),
            date=details.date,
            time=details.time,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking