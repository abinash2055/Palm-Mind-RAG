import json

import redis

from app.core.config import settings


class ChatMemory:
    """Redis-backed conversational memory."""

    def __init__(self) -> None:
        self.redis = redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    def _key(self, session_id: str) -> str:
        return f"chat:{session_id}"

    def get_messages(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:
        """Return conversation history."""

        raw_messages = self.redis.lrange(
            self._key(session_id),
            0,
            -1,
        )

        return [
            json.loads(message)
            for message in raw_messages
        ]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        """Store one conversation message."""

        message = json.dumps(
            {
                "role": role,
                "content": content,
            }
        )

        key = self._key(session_id)

        self.redis.rpush(key, message)

        # Keep a reasonable conversation size.
        self.redis.ltrim(key, -20, -1)

        # Expire inactive conversations after 24 hours.
        self.redis.expire(key, 86400)

    def clear(
        self,
        session_id: str,
    ) -> None:
        """Delete conversation history."""

        self.redis.delete(
            self._key(session_id)
        )