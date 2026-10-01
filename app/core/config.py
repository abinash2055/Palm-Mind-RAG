from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    app_name: str = "Palm Mind RAG API"
    app_env: str = "development"

    database_url: str
    redis_url: str

    qdrant_url: str
    qdrant_collection: str = "document_chunks"

    openai_api_key: str
    openai_chat_model: str = "gpt-5"
    openai_embedding_model: str = "text-embedding-3-small"

    top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()