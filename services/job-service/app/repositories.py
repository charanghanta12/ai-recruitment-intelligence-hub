from typing import List, Optional

from sqlalchemy.orm import Session

try:
    from app.models import Application, Job
    from app.schemas import ApplicationCreate, JobCreate, JobUpdate
except ImportError:  # pragma: no cover
    from models import Application, Job
    from schemas import ApplicationCreate, JobCreate, JobUpdate


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Job]:
        return self.db.query(Job).order_by(Job.id.desc()).all()

    def get(self, job_id: int) -> Optional[Job]:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def create(self, payload: JobCreate) -> Job:
        job = Job(**payload.model_dump())
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update(self, job_id: int, payload: JobUpdate) -> Optional[Job]:
        job = self.get(job_id)
        if job is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(job, field, value)
        self.db.commit()
        self.db.refresh(job)
        return job

    def delete(self, job_id: int) -> bool:
        job = self.get(job_id)
        if job is None:
            return False
        self.db.delete(job)
        self.db.commit()
        return True


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ApplicationCreate) -> Application:
        application = Application(**payload.model_dump())
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def list(self) -> List[Application]:
        return self.db.query(Application).order_by(Application.id.desc()).all()

    def get_job_applications(self, job_id: int) -> List[Application]:
        return self.db.query(Application).filter(Application.job_id == job_id).order_by(Application.id.desc()).all()
