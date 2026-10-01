from pydantic import BaseModel, EmailStr


class BookingDetails(BaseModel):
    """Interview booking information."""

    name: str | None = None
    email: EmailStr | None = None
    date: str | None = None
    time: str | None = None


class BookingResponse(BaseModel):
    """Stored booking response."""

    booking_id: str
    name: str
    email: str
    date: str
    time: str