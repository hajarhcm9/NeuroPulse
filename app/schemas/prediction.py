"""Prediction schemas."""
from typing import List, Optional
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    heart_rate: float = Field(75.0, description="Heart rate BPM")
    spo2: float = Field(98.0, description="SpO2 percentage")
    accelerometer: float = Field(0.5, description="Accel magnitude g")

    emg_signal: float = Field(0.3, description="EMG strength 0-1")
    eda_signal: float = Field(0.3, description="EDA level 0-1")
    temperature: float = Field(36.5, description="Temp Celsius")
    eeg_data: Optional[List[float]] = Field(None, description="Optional EEG")

class EEGSegmentRequest(BaseModel):
    eeg_data: List[float] = Field(..., min_length=178, description="Raw EEG samples")
    sampling_rate: int = Field(173, description="EEG Hz")
    channel: str = Field("Fp1", description="EEG channel")

class PredictionResponse(BaseModel):
    seizure_probability: float
    is_seizure: bool
    confidence: float

    prediction_mode: str = Field("sensor", description="Mode used")
    risk_factors: List[str] = Field(default_factory=list)
    model_version: str = "unknown"
    timestamp: Optional[str] = None

class ModelInfoResponse(BaseModel):
    sensor_model_available: bool = True
    eeg_model_available: bool = False
    sensor_model_version: str = "sensor-heuristic-v1.0"

    eeg_model_version: Optional[str] = None
    prediction_modes: List[str] = ["sensor", "eeg", "hybrid"]

class BatchPredictionRequest(BaseModel):
    predictions: List[PredictionRequest] = Field(..., description="List of predictions")

class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse] = Field(default_factory=list)
    total_count: int = 0
    seizure_count: int = 0
