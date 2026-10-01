from app.services.embeddings import EmbeddingService
from app.services.llm import LLMService
from app.services.memory import ChatMemory
from app.services.vector_store import VectorStore


class RAGService:
    """Custom conversational RAG implementation."""

    def __init__(self) -> None:
        self.embeddings = EmbeddingService()
        self.vector_store = VectorStore()
        self.memory = ChatMemory()
        self.llm = LLMService()

    def answer(
        self,
        session_id: str,
        question: str,
    ) -> tuple[str, list[dict]]:
        """Generate a response using retrieval and conversation memory."""

        query_embedding = self.embeddings.embed(
            question
        )

        retrieved = self.vector_store.search(
            embedding=query_embedding,
            limit=5,
        )

        history = self.memory.get_messages(
            session_id
        )

        context = "\n\n".join(
            (
                f"Source: {item['filename']}\n"
                f"{item['text']}"
            )
            for item in retrieved
        )

        system_prompt = """
You are a helpful conversational assistant.

Answer the user's question using the supplied document
context and conversation history.

Rules:
1. Prefer information from the retrieved context.
2. If the answer is not contained in the context, say
   that the information is not available in the documents.
3. Do not invent facts.
4. Use conversation history to understand follow-up questions.
5. Keep answers clear and concise.

Retrieved document context:
"""

        system_prompt += context

        messages = [
            *history,
            {
                "role": "user",
                "content": question,
            },
        ]

        answer = self.llm.generate(
            system_prompt=system_prompt,
            messages=messages,
        )

        self.memory.add_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        self.memory.add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        sources = [
            {
                "document_id": item["document_id"],
                "filename": item["filename"],
                "score": item["score"],
            }
            for item in retrieved
        ]

        return answer, sources