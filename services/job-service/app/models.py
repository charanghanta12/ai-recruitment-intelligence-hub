from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

try:
    from app.database import Base
except ImportError:  # pragma: no cover
    from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    required_skills = Column(Text, nullable=True)
    experience_required = Column(Integer, default=0)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)
    status = Column(String(50), default="applied")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
