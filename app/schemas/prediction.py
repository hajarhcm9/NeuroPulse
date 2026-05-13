"""Smart Guardian - Prediction schemas"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Schema for prediction request with sensor data"""
    user_id: int
    device_id: str
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


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    user_id: int
    device_id: str
    seizure_probability: float
    is_seizure: bool
    confidence: float
    model_version: str
    timestamp: datetime = Field(default_factory=datetime.now)
    error: Optional[str] = None


class ModelInfoResponse(BaseModel):
    """Schema for model info response"""
    model_type: str
    version: str
    threshold: float
    status: str
    input_shape: Optional[str] = None
    output_shape: Optional[str] = None


class BatchPredictionRequest(BaseModel):
    """Schema for batch prediction with multiple data points"""
    user_id: int
    device_id: str
    data_points: List[PredictionRequest] = Field(..., min_length=1, max_length=100)


class BatchPredictionResponse(BaseModel):
    """Schema for batch prediction response"""
    user_id: int
    device_id: str
    predictions: List[PredictionResponse]
    avg_seizure_probability: float
    max_seizure_probability: float
