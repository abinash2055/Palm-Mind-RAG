from app.services.chunker import (
    fixed_chunking,
    recursive_chunking,
)


def test_fixed_chunking():
    text = "A" * 2500

    chunks = fixed_chunking(
        text,
        chunk_size=1000,
        overlap=100,
    )

    assert len(chunks) > 1
    from app.services.chunker import (
    fixed_chunking,
    recursive_chunking,
)


def test_fixed_chunking():
    text = "A" * 2500

    chunks = fixed_chunking(
        text,
        chunk_size=1000,
        overlap=100,
    )

    assert len(chunks) > 1
    assert all(chunks)