from datetime import datetime
from typing import Any

from pydantic import BaseModel


class DecisionRequest(BaseModel):
    agent: str
    process: str | None = None
    data: dict[str, Any]


class DecisionResponse(BaseModel):
    decision_id: str
    decision: str
    rules_triggered: list[str]
    actions: list[str]
    timestamp: datetime
