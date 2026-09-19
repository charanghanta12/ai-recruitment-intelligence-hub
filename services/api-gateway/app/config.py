from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    app_name: str = "api-gateway"
    service_port: int = 8000
    candidate_service_url: str = "http://localhost:8001"
    job_service_url: str = "http://localhost:8002"
    resume_service_url: str = "http://localhost:8003"
    screening_service_url: str = "http://localhost:8004"
    interview_service_url: str = "http://localhost:8005"
    assistant_service_url: str = "http://localhost:8006"
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=ROOT_ENV_FILE, env_prefix="", extra="ignore")


settings = Settings()
