from collections.abc import Callable


class ChunkingError(Exception):
    """Raised for invalid chunking configuration."""


def fixed_chunking(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    """Split text into fixed-size overlapping chunks."""

    if chunk_size <= 0:
        raise ChunkingError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ChunkingError(
            "overlap must be >= 0 and smaller than chunk_size."
        )

    chunks: list[str] = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def recursive_chunking(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    """Split text recursively using paragraph and sentence boundaries."""

    if not text.strip():
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 1 <= chunk_size:
            current = (
                f"{current}\n\n{paragraph}"
                if current
                else paragraph
            )
            continue

        if current:
            chunks.append(current.strip())

        if len(paragraph) <= chunk_size:
            current = paragraph
            continue

        sentences = paragraph.replace("!", ".").replace("?", ".").split(".")

        current = ""

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            if len(current) + len(sentence) + 1 <= chunk_size:
                current = (
                    f"{current} {sentence}"
                    if current
                    else sentence
                )
            else:
                if current:
                    chunks.append(current.strip())

                current = sentence

    if current:
        chunks.append(current.strip())

    if overlap == 0:
        return chunks

    return _add_overlap(chunks, overlap)


def _add_overlap(
    chunks: list[str],
    overlap: int,
) -> list[str]:
    """Add trailing overlap from the previous chunk."""

    if not chunks:
        return []

    result = [chunks[0]]

    for index in range(1, len(chunks)):
        previous = chunks[index - 1]
        prefix = previous[-overlap:]

        result.append(
            f"{prefix}\n{chunks[index]}"
        )

    return result


Chunker = Callable[[str, int, int], list[str]]


def get_chunker(strategy: str) -> Chunker:
    """Return a chunking function by strategy name."""

    strategies: dict[str, Chunker] = {
        "fixed": fixed_chunking,
        "recursive": recursive_chunking,
    }

    try:
        return strategies[strategy]
    except KeyError as exc:
        raise ChunkingError(
            f"Unknown chunking strategy: {strategy}"
        ) from exc