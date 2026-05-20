import urllib.parse
from src.storage.s3_client import S3Storage
from src.storage.qdrant_client import QdrantVectorStore
from src.storage.dynamodb_client import IncidentMetadataStore
from src.ingestion.pii_masker import mask_sensitive_data
from src.ingestion.metadata_extractor import (
    extract_metadata,
    parse_json_if_possible,
)
from src.ingestion.chunker import chunk_text
from src.observability.tracing import configure_tracing, get_tracer


configure_tracing()
tracer = get_tracer()


def lambda_handler(event, context):
    s3 = S3Storage()
    vector_store = QdrantVectorStore()
    metadata_store = IncidentMetadataStore()

    processed = []

    with tracer.start_as_current_span("s3_ingestion_lambda"):
        for record in event.get("Records", []):
            bucket = record["s3"]["bucket"]["name"]
            key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

            with tracer.start_as_current_span("process_s3_object"):
                raw_text = s3.read_text(key)
                normalized_text = parse_json_if_possible(raw_text)
                safe_text = mask_sensitive_data(normalized_text)

                metadata = extract_metadata(safe_text, key)
                incident_id = metadata["incident_id"]

                chunks = chunk_text(safe_text, metadata)
                vector_store.upsert_chunks(chunks)

                metadata_store.upsert_incident(
                    incident_id=incident_id,
                    attributes={
                        "status": "INGESTED",
                        "source_bucket": bucket,
                        "last_ingested_key": key,
                        "source_type": metadata["source_type"],
                        "services": metadata["services"],
                    },
                )

                processed.append(
                    {
                        "bucket": bucket,
                        "key": key,
                        "incident_id": incident_id,
                        "chunks_indexed": len(chunks),
                    }
                )

    return {
        "statusCode": 200,
        "body": {
            "processed": processed,
        },
    }
