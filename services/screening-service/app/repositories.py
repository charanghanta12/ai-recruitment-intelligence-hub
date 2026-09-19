from typing import Optional

from sqlalchemy.orm import Session

try:
    from app.models import Screening
except ImportError:  # pragma: no cover
    from models import Screening


class ScreeningRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, candidate_id: int, job_id: int) -> Screening:
        screening = Screening(candidate_id=candidate_id, job_id=job_id, status="processing")
        self.db.add(screening)
        self.db.commit()
        self.db.refresh(screening)
        return screening

    def get(self, screening_id: int) -> Optional[Screening]:
        return self.db.query(Screening).filter(Screening.id == screening_id).first()

    def list(self) -> list[Screening]:
        return self.db.query(Screening).order_by(Screening.id.desc()).all()

    def update_result(self, screening_id: int, status: str, result: dict | None = None, error: str | None = None) -> Optional[Screening]:
        screening = self.get(screening_id)
        if screening is None:
            return None
        screening.status = status
        if result is not None:
            screening.result = result
        if error is not None:
            screening.error = error
        self.db.commit()
        self.db.refresh(screening)
        return screening
