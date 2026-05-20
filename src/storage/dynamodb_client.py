import boto3
from datetime import datetime
from src.config import settings


class IncidentMetadataStore:
    def __init__(self) -> None:
        dynamodb = boto3.resource("dynamodb", region_name=settings.aws_region)
        self.table = dynamodb.Table(settings.dynamodb_table_name)

    def upsert_incident(self, incident_id: str, attributes: dict) -> None:
        now = datetime.utcnow().isoformat() + "Z"

        item = {
            "incident_id": incident_id,
            "updated_at": now,
            **attributes,
        }

        if "created_at" not in item:
            item["created_at"] = now

        self.table.put_item(Item=item)

    def get_incident(self, incident_id: str) -> dict | None:
        response = self.table.get_item(Key={"incident_id": incident_id})
        return response.get("Item")

    def save_analysis(self, incident_id: str, analysis: dict) -> None:
        now = datetime.utcnow().isoformat() + "Z"

        self.table.update_item(
            Key={"incident_id": incident_id},
            UpdateExpression="""
                SET #status = :status,
                    analysis = :analysis,
                    needs_human_review = :needs_human_review,
                    updated_at = :updated_at
            """,
            ExpressionAttributeNames={
                "#status": "status",
            },
            ExpressionAttributeValues={
                ":status": "ANALYZED",
                ":analysis": analysis,
                ":needs_human_review": analysis.get("needs_human_review", False),
                ":updated_at": now,
            },
        )
