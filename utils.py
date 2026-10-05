from datetime import datetime


def parse_slot(value: str) -> datetime:
    """Parse an ISO 8601 slot time, e.g. '2026-10-20T14:00'."""
    return datetime.fromisoformat(value)
