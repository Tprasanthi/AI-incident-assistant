import json
import re
from datetime import datetime
from typing import Any


TIMESTAMP_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z"
)

SERVICE_PATTERN = re.compile(
    r"(auth-service|payment-service|user-service|order-service|inventory-service|postgres-primary|redis-cache)"
)


def infer_source_type(s3_key: str) -> str:
    lowered = s3_key.lower()

    if "log" in lowered:
        return "log"
    if "metric" in lowered:
        return "metric"
    if "alert" in lowered:
        return "alert"
    if "ticket" in lowered:
        return "ticket"
    if "deployment" in lowered:
        return "deployment"

    return "unknown"


def extract_incident_id(s3_key: str) -> str:
    parts = s3_key.split("/")

    for part in parts:
        if part.startswith("INC-"):
            return part

    return "UNKNOWN"


def extract_metadata(text: str, s3_key: str) -> dict[str, Any]:
    timestamps = TIMESTAMP_PATTERN.findall(text)
    services = list(set(SERVICE_PATTERN.findall(text)))

    first_timestamp = timestamps[0] if timestamps else None

    return {
        "incident_id": extract_incident_id(s3_key),
        "source_type": infer_source_type(s3_key),
        "services": services,
        "first_timestamp": first_timestamp,
        "s3_key": s3_key,
        "ingested_at": datetime.utcnow().isoformat() + "Z",
    }


def parse_json_if_possible(raw_text: str) -> str:
    try:
        obj = json.loads(raw_text)
        return json.dumps(obj, indent=2)
    except Exception:
        return raw_text
