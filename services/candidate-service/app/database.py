import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from config import settings
else:
    from app.config import settings

engine_options = {"connect_args": {"check_same_thread": False}} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, future=True, pool_pre_ping=True, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
