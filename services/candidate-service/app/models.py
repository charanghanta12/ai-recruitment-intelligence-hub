from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, DateTime, Integer, String, Text

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from database import Base
else:
    from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    experience_years = Column(Integer, default=0)
    education = Column(String(255), nullable=True)
    skills = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
