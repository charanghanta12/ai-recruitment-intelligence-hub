from __future__ import annotations

from typing import Optional

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from pypdf import PdfReader
from sqlalchemy.orm import Session

try:
    from app.database import Base, engine, get_db
    from app.repositories import ResumeRepository
    from app.schemas import ResumeRead
except ImportError:  # pragma: no cover
    from database import Base, engine, get_db
    from repositories import ResumeRepository
    from schemas import ResumeRead

try:
    Base.metadata.create_all(bind=engine)
except Exception:  # pragma: no cover
    pass


app = FastAPI(title="Resume Service", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "resume-service"}


@app.post("/api/resumes/upload", response_model=ResumeRead, status_code=status.HTTP_201_CREATED)
async def upload_resume(candidate_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        reader = PdfReader(__import__('io').BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        content_text = "\n".join(pages).strip()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid PDF: {str(exc)}") from exc

    if not content_text:
        raise HTTPException(status_code=400, detail="Could not extract text from the PDF")

    resume = ResumeRepository(db).create(candidate_id, file.filename, file_bytes, content_text)
    return resume


@app.get("/api/resumes/candidate/{candidate_id}", response_model=Optional[ResumeRead])
async def get_resume_for_candidate(candidate_id: int, db: Session = Depends(get_db)):
    resume = ResumeRepository(db).get_by_candidate(candidate_id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True)
