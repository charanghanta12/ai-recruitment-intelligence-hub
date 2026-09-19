from typing import List, Optional

from sqlalchemy.orm import Session

try:
    from app.models import Interview
    from app.schemas import InterviewCreate, InterviewUpdate
except ImportError:  # pragma: no cover
    from models import Interview
    from schemas import InterviewCreate, InterviewUpdate


class InterviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Interview]:
        return self.db.query(Interview).order_by(Interview.id.desc()).all()

    def get(self, interview_id: int) -> Optional[Interview]:
        return self.db.query(Interview).filter(Interview.id == interview_id).first()

    def create(self, payload: InterviewCreate) -> Interview:
        interview = Interview(**payload.model_dump())
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)
        return interview

    def update(self, interview_id: int, payload: InterviewUpdate) -> Optional[Interview]:
        interview = self.get(interview_id)
        if interview is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(interview, field, value)
        self.db.commit()
        self.db.refresh(interview)
        return interview
