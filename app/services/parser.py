from io import BytesIO
from pathlib import Path

import fitz
from docx import Document


class  UnsupportedFileTypeError(Exception):
    """Raised when a file type is not supported."""


def extract_text(
        filename: str,
        content: bytes,
) -> str:
    """Extract text from TXT or PDF content."""

    extension = Path(filename).suffix.lower()

    if extension == ".txt":
        return content.decode("utf-8")

    if extension == ".pdf":
        document = fitz.open(
            stream=BytesIO(content),
            filetype="pdf",
        )

        pages = [
            page.get_text()
            for page in document
        ]

        document.close()

        return "\n".join(pages)

    if extension == ".docx":
        document = Document(BytesIO(content))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        return "\n".join(paragraphs)
    

    raise UnsupportedFileTypeError(
        f"Unsupported file type: {extension}"
    )