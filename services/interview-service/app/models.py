from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

try:
    from app.database import Base
except ImportError:  # pragma: no cover
    from database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    interview_type = Column(String(100), default="phone")
    status = Column(String(50), default="scheduled")
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
