from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_openai import OpenAIEmbeddings
from src.config import settings
import uuid


EMBEDDING_DIMENSION = 1536


class QdrantVectorStore:
    def __init__(self) -> None:
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    def ensure_collection(self) -> None:
        collections = self.client.get_collections().collections
        names = [collection.name for collection in collections]

        if settings.qdrant_collection not in names:
            self.client.create_collection(
                collection_name=settings.qdrant_collection,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )

    def upsert_chunks(self, chunks: list[dict]) -> None:
        self.ensure_collection()

        texts = [chunk["text"] for chunk in chunks]
        vectors = self.embeddings.embed_documents(texts)

        points = []

        for chunk, vector in zip(chunks, vectors):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "text": chunk["text"],
                        **chunk["metadata"],
                    },
                )
            )

        self.client.upsert(
            collection_name=settings.qdrant_collection,
            points=points,
        )

    def search(self, query: str, incident_id: str, limit: int = 8) -> list[dict]:
        query_vector = self.embeddings.embed_query(query)

        results = self.client.search(
            collection_name=settings.qdrant_collection,
            query_vector=query_vector,
            query_filter={
                "must": [
                    {
                        "key": "incident_id",
                        "match": {
                            "value": incident_id,
                        },
                    }
                ]
            },
            limit=limit,
        )

        return [
            {
                "score": item.score,
                "text": item.payload.get("text", ""),
                "metadata": item.payload,
            }
            for item in results
        ]
