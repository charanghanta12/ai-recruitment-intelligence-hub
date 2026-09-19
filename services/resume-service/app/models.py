from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String, Text

try:
    from app.database import Base
except ImportError:  # pragma: no cover
    from database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_data = Column(LargeBinary, nullable=False)
    content_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
