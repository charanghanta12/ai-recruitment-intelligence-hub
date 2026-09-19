import os
import sys
from pathlib import Path

from groq import Groq

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from config import settings
else:
    from app.config import settings


class GroqAIClient:
    def __init__(self, api_key: str | None = None):
        self.client = Groq(api_key=api_key or settings.groq_api_key or os.getenv("GROQ_API_KEY", ""))

    def evaluate_candidate(self, prompt: str) -> dict:
        if not self.client.api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        response = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": "You are an AI hiring analyst. Use only information present in the candidate resume and job description. Do not invent experience or skills. Clearly identify missing information, provide evidence-based observations, and generate useful interview questions. Do not make a final hiring decision or recommend accept/reject. Return valid JSON with exactly these keys: summary (string), matching_skills (array of strings), missing_skills (array of strings), experience_analysis (string), strengths (array of strings), areas_to_explore (array of strings), interview_questions (array of strings). Always include summary and experience_analysis, even when information is missing."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Groq returned empty response")
        return __import__("json").loads(content)
