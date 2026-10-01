from io import BytesIO
from pathlib import Path

import fitz


class UnsupportedFileTypeError(Exception):
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

    raise UnsupportedFileTypeError(
        f"Unsupported file type: {extension}"
    )