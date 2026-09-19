from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import httpx

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from config import settings
else:
    from app.config import settings

app = FastAPI(title="RecruitFlow API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICE_URLS = {
    "candidate": settings.candidate_service_url,
    "job": settings.job_service_url,
    "resume": settings.resume_service_url,
    "screening": settings.screening_service_url,
    "interview": settings.interview_service_url,
    "assistant": settings.assistant_service_url,
}


async def proxy_request(service_name: str, path: str, method: str = "GET", **kwargs):
    base_url = SERVICE_URLS.get(service_name)
    if not base_url:
        raise ValueError(f"Unknown service: {service_name}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(method, f"{base_url}{path}", **kwargs)
        try:
            payload = response.json()
        except ValueError:
            payload = {"detail": response.text}

        if response.is_error:
            raise httpx.HTTPStatusError(
                message=f"{service_name} service returned {response.status_code}",
                request=response.request,
                response=response,
            )
        return payload


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "api-gateway"}


@app.get("/api/candidates")
async def list_candidates():
    return await proxy_request("candidate", "/api/candidates")


@app.post("/api/candidates")
async def create_candidate(payload: dict):
    return await proxy_request("candidate", "/api/candidates", method="POST", json=payload)


@app.get("/api/candidates/{candidate_id}")
async def get_candidate(candidate_id: int):
    return await proxy_request("candidate", f"/api/candidates/{candidate_id}")


@app.put("/api/candidates/{candidate_id}")
async def update_candidate(candidate_id: int, payload: dict):
    return await proxy_request("candidate", f"/api/candidates/{candidate_id}", method="PUT", json=payload)


@app.delete("/api/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int):
    return await proxy_request("candidate", f"/api/candidates/{candidate_id}", method="DELETE")


@app.get("/api/jobs")
async def list_jobs():
    return await proxy_request("job", "/api/jobs")


@app.post("/api/jobs")
async def create_job(payload: dict):
    return await proxy_request("job", "/api/jobs", method="POST", json=payload)


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: int):
    return await proxy_request("job", f"/api/jobs/{job_id}")


@app.put("/api/jobs/{job_id}")
async def update_job(job_id: int, payload: dict):
    return await proxy_request("job", f"/api/jobs/{job_id}", method="PUT", json=payload)


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: int):
    return await proxy_request("job", f"/api/jobs/{job_id}", method="DELETE")


@app.post("/api/applications")
async def create_application(payload: dict):
    return await proxy_request("job", "/api/applications", method="POST", json=payload)


@app.get("/api/applications")
async def list_applications():
    return await proxy_request("job", "/api/applications")


@app.get("/api/jobs/{job_id}/applications")
async def get_job_applications(job_id: int):
    return await proxy_request("job", f"/api/jobs/{job_id}/applications")


@app.post("/api/resumes/upload")
async def upload_resume(candidate_id: int, file: UploadFile = File(...)):
    file_bytes = await file.read()
    return await proxy_request(
        "resume",
        f"/api/resumes/upload?candidate_id={candidate_id}",
        method="POST",
        files={"file": (file.filename, file_bytes, file.content_type or "application/pdf")},
    )


@app.get("/api/resumes/candidate/{candidate_id}")
async def get_resume(candidate_id: int):
    return await proxy_request("resume", f"/api/resumes/candidate/{candidate_id}")


@app.post("/api/screenings")
async def create_screening(payload: dict):
    return await proxy_request("screening", "/api/screenings", method="POST", json=payload)


@app.get("/api/screenings")
async def list_screenings():
    return await proxy_request("screening", "/api/screenings")


@app.get("/api/screenings/{screening_id}")
async def get_screening(screening_id: int):
    return await proxy_request("screening", f"/api/screenings/{screening_id}")


@app.get("/api/interviews")
async def list_interviews():
    return await proxy_request("interview", "/api/interviews")


@app.post("/api/interviews")
async def create_interview(payload: dict):
    return await proxy_request("interview", "/api/interviews", method="POST", json=payload)


@app.get("/api/interviews/{interview_id}")
async def get_interview(interview_id: int):
    return await proxy_request("interview", f"/api/interviews/{interview_id}")


@app.put("/api/interviews/{interview_id}")
async def update_interview(interview_id: int, payload: dict):
    return await proxy_request("interview", f"/api/interviews/{interview_id}", method="PUT", json=payload)


@app.post("/api/assistant/chat")
async def assistant_chat(payload: dict):
    return await proxy_request("assistant", "/api/assistant/chat", method="POST", json=payload)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.service_port, reload=True)
