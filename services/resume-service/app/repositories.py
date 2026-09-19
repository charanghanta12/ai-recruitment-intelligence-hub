from typing import Optional

from sqlalchemy.orm import Session

try:
    from app.models import Resume
except ImportError:  # pragma: no cover
    from models import Resume


class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, candidate_id: int, filename: str, file_data: bytes, content_text: str) -> Resume:
        resume = Resume(candidate_id=candidate_id, filename=filename, file_data=file_data, content_text=content_text)
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_by_candidate(self, candidate_id: int) -> Optional[Resume]:
        return self.db.query(Resume).filter(Resume.candidate_id == candidate_id).order_by(Resume.id.desc()).first()
