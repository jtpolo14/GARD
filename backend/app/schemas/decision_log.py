from datetime import datetime
from typing import Any

from pydantic import BaseModel


class DecisionLogResponse(BaseModel):
    id: str
    agent_id: str
    process_code: str | None
    input_data: Any
    rules_evaluated: Any
    rules_triggered: Any
    outcome: Any
    decision: str
    created_at: datetime

    model_config = {"from_attributes": True}
