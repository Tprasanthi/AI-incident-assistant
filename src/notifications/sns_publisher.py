import json
import boto3
from src.config import settings


class SnsPublisher:
    def __init__(self) -> None:
        self.client = boto3.client("sns", region_name=settings.aws_region)

    def publish_incident_analysis(self, analysis: dict) -> None:
        if not settings.sns_topic_arn:
            return

        message = {
            "incident_id": analysis.get("incident_id"),
            "severity": analysis.get("severity"),
            "summary": analysis.get("summary"),
            "probable_root_cause": analysis.get("probable_root_cause"),
            "confidence": analysis.get("confidence"),
            "needs_human_review": analysis.get("needs_human_review"),
        }

        self.client.publish(
            TopicArn=settings.sns_topic_arn,
            Subject=f"Incident RCA: {analysis.get('incident_id')}",
            Message=json.dumps(message, indent=2),
        )
