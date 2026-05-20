from typing import TypedDict, Any
from pydantic import BaseModel, Field



class RCAState(TypedDict, total=False):
    incident_id: str
    user_query: str
    retrieved_context: list[dict[str, Any]]
    summary: str
    timeline: list[dict[str, str]]
    anomalies: list[dict[str, Any]]
    probable_root_cause: str
    alternative_causes: list[str]
    remediation_steps: list[str]
    confidence: float
    severity: str
    impacted_services: list[str]
    needs_human_review: bool
    final_result: dict[str, Any]


class IncidentAnalysisOutput(BaseModel):
    incident_id: str
    severity: str = Field(description="SEV1, SEV2, SEV3, or SEV4")
    summary: str
    impacted_services: list[str]
    timeline: list[dict[str, str]]
    anomalies: list[dict[str, Any]]
    probable_root_cause: str
    alternative_causes: list[str]
    remediation_steps: list[str]
    confidence: float
    needs_human_review: bool
    reasoning: str
