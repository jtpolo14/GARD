from datetime import datetime

from pydantic import BaseModel


class PolicyBase(BaseModel):
    code: str
    name: str
    description: str | None = None
    process_id: str | None = None
    is_active: bool = True


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    process_id: str | None = None
    is_active: bool | None = None


class PolicyResponse(PolicyBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
