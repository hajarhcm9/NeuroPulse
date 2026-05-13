"""Smart Guardian - Alert model"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text, Boolean
from app.models.base import BaseModel


class Alert(BaseModel):
    """Seizure alert model"""
    __tablename__ = "alerts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    device_id = Column(String(100), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False, default="warning")
    confidence = Column(Float, nullable=True)
    heart_rate = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    message = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    is_resolved = Column(Boolean, default=False, nullable=False)
