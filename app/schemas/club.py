from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ClubMemberBase(BaseModel):
    role: str = "MEMBER"

class ClubMemberCreate(ClubMemberBase):
    user_id: int

class ClubMemberResponse(ClubMemberBase):
    club_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ClubBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ClubUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ClubResponse(ClubBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)