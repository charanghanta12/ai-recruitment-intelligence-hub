from __future__ import annotations

import sys
from pathlib import Path

import httpx
from fastapi import FastAPI
from groq import Groq

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from config import settings
else:
    from app.config import settings

app = FastAPI(title="AI Assistant Service", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "assistant-service"}


@app.post("/api/assistant/chat")
async def chat(payload: dict):
    question = payload.get("question") or payload.get("message")
    if not question:
        return {"answer": "Please provide a question to analyze."}

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            candidates = (await client.get("http://localhost:8001/api/candidates")).json()
            jobs = (await client.get("http://localhost:8002/api/jobs")).json()
            applications = (await client.get("http://localhost:8002/api/applications")).json()
    except Exception as exc:
        raise RuntimeError(f"Failed to retrieve recruitment data: {exc}") from exc

    client = Groq(api_key=settings.groq_api_key)
    context = {
        "question": question,
        "candidates": candidates,
        "jobs": jobs,
        "applications": applications,
    }
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": "You are a recruitment assistant. Use the provided application data to answer the recruiter question. Do not invent data. Summarize what is relevant and clearly mention any missing information."},
            {"role": "user", "content": str(context)},
        ],
        temperature=0.2,
    )
    answer = response.choices[0].message.content
    return {"answer": answer or "No answer generated."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8006, reload=True)
