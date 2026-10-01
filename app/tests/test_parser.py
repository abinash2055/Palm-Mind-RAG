import pytest

from app.services.parser import (
    UnsupportedFileTypeError,
    extract_text,
)


def test_extract_txt():
    content = b"Hello Palm Mind"

    result = extract_text(
        "test.txt",
        content,
    )

    assert result == "Hello Palm Mind"


def test_unsupported_file():
    with pytest.raises(
        UnsupportedFileTypeError
    ):
        extract_text(
            "test.jpg",
            b"image",
        )