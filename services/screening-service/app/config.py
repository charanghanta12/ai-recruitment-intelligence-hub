from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    app_name: str = "screening-service"
    service_port: int = 8004
    database_url: str = "sqlite:///./screening-service.db"
    groq_api_key: str = ""
    model_config = SettingsConfigDict(env_file=ROOT_ENV_FILE, env_prefix="", extra="ignore")


settings = Settings()
