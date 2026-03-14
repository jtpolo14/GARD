from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RuleBase(BaseModel):
    code: str
    name: str
    description: str | None = None
    process_id: str | None = None
    logic: dict[str, Any]
    action: str
    priority: int = 100
    status: str = "active"


class RuleCreate(RuleBase):
    pass


class RuleUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    process_id: str | None = None
    logic: dict[str, Any] | None = None
    action: str | None = None
    priority: int | None = None
    status: str | None = None


class RuleResponse(RuleBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
