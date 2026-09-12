from pydantic import BaseModel
from datetime import datetime


class AuditLogCreate(BaseModel):
    action: str
    description: str
    user: str | None = None
    work_id: str | None = None


class AuditLogResponse(BaseModel):
    id: int
    action: str
    description: str
    user: str | None = None
    work_id: str | None = None
    created_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }