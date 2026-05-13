"""Smart Guardian - Emergency Contact model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from app.models.base import BaseModel


class EmergencyContact(BaseModel):
    """Emergency contact for a patient"""
    __tablename__ = "emergency_contacts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    relationship = Column(String(50), nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)
    notify_on_alert = Column(Boolean, default=True, nullable=False)
