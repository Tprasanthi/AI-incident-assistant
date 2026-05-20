
---

#  Design Decisions and Tradeoffs


```markdown
# Design Decisions and Tradeoffs

## 1. LangGraph over single prompt

The RCA flow is implemented using LangGraph because incident analysis is naturally multi-step:

- Retrieve context
- Summarize
- Build timeline
- Detect anomalies
- Infer root cause
- Recommend remediation
- Decide escalation

This makes the system easier to debug, evaluate, and extend.

Tradeoff: LangGraph adds more implementation complexity than a single LLM call.

## 2. Qdrant for vector retrieval

Qdrant stores incident chunks and enables semantic search across logs, tickets, metrics, and alerts.

Tradeoff: For exact timestamp correlation, a time-series database would be better. This MVP uses Qdrant plus metadata filtering.

## 3. DynamoDB for incident state

DynamoDB is used for low-latency incident metadata and analysis state.

Tradeoff: It is not ideal for complex analytics queries, but works well for incident lookups and state tracking.

## 4. S3 as raw data source of truth

S3 stores raw and processed incident data.

Tradeoff: S3 is durable and cost-effective but not optimized for low-latency querying.

## 5. Rule-based anomaly detection plus LLM reasoning

The MVP uses lightweight pattern and metric threshold detection before LLM reasoning.

Tradeoff: This is simple and explainable, but less powerful than statistical anomaly detection or ML-based time-series models.

## 6. Human-in-the-loop escalation

The assistant marks low-confidence or high-impact incidents for human review.

Tradeoff: This avoids unsafe over-automation but may increase manual review volume.

## 7. PII and secret masking before indexing

Sensitive data is masked before embedding and storage.

Tradeoff: Masking can remove useful debugging context, but privacy and safety are higher priority.
