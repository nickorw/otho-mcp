"""
Shared timing utilities for duration formatting.
"""

from datetime import datetime
from typing import Optional


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "30.5s", "2m 30s", or "1h 5m 30s"
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    # Round to nearest second for durations >= 60s
    total_seconds = round(seconds)
    minutes, secs = divmod(total_seconds, 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"

    hours, mins = divmod(minutes, 60)
    return f"{hours}h {mins}m {secs}s"


def calculate_duration_seconds(
    start_time: Optional[str], end_time: Optional[str]
) -> Optional[float]:
    """
    Calculate duration in seconds between two ISO format timestamps.

    Args:
        start_time: ISO format start timestamp string (or None)
        end_time: ISO format end timestamp string (or None)

    Returns:
        Duration in seconds, or None if timestamps are missing or invalid
    """
    if not start_time or not end_time:
        return None

    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        return (end - start).total_seconds()
    except (ValueError, TypeError):
        return None
