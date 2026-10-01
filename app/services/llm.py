from collections.abc import Sequence

from openai import OpenAI

from app.core.config import settings


class LLMService:
    """Service responsible for LLM interactions."""

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def generate(
        self,
        system_prompt: str,
        messages: Sequence[dict[str, str]],
    ) -> str:
        """Generate an LLM response."""

        input_messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            *messages,
        ]

        response = self.client.responses.create(
            model=settings.openai_chat_model,
            input=input_messages,
        )

        return response.output_text