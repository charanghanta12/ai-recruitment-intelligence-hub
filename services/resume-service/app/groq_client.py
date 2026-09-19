import json

from groq import Groq
from pydantic import BaseModel, Field

try:
    from app.config import settings
except ImportError:  # pragma: no cover
    from config import settings


class ResumeExtraction(BaseModel):
    name: str = Field(min_length=1)
    email: str
    phone: str | None = None
    experience_years: int = Field(default=0, ge=0)
    education: str | None = None
    skills: list[str] = Field(default_factory=list)


class GroqResumeParser:
    def __init__(self) -> None:
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is not configured")
        self.client = Groq(api_key=settings.groq_api_key)

    def parse(self, resume_text: str) -> ResumeExtraction:
        response = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": "Extract factual candidate information from the resume. Return valid JSON with exactly these keys: name, email, phone, experience_years, education, skills. Do not infer missing facts. Use an empty string, null, 0, or [] when a field is absent.",
                },
                {"role": "user", "content": resume_text},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Groq returned an empty resume extraction")
        return ResumeExtraction.model_validate(json.loads(content))
