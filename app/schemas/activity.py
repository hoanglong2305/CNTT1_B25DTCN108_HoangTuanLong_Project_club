from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    club_id: int

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

class ActivityResponse(ActivityBase):
    id: int
    club_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)