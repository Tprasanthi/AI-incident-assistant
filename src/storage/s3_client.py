import boto3
from src.config import settings


class S3Storage:
    def __init__(self) -> None:
        self.client = boto3.client("s3", region_name=settings.aws_region)

    def read_text(self, key: str) -> str:
        response = self.client.get_object(
            Bucket=settings.s3_bucket_name,
            Key=key,
        )
        return response["Body"].read().decode("utf-8")

    def write_text(self, key: str, content: str) -> None:
        self.client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=key,
            Body=content.encode("utf-8"),
            ContentType="application/json",
        )
