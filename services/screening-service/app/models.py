from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

try:
    from app.database import Base
except ImportError:  # pragma: no cover
    from database import Base


class Screening(Base):
    __tablename__ = "screenings"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False, index=True)
    job_id = Column(Integer, nullable=False, index=True)
    status = Column(String(50), default="processing", nullable=False)
    summary = Column(Text, nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
