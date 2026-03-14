from datetime import datetime

from pydantic import BaseModel


class AgentBase(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class AgentResponse(AgentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
