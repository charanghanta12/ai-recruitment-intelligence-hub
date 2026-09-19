from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

try:
    from app.database import Base, engine, get_db
    from app.repositories import ApplicationRepository, JobRepository
    from app.schemas import ApplicationCreate, ApplicationRead, JobCreate, JobRead, JobUpdate
except ImportError:  # pragma: no cover
    from database import Base, engine, get_db
    from repositories import ApplicationRepository, JobRepository
    from schemas import ApplicationCreate, ApplicationRead, JobCreate, JobRead, JobUpdate

try:
    Base.metadata.create_all(bind=engine)
except Exception:  # pragma: no cover
    pass


app = FastAPI(title="Job Service", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "job-service"}


@app.get("/api/jobs", response_model=List[JobRead])
async def list_jobs(db: Session = Depends(get_db)):
    return JobRepository(db).list()


@app.post("/api/jobs", response_model=JobRead, status_code=status.HTTP_201_CREATED)
async def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    return JobRepository(db).create(payload)


@app.get("/api/jobs/{job_id}", response_model=JobRead)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = JobRepository(db).get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.put("/api/jobs/{job_id}", response_model=JobRead)
async def update_job(job_id: int, payload: JobUpdate, db: Session = Depends(get_db)):
    job = JobRepository(db).update(job_id, payload)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    deleted = JobRepository(db).delete(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}


@app.post("/api/applications", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    return ApplicationRepository(db).create(payload)


@app.get("/api/applications", response_model=List[ApplicationRead])
async def list_applications(db: Session = Depends(get_db)):
    return ApplicationRepository(db).list()


@app.get("/api/jobs/{job_id}/applications", response_model=List[ApplicationRead])
async def get_job_applications(job_id: int, db: Session = Depends(get_db)):
    return ApplicationRepository(db).get_job_applications(job_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)
