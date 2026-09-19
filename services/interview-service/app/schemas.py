from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InterviewCreate(BaseModel):
    candidate_id: int
    job_id: int
    scheduled_at: datetime
    interview_type: str = "phone"
    status: str = "scheduled"
    feedback: Optional[str] = None


class InterviewUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    interview_type: Optional[str] = None
    status: Optional[str] = None
    feedback: Optional[str] = None


class InterviewRead(InterviewCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
