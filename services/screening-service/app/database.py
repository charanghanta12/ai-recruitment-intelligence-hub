from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    from app.config import settings
except ImportError:  # pragma: no cover
    from config import settings

if not settings.database_url.startswith("postgresql"):
    raise ValueError("DATABASE_URL must use PostgreSQL; temporary SQLite databases are disabled")

engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
