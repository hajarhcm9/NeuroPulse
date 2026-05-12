"""Smart Guardian - Base model with common fields"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from app.core.database import Base


class BaseModel(Base):
    """Abstract base model with id and timestamps"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
