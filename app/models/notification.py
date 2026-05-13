"""Smart Guardian - Notification model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from app.models.base import BaseModel


class Notification(BaseModel):
    """Notification model for push/email alerts"""
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)
    channel = Column(String(20), nullable=False, default="in_app")
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    is_sent = Column(Boolean, default=False, nullable=False)
    sent_at = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
