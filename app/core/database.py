"""Smart Guardian - Database configuration"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

_is_sqlite = "sqlite" in str(settings.database_url)
_engine_kwargs = {
    "echo": settings.debug,
}
if not _is_sqlite:
    _engine_kwargs["pool_size"] = settings.database_pool_size
    _engine_kwargs["max_overflow"] = settings.database_max_overflow

engine = create_engine(settings.database_url, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
