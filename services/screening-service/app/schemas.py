from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ScreeningCreate(BaseModel):
    candidate_id: int
    job_id: int


class AIEvaluation(BaseModel):
    summary: str
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    experience_analysis: str
    strengths: List[str] = Field(default_factory=list)
    areas_to_explore: List[str] = Field(default_factory=list)
    interview_questions: List[str] = Field(default_factory=list)


class ScreeningRead(BaseModel):
    screening_id: int
    candidate_id: Optional[int] = None
    job_id: Optional[int] = None
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
