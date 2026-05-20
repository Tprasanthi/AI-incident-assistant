import json
from src.analysis.graph import build_rca_graph
from src.storage.dynamodb_client import IncidentMetadataStore
from src.storage.s3_client import S3Storage
from src.notifications.sns_publisher import SnsPublisher
from src.observability.tracing import configure_tracing, get_tracer


configure_tracing()
tracer = get_tracer()


def lambda_handler(event, context):
    incident_id = event.get("incident_id")
    user_query = event.get("query", "Analyze this incident and identify root cause")

    if not incident_id:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": "incident_id is required",
                }
            ),
        }

    metadata_store = IncidentMetadataStore()
    
    s3 = S3Storage()
    sns = SnsPublisher()

    with tracer.start_as_current_span("analysis_lambda"):
        graph = build_rca_graph()

        final_state = graph.invoke(
            {
                "incident_id": incident_id,
                "user_query": user_query,
            }
        )

        analysis = final_state["final_result"]
        analysis_key = f"analysis/{incident_id}/result.json"

        s3.write_text(
            key=analysis_key,
            content=json.dumps(analysis, indent=2),
        )

        metadata_store.save_analysis(incident_id, analysis)
        sns.publish_incident_analysis(analysis)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "incident_id": incident_id,
                "analysis": analysis,
                "analysis_s3_key": analysis_key,
            }
        ),
    }
