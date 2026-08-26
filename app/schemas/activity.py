from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ActivityStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class ActivityPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ActivityBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: ActivityPriority = ActivityPriority.MEDIUM

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[ActivityPriority] = None
    status: Optional[ActivityStatus] = None
    assignee_id: Optional[int] = None

class ActivityResponse(ActivityBase):
    id: int
    club_id: int
    assignee_id: Optional[int] = None
    status: ActivityStatus
    created_at: datetime

    class Config:
        from_attributes = True

class ActivityListResponse(BaseModel):
    total: int
    items: List[ActivityResponse]