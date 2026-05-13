"""Smart Guardian - Notification schemas"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    """Schema for creating a notification"""
    user_id: int
    alert_id: Optional[int] = None
    channel: str = Field(default="in_app", pattern="^(in_app|email|sms|push)$")
    title: str
    body: Optional[str] = None


class NotificationResponse(BaseModel):
    """Schema for notification response"""
    id: int
    user_id: int
    alert_id: Optional[int] = None
    channel: str
    title: str
    body: Optional[str] = None
    is_read: bool
    is_sent: bool
    sent_at: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationUpdate(BaseModel):
    """Schema for updating a notification"""
    is_read: Optional[bool] = None


class NotificationPreferences(BaseModel):
    """Schema for user notification preferences"""
    email_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = True
    in_app_enabled: bool = True
    critical_only: bool = False
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
