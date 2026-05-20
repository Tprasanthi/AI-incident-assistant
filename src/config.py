import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()



@dataclass(frozen=True)
class Settings:
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")

    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "incident-rca-assistant")
    dynamodb_table_name: str = os.getenv("DYNAMODB_TABLE_NAME", "IncidentMetadata")
    sns_topic_arn: str = os.getenv("SNS_TOPIC_ARN", "")

    qdrant_url: str = os.getenv("QDRANT_URL", "[localhost](http://localhost:6333)")
    qdrant_api_key: str | None = os.getenv("QDRANT_API_KEY") or None
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "incident_chunks")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    otel_service_name: str = os.getenv("OTEL_SERVICE_NAME", "incident-rca-assistant")


settings = Settings()
