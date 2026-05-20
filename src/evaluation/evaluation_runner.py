import json
from pathlib import Path
from src.analysis.analysis_lambda import lambda_handler


def keyword_score(text: str, keywords: list[str]) -> float:
    
    lowered = text.lower()
    hits = sum(1 for keyword in keywords if keyword.lower() in lowered)

    if not keywords:
        return 0.0

    return hits / len(keywords)


def run_eval() -> None:
    dataset_path = Path(__file__).parent / "golden_dataset.json"

    with open(dataset_path, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    scores = []

    for item in dataset:
        response = lambda_handler(
            {
                "incident_id": item["incident_id"],
                "query": "Analyze incident and identify root cause",
            },
            None,
        )

        body = json.loads(response["body"])
        analysis = body["analysis"]

        root_cause_score = keyword_score(
            analysis.get("probable_root_cause", ""),
            item["expected_root_cause_keywords"],
        )

        remediation_score = keyword_score(
            " ".join(analysis.get("remediation_steps", [])),
            item["expected_remediation_keywords"],
        )

        impacted_services_score = keyword_score(
            " ".join(analysis.get("impacted_services", [])),
            item["expected_impacted_services"],
        )

        final_score = (
            root_cause_score * 0.5
            + remediation_score * 0.3
            + impacted_services_score * 0.2
        )

        scores.append(
            {
                "incident_id": item["incident_id"],
                "root_cause_score": root_cause_score,
                "remediation_score": remediation_score,
                "impacted_services_score": impacted_services_score,
                "final_score": final_score,
            }
        )

    print(json.dumps(scores, indent=2))


if __name__ == "__main__":
    run_eval()
