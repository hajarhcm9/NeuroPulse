"""Smart Guardian - Seizure Detection Service"""

import logging
import numpy as np
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.services.model_service import model_service
from app.services.alert_service import AlertService
from app.services.sensor_service import SensorService
from app.schemas.prediction import PredictionRequest, PredictionResponse, BatchPredictionRequest, BatchPredictionResponse
from app.schemas.alert import AlertCreate
from app.schemas.sensor_data import SensorDataCreate
from app.core.config import settings

logger = logging.getLogger("smart-guardian")


class SeizureDetectionService:
    """Service that orchestrates seizure detection from sensor data to alerts"""

    def __init__(self, db):
        self.db = db
        self.alert_service = AlertService(db)
        self.sensor_service = SensorService(db)

    def _extract_features(self, data: PredictionRequest) -> np.ndarray:
        """Extract feature vector from sensor data for model input"""
        features = [
            data.heart_rate or 0.0,
            data.spo2 or 0.0,
            data.temperature or 0.0,
            data.accelerometer_x or 0.0,
            data.accelerometer_y or 0.0,
            data.accelerometer_z or 0.0,
            data.gyroscope_x or 0.0,
            data.gyroscope_y or 0.0,
            data.gyroscope_z or 0.0,
            data.emg_signal or 0.0,
            data.eda_signal or 0.0,
        ]
        return np.array([features], dtype=np.float32)

    def _determine_severity(self, seizure_probability: float) -> str:
        """Determine alert severity based on seizure probability"""
        if seizure_probability >= 0.9:
            return "critical"
        elif seizure_probability >= 0.7:
            return "warning"
        return "info"

    def _build_alert_message(self, data: PredictionRequest, result: Dict[str, Any]) -> str:
        """Build a human-readable alert message"""
        severity = self._determine_severity(result["seizure_probability"])
        msg = f"Seizure detection alert ({severity}): "
        msg += f"probability={result["seizure_probability"]:.2f}, "
        msg += f"confidence={result["confidence"]:.2f}. "
        if data.heart_rate:
            msg += f"HR={data.heart_rate:.1f} bpm, "
        if data.spo2:
            msg += f"SpO2={data.spo2:.1f}%, "
        return msg.rstrip(", ")

    async def analyze(self, data: PredictionRequest) -> PredictionResponse:
        """Analyze sensor data for seizure detection"""
        features = self._extract_features(data)
        result = model_service.predict(features)

        response = PredictionResponse(
            user_id=data.user_id,
            device_id=data.device_id,
            seizure_probability=result["seizure_probability"],
            is_seizure=result["is_seizure"],
            confidence=result["confidence"],
            model_version=result["model_version"],
            error=result.get("error"),
        )

        if result["is_seizure"]:
            severity = self._determine_severity(result["seizure_probability"])
            alert_data = AlertCreate(
                user_id=data.user_id,
                device_id=data.device_id,
                alert_type="seizure_detection",
                severity=severity,
                confidence=result["confidence"],
                heart_rate=data.heart_rate,
                spo2=data.spo2,
                message=self._build_alert_message(data, result),
            )
            try:
                self.alert_service.create_alert(alert_data)
                logger.warning("Seizure alert created for user %s (prob=%.2f)", data.user_id, result["seizure_probability"])
            except Exception as e:
                logger.error("Failed to create seizure alert: %s", str(e))

        try:
            sensor_data = SensorDataCreate(
                user_id=data.user_id,
                device_id=data.device_id,
                sensor_type="multi",
                heart_rate=data.heart_rate,
                spo2=data.spo2,
                temperature=data.temperature,
                accelerometer_x=data.accelerometer_x,
                accelerometer_y=data.accelerometer_y,
                accelerometer_z=data.accelerometer_z,
                gyroscope_x=data.gyroscope_x,
                gyroscope_y=data.gyroscope_y,
                gyroscope_z=data.gyroscope_z,
                emg_signal=data.emg_signal,
                eda_signal=data.eda_signal,
            )
            self.sensor_service.store_sensor_data(sensor_data)
        except Exception as e:
            logger.error("Failed to store sensor data: %s", str(e))

        return response

    async def batch_analyze(self, data: BatchPredictionRequest) -> BatchPredictionResponse:
        """Analyze multiple sensor data points for seizure detection"""
        predictions = []
        for point in data.data_points:
            point.user_id = data.user_id
            point.device_id = data.device_id
            pred = await self.analyze(point)
            predictions.append(pred)

        probs = [p.seizure_probability for p in predictions]
        return BatchPredictionResponse(
            user_id=data.user_id,
            device_id=data.device_id,
            predictions=predictions,
            avg_seizure_probability=sum(probs) / len(probs) if probs else 0.0,
            max_seizure_probability=max(probs) if probs else 0.0,
        )
