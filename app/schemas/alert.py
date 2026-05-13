"""Smart Guardian - Alert schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    """Schema for creating an alert"""
    user_id: int
    device_id: str
    alert_type: str
    severity: str = Field(default="warning", pattern="^(info|warning|critical)$")
    confidence: Optional[float] = None
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    message: Optional[str] = None


class AlertResponse(BaseModel):
    """Schema for alert response"""
    id: int
    user_id: int
    device_id: str
    alert_type: str
    severity: str
    confidence: Optional[float] = None
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    message: Optional[str] = None
    is_read: bool
    is_resolved: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertUpdate(BaseModel):
    """Schema for updating an alert"""
    is_read: Optional[bool] = None
    is_resolved: Optional[bool] = None
