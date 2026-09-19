from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ResumeRead(BaseModel):
    id: int
    candidate_id: int
    filename: str
    content_text: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True
