import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config import settings


class VectorStore:
    """Qdrant vector database service."""

    def __init__(self) -> None:
        self.client = QdrantClient(
            url=settings.qdrant_url
        )
        self.collection_name = settings.qdrant_collection

    def ensure_collection(
        self,
        vector_size: int,
    ) -> None:
        """Create the collection if it does not exist."""

        collections = self.client.get_collections()

        exists = any(
            collection.name == self.collection_name
            for collection in collections.collections
        )

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add_chunks(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        document_id: str,
        filename: str,
    ) -> None:
        """Store document chunk vectors."""

        points: list[PointStruct] = []

        for index, (
            chunk,
            embedding,
        ) in enumerate(
            zip(chunks, embeddings, strict=True)
        ):
            point_id = str(uuid.uuid4())

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "document_id": document_id,
                        "filename": filename,
                        "chunk_index": index,
                        "text": chunk,
                    },
                )
            )

        if not points:
            return

        self.ensure_collection(
            vector_size=len(embeddings[0])
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        embedding: list[float],
        limit: int,
    ) -> list[dict[str, Any]]:
        """Search for semantically similar chunks."""

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            limit=limit,
            with_payload=True,
        ).points

        return [
            {
                "score": result.score,
                "text": result.payload.get("text", ""),
                "document_id": result.payload.get(
                    "document_id"
                ),
                "filename": result.payload.get(
                    "filename"
                ),
                "chunk_index": result.payload.get(
                    "chunk_index"
                ),
            }
            for result in results
        ]