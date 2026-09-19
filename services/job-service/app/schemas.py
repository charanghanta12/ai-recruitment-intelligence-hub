from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class JobBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    required_skills: Optional[str] = None
    experience_required: int = 0
    location: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[str] = None
    experience_required: Optional[int] = None
    location: Optional[str] = None


class JobRead(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    candidate_id: int
    job_id: int


class ApplicationRead(ApplicationCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
