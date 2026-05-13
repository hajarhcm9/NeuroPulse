"""Smart Guardian - Emergency Contact schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class EmergencyContactCreate(BaseModel):
    """Schema for creating an emergency contact"""
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=5, max_length=20)
    email: Optional[EmailStr] = None
    relationship: Optional[str] = Field(None, max_length=50)
    is_primary: bool = False
    notify_on_alert: bool = True


class EmergencyContactUpdate(BaseModel):
    """Schema for updating an emergency contact"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, min_length=5, max_length=20)
    email: Optional[EmailStr] = None
    relationship: Optional[str] = Field(None, max_length=50)
    is_primary: Optional[bool] = None
    notify_on_alert: Optional[bool] = None


class EmergencyContactResponse(BaseModel):
    """Schema for emergency contact response"""
    id: int
    user_id: int
    full_name: str
    phone: str
    email: Optional[str] = None
    relationship: Optional[str] = None
    is_primary: bool
    notify_on_alert: bool
    created_at: datetime

    model_config = {"from_attributes": True}
