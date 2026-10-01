from openai import OpenAI

from app.core.config import settings


class EmbeddingService:
    """Generate embeddings using OpenAI."""

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def embed(self, text: str) -> list[float]:
        """Generate an embedding for one text."""

        response = self.client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text,
        )

        return response.data[0].embedding