from typing import Any
from pydantic import BaseModel


class ValidationResult(BaseModel):
    success: bool
    tool: str
    data: dict[str, Any]
    markdown_summary: str
    execution_time_seconds: float
