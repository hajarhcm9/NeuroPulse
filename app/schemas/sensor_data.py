"""Smart Guardian - Sensor data schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SensorDataCreate(BaseModel):
    """Schema for incoming sensor data (from bracelet)"""
    device_id: str
    user_id: int
    sensor_type: str = "wearable"
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    temperature: Optional[float] = None
    accelerometer_x: Optional[float] = None
    accelerometer_y: Optional[float] = None
    accelerometer_z: Optional[float] = None
    gyroscope_x: Optional[float] = None
    gyroscope_y: Optional[float] = None
    gyroscope_z: Optional[float] = None
    emg_signal: Optional[float] = None
    eda_signal: Optional[float] = None
    raw_data: Optional[str] = None


class SensorDataResponse(BaseModel):
    """Schema for sensor data response"""
    id: int
    user_id: int
    device_id: str
    sensor_type: str
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    temperature: Optional[float] = None
    accelerometer_x: Optional[float] = None
    accelerometer_y: Optional[float] = None
    accelerometer_z: Optional[float] = None
    gyroscope_x: Optional[float] = None
    gyroscope_y: Optional[float] = None
    gyroscope_z: Optional[float] = None
    emg_signal: Optional[float] = None
    eda_signal: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}
