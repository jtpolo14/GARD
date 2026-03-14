from datetime import datetime

from pydantic import BaseModel


class ProcessBase(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True


class ProcessCreate(ProcessBase):
    pass


class ProcessUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ProcessResponse(ProcessBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
