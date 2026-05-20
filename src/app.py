import json
from fastapi import FastAPI
from pydantic import BaseModel

from src.analysis.analysis_lambda import lambda_handler as analyze_handler

app = FastAPI(
    title="AI Incident Root Cause Assistant",
    version="0.1.0",
)


class AnalyzeRequest(BaseModel):
    incident_id: str
    query: str | None = None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-incident-rca-assistant",
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    event = {
        "incident_id": request.incident_id,
        "query": request.query or "Analyze this incident and identify root cause",
    }

    response = analyze_handler(event, None)

    return json.loads(response["body"])
