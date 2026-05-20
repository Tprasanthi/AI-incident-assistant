import re
from typing import Any


ERROR_PATTERNS = [
    "ERROR",
    "Exception",
    "timeout",
    "connection refused",
    "connection pool exhausted",
    "OutOfMemory",
    "OOMKilled",
    "5xx",
    "latency",
    "throttling",
    "rate limit",
]

METRIC_PATTERNS = {
    "high_cpu": re.compile(r"cpu(?:_usage)?[=: ]+(9\d|100)%?", re.IGNORECASE),
    "high_memory": re.compile(r"memory(?:_usage)?[=: ]+(9\d|100)%?", re.IGNORECASE),
    "high_latency": re.compile(r"p95_latency_ms[=: ]+([1-9]\d{3,})", re.IGNORECASE),
    "high_error_rate": re.compile(r"error_rate[=: ]+([1-9]\d?)%", re.IGNORECASE),
    "db_connections": re.compile(r"db_connections_used[=: ]+(9\d|100)%?", re.IGNORECASE),
}



def detect_anomalies(context_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    anomalies = []

    for item in context_items:
        text = item.get("text", "")
        metadata = item.get("metadata", {})

        for pattern in ERROR_PATTERNS:
            if pattern.lower() in text.lower():
                anomalies.append(
                    {
                        "signal": pattern,
                        "service": metadata.get("services", ["unknown"]),
                        "timestamp": metadata.get("first_timestamp", "unknown"),
                        "description": text[:300],
                    }
                )

        for signal, regex in METRIC_PATTERNS.items():
            if regex.search(text):
                anomalies.append(
                    {
                        "signal": signal,
                        "service": metadata.get("services", ["unknown"]),
                        "timestamp": metadata.get("first_timestamp", "unknown"),
                        "description": text[:300],
                    }
                )

    return anomalies[:15]
