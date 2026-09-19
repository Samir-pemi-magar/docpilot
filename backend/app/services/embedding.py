import httpx

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.url = f"{settings.embedding_url}/embed"
        self.model = settings.embedding_model
        self.dimension = settings.embedding_dimension
        self.timeout = settings.embedding_timeout

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        payload = {
            "inputs": texts,
        }

        async with httpx.AsyncClient(
            timeout=self.timeout,
        ) as client:
            response = await client.post(
                self.url,
                json=payload,
            )

        response.raise_for_status()

        embeddings = response.json()

        if not isinstance(embeddings, list):
            raise ValueError("Embedding service returned an invalid response")

        if len(embeddings) != len(texts):
            raise ValueError(
                "Embedding service returned a different number of vectors "
                "than requested"
            )

        for embedding in embeddings:
            if not isinstance(embedding, list):
                raise ValueError(
                    "Embedding service returned an invalid vector"
                )

            if len(embedding) != self.dimension:
                raise ValueError(
                    f"Expected embedding dimension {self.dimension}, "
                    f"got {len(embedding)}"
                )

        return embeddings


embedding_service = EmbeddingService()
