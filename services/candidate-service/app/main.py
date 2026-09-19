import sys
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from database import Base, engine, get_db
    from repositories import CandidateRepository
    from schemas import CandidateCreate, CandidateRead, CandidateUpdate
else:
    from app.database import Base, engine, get_db
    from app.repositories import CandidateRepository
    from app.schemas import CandidateCreate, CandidateRead, CandidateUpdate

try:
    Base.metadata.create_all(bind=engine)
except Exception:  # pragma: no cover
    pass


app = FastAPI(title="Candidate Service", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "candidate-service"}


@app.get("/api/candidates", response_model=List[CandidateRead])
async def list_candidates(db: Session = Depends(get_db)):
    return CandidateRepository(db).list()


@app.post("/api/candidates", response_model=CandidateRead, status_code=status.HTTP_201_CREATED)
async def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    try:
        return CandidateRepository(db).create(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@app.get("/api/candidates/{candidate_id}", response_model=CandidateRead)
async def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = CandidateRepository(db).get(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.put("/api/candidates/{candidate_id}", response_model=CandidateRead)
async def update_candidate(candidate_id: int, payload: CandidateUpdate, db: Session = Depends(get_db)):
    candidate = CandidateRepository(db).update(candidate_id, payload)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.delete("/api/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    deleted = CandidateRepository(db).delete(candidate_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted successfully"}


@app.get("/api/candidates/search")
async def search_candidates(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return CandidateRepository(db).search(q)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
