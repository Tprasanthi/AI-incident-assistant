SUMMARY_PROMPT = """
You are an expert senior site reliability engineer.

Analyze the incident context and produce a concise incident summary.

Return:
- One paragraph summary
- Impacted services
- Customer/business impact if available
- Severity estimate

Incident context:
{context}
"""


TIMELINE_PROMPT = """
You are analyzing production incident telemetry.

Extract a chronological timeline of key events.
Focus on timestamps, deployments, alerts, error spikes, metric anomalies, and recovery signals.

Return JSON array format:
[
  {{
    "timestamp": "ISO timestamp or unknown",
    "event": "description",
    "source": "log/metric/alert/ticket/deployment"
  }}
]

Incident context:
{context}
"""



ROOT_CAUSE_PROMPT = """
You are an expert incident commander and distributed systems engineer.

Given the summary, timeline, anomalies, and retrieved telemetry, infer the most probable root cause.

Consider:
- Deployment timing
- Error propagation
- Dependency failures
- Resource saturation
- Database/network issues
- Misconfiguration
- Retry storms
- Cascading failures

Return:
- Probable root cause
- Evidence
- Alternative hypotheses
- Confidence from 0.0 to 1.0
- Reasoning

Incident ID: {incident_id}

Summary:
{summary}

Timeline:
{timeline}

Anomalies:
{anomalies}

Context:
{context}
"""


REMEDIATION_PROMPT = """
You are a senior production engineer.

Recommend concrete remediation steps for this incident.
Separate immediate mitigation from long-term prevention.

Root cause:
{root_cause}

Summary:
{summary}

Anomalies:
{anomalies}

Return concise actionable steps.
"""


FINAL_OUTPUT_PROMPT = """
Create a final structured JSON incident analysis.

Use this schema:
{{
  "incident_id": "...",
  "severity": "SEV1|SEV2|SEV3|SEV4",
  "summary": "...",
  "impacted_services": ["..."],
  "timeline": [
    {{
      "timestamp": "...",
      "event": "...",
      "source": "..."
    }}
  ],
  "anomalies": [
    {{
      "signal": "...",
      "service": "...",
      "timestamp": "...",
      "description": "..."
    }}
  ],
  "probable_root_cause": "...",
  "alternative_causes": ["..."],
  "remediation_steps": ["..."],
  "confidence": 0.0,
  "needs_human_review": true,
  "reasoning": "..."
}}

Rules:
- Be factual and evidence-based.
- Do not invent telemetry that is not present.
- If evidence is weak, lower confidence.
- Set needs_human_review=true when confidence < 0.65 or impact is severe.
- Output valid JSON only.

Incident ID:
{incident_id}

Summary:
{summary}

Timeline:
{timeline}

Anomalies:
{anomalies}

Root cause:
{root_cause}

Remediation:
{remediation}
"""
