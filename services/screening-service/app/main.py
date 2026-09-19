from __future__ import annotations

import json

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

try:
    from app.database import Base, engine, get_db
    from app.groq_client import GroqAIClient
    from app.repositories import ScreeningRepository
    from app.schemas import AIEvaluation, ScreeningCreate, ScreeningRead
except ImportError:  # pragma: no cover
    from database import Base, engine, get_db
    from groq_client import GroqAIClient
    from repositories import ScreeningRepository
    from schemas import AIEvaluation, ScreeningCreate, ScreeningRead

try:
    Base.metadata.create_all(bind=engine)
except Exception:  # pragma: no cover
    pass


app = FastAPI(title="Screening Service", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "screening-service"}


async def get_candidate(candidate_id: int):
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(f"http://localhost:8001/api/candidates/{candidate_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Candidate not found")
        response.raise_for_status()
        return response.json()


async def get_job(job_id: int):
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(f"http://localhost:8002/api/jobs/{job_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Job not found")
        response.raise_for_status()
        return response.json()


async def get_resume(candidate_id: int):
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(f"http://localhost:8003/api/resumes/candidate/{candidate_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


@app.post("/api/screenings", response_model=ScreeningRead, status_code=status.HTTP_202_ACCEPTED)
async def create_screening(payload: ScreeningCreate, db: Session = Depends(get_db)):
    screening = ScreeningRepository(db).create(payload.candidate_id, payload.job_id)

    try:
        candidate = await get_candidate(payload.candidate_id)
        job = await get_job(payload.job_id)
        resume = await get_resume(payload.candidate_id)

        if resume is None:
            ScreeningRepository(db).update_result(screening.id, "failed", error="Resume not found for candidate")
            return {"screening_id": screening.id, "status": "failed", "error": "Resume not found for candidate"}

        prompt = f"""
        Candidate profile:
        Name: {candidate.get('name')}
        Email: {candidate.get('email')}
        Experience years: {candidate.get('experience_years')}
        Education: {candidate.get('education')}
        Skills: {candidate.get('skills')}

        Job description:
        Title: {job.get('title')}
        Description: {job.get('description')}
        Required skills: {job.get('required_skills')}
        Experience required: {job.get('experience_required')}
        Location: {job.get('location')}

        Resume content:
        {resume.get('content_text')}
        """

        ai_client = GroqAIClient()
        raw_result = ai_client.evaluate_candidate(prompt)
        validated = AIEvaluation.model_validate(raw_result)
        ScreeningRepository(db).update_result(screening.id, "completed", result=validated.model_dump())
        return {"screening_id": screening.id, "status": "completed", "result": validated.model_dump()}
    except Exception as exc:
        ScreeningRepository(db).update_result(screening.id, "failed", error=str(exc))
        return {"screening_id": screening.id, "status": "failed", "error": str(exc)}


@app.get("/api/screenings", response_model=list[ScreeningRead])
async def list_screenings(db: Session = Depends(get_db)):
    return [
        {
            "screening_id": screening.id,
            "candidate_id": screening.candidate_id,
            "job_id": screening.job_id,
            "status": screening.status,
            "result": screening.result,
            "error": screening.error,
            "created_at": screening.created_at,
        }
        for screening in ScreeningRepository(db).list()
    ]


@app.get("/api/screenings/{screening_id}", response_model=ScreeningRead)
async def get_screening(screening_id: int, db: Session = Depends(get_db)):
    screening = ScreeningRepository(db).get(screening_id)
    if screening is None:
        raise HTTPException(status_code=404, detail="Screening not found")
    return {
        "screening_id": screening.id,
        "status": screening.status,
        "result": screening.result,
        "error": screening.error,
        "created_at": screening.created_at,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8004, reload=True)
