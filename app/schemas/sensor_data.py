"""Smart Guardian - Sensor data schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SensorDataCreate(BaseModel):
    """Schema for incoming sensor data (from bracelet)"""
    device_id: str
    user_id: int
    sensor_type: str = "wearable"
    heart_rate: Optional[float] = Field(None, ge=20, le=300, description="Heart rate BPM")
    spo2: Optional[float] = Field(None, ge=0, le=100, description="SpO2 percentage")
    temperature: Optional[float] = Field(None, ge=25, le=45, description="Temperature Celsius")
    accelerometer_x: Optional[float] = None
    accelerometer_y: Optional[float] = None
    accelerometer_z: Optional[float] = None
    gyroscope_x: Optional[float] = None
    gyroscope_y: Optional[float] = None
    gyroscope_z: Optional[float] = None
    emg_signal: Optional[float] = Field(None, ge=0, le=1, description="EMG signal 0-1")
    eda_signal: Optional[float] = Field(None, ge=0, le=1, description="EDA signal 0-1")
    raw_data: Optional[str] = None


class SensorDataResponse(BaseModel):
    """Schema for sensor data response"""
    id: int
    user_id: int
    device_id: str
    sensor_type: str
    heart_rate: Optional[float] = Field(None, ge=20, le=300, description="Heart rate BPM")
    spo2: Optional[float] = Field(None, ge=0, le=100, description="SpO2 percentage")
    temperature: Optional[float] = Field(None, ge=25, le=45, description="Temperature Celsius")
    accelerometer_x: Optional[float] = None
    accelerometer_y: Optional[float] = None
    accelerometer_z: Optional[float] = None
    gyroscope_x: Optional[float] = None
    gyroscope_y: Optional[float] = None
    gyroscope_z: Optional[float] = None
    emg_signal: Optional[float] = Field(None, ge=0, le=1, description="EMG signal 0-1")
    eda_signal: Optional[float] = Field(None, ge=0, le=1, description="EDA signal 0-1")
    created_at: datetime

    model_config = {"from_attributes": True}
