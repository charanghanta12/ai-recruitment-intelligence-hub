import sys
from pathlib import Path
from typing import List, Optional

from sqlalchemy.orm import Session

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from models import Candidate
    from schemas import CandidateCreate, CandidateUpdate
else:
    from app.models import Candidate
    from app.schemas import CandidateCreate, CandidateUpdate


class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Candidate]:
        return self.db.query(Candidate).order_by(Candidate.id.desc()).all()

    def get(self, candidate_id: int) -> Optional[Candidate]:
        return self.db.query(Candidate).filter(Candidate.id == candidate_id).first()

    def create(self, payload: CandidateCreate) -> Candidate:
        candidate = Candidate(**payload.model_dump())
        self.db.add(candidate)
        self.db.commit()
        self.db.refresh(candidate)
        return candidate

    def update(self, candidate_id: int, payload: CandidateUpdate) -> Optional[Candidate]:
        candidate = self.get(candidate_id)
        if candidate is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(candidate, field, value)
        self.db.commit()
        self.db.refresh(candidate)
        return candidate

    def delete(self, candidate_id: int) -> bool:
        candidate = self.get(candidate_id)
        if candidate is None:
            return False
        self.db.delete(candidate)
        self.db.commit()
        return True

    def search(self, q: str) -> List[Candidate]:
        term = f"%{q.lower()}%"
        return (
            self.db.query(Candidate)
            .filter(
                (Candidate.name.ilike(term))
                | (Candidate.email.ilike(term))
                | (Candidate.skills.ilike(term))
            )
            .order_by(Candidate.id.desc())
            .all()
        )
