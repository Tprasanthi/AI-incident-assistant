from src.storage.qdrant_client import QdrantVectorStore


class IncidentRetriever:
    def __init__(self) -> None:
        self.vector_store = QdrantVectorStore()
        

    def retrieve_incident_context(self, incident_id: str, query: str) -> list[dict]:
        search_queries = [
            query,
            "errors latency deployment database timeout memory cpu alerts metrics",
            "root cause incident timeline impacted services remediation",
        ]

        all_results = []

        for search_query in search_queries:
            results = self.vector_store.search(
                query=search_query,
                incident_id=incident_id,
                limit=6,
            )
            all_results.extend(results)

        deduped = {}
        for item in all_results:
            text = item["text"]
            deduped[text] = item

        return list(deduped.values())[:12]


def format_context(results: list[dict]) -> str:
    formatted = []

    for index, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})
        formatted.append(
            f"""
[Context {index}]
source_type: {metadata.get("source_type")}
service: {metadata.get("services")}
timestamp: {metadata.get("first_timestamp")}
score: {result.get("score")}
text:
{result.get("text")}
"""
        )

    return "\n".join(formatted)
