from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    app_name: str = "resume-service"
    service_port: int = 8003
    database_url: str = "sqlite:///./resume-service.db"
    model_config = SettingsConfigDict(env_file=ROOT_ENV_FILE, env_prefix="", extra="ignore")


settings = Settings()
