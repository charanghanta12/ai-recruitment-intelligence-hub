from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

try:
    from app.database import Base, engine, get_db
    from app.repositories import InterviewRepository
    from app.schemas import InterviewCreate, InterviewRead, InterviewUpdate
except ImportError:  # pragma: no cover
    from database import Base, engine, get_db
    from repositories import InterviewRepository
    from schemas import InterviewCreate, InterviewRead, InterviewUpdate

try:
    Base.metadata.create_all(bind=engine)
except Exception:  # pragma: no cover
    pass


app = FastAPI(title="Interview Service", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "interview-service"}


@app.get("/api/interviews", response_model=List[InterviewRead])
async def list_interviews(db: Session = Depends(get_db)):
    return InterviewRepository(db).list()


@app.post("/api/interviews", response_model=InterviewRead, status_code=status.HTTP_201_CREATED)
async def create_interview(payload: InterviewCreate, db: Session = Depends(get_db)):
    return InterviewRepository(db).create(payload)


@app.get("/api/interviews/{interview_id}", response_model=InterviewRead)
async def get_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = InterviewRepository(db).get(interview_id)
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@app.put("/api/interviews/{interview_id}", response_model=InterviewRead)
async def update_interview(interview_id: int, payload: InterviewUpdate, db: Session = Depends(get_db)):
    interview = InterviewRepository(db).update(interview_id, payload)
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8005, reload=True)
