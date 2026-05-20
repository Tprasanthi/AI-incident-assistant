import re

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{8,})"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def mask_sensitive_data(text: str) -> str:
    masked = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", text)
    masked = IP_PATTERN.sub("[IP_REDACTED]", masked)

    for pattern in SECRET_PATTERNS:
        masked = pattern.sub("[SECRET_REDACTED]", masked)

    return masked
