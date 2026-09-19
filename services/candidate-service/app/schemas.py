from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class CandidateBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: Optional[str] = None
    experience_years: int = 0
    education: Optional[str] = None
    skills: Optional[str] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    experience_years: Optional[int] = None
    education: Optional[str] = None
    skills: Optional[str] = None


class CandidateRead(CandidateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
