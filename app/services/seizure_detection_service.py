"""Smart Guardian - Seizure Detection Service (Dual-Mode)

Orchestrates seizure detection using sensor heuristic model,
EEG deep learning model, or hybrid combination.
"""

import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.model_service import model_service
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    EEGSegmentRequest,
    BatchPredictionRequest,
    BatchPredictionResponse,
)

logger = logging.getLogger(__name__)


class SeizureDetectionService:
    """Service for seizure detection analysis."""

    def __init__(self, db: Session):
        self.db = db

    def _extract_features_dict(self, data: PredictionRequest) -> dict:
        """Convert PredictionRequest to a features dict for the sensor model."""
        return {
            "heart_rate": data.heart_rate,
            "spo2": data.spo2,
            "temperature": data.temperature,
            "accelerometer_x": data.accelerometer_x,
            "accelerometer_y": data.accelerometer_y,
            "accelerometer_z": data.accelerometer_z,
            "gyroscope_x": data.gyroscope_x,
            "gyroscope_y": data.gyroscope_y,
            "gyroscope_z": data.gyroscope_z,
            "emg_signal": data.emg_signal,
            "eda_signal": data.eda_signal,
        }

    async def analyze(self, data: PredictionRequest) -> PredictionResponse:
        """Analyze sensor data for seizure detection."""
        features_dict = self._extract_features_dict(data)

        # Check if EEG data is also provided for hybrid mode
        if data.eeg_data is not None and len(data.eeg_data) > 0 and model_service.model is not None:
            result = model_service.predict_hybrid(features_dict, data.eeg_data)
            mode = "hybrid"
        elif data.eeg_data is not None and len(data.eeg_data) > 0 and model_service.sensor_model is not None:
            # EEG data provided but EEG model not loaded - fall back to sensor
            result = model_service.sensor_model.predict(features_dict)
            mode = "sensor"
        else:
            # Sensor-only mode
            if model_service.sensor_model is not None:
                result = model_service.sensor_model.predict(features_dict)
            else:
                result = {
                    "seizure_probability": 0.0,
                    "is_seizure": False,
                    "confidence": 0.0,
                    "model_version": "unavailable",
                    "risk_factors": [],
                }
            mode = "sensor"

        # Save prediction to DB if possible
        try:
            from app.models.prediction import Prediction
            pred = Prediction(
                user_id=data.user_id,
                device_id=data.device_id,
                seizure_probability=result.get("seizure_probability", 0.0),
                is_seizure=result.get("is_seizure", False),
                confidence=result.get("confidence", 0.0),
                prediction_mode=mode,
                model_version=result.get("model_version", "unknown"),
            )
            self.db.add(pred)
            self.db.commit()
        except Exception as e:
            logger.warning(f"Could not save prediction to DB: {e}")

        # Create alert if seizure detected
        if result.get("is_seizure", False):
            try:
                from app.services.alert_service import create_alert
                risk_str = ", ".join(result.get("risk_factors", []))
                await create_alert(
                    self.db,
                    user_id=data.user_id,
                    device_id=data.device_id,
                    alert_type="seizure",
                    severity="critical" if result["seizure_probability"] >= 0.7 else "warning",
                    confidence=result["seizure_probability"],
                    heart_rate=data.heart_rate,
                    spo2=data.spo2,
                    message=f"Seizure detected (prob={result['seizure_probability']:.2f}, mode={mode}). {risk_str}",
                )
            except Exception as e:
                logger.warning(f"Could not create seizure alert: {e}")

        return PredictionResponse(
            seizure_probability=result.get("seizure_probability", 0.0),
            is_seizure=result.get("is_seizure", False),
            confidence=result.get("confidence", 0.0),
            prediction_mode=mode,
            model_version=result.get("model_version", "unknown"),
            risk_factors=result.get("risk_factors"),
        )

    async def analyze_eeg(self, data: EEGSegmentRequest) -> PredictionResponse:
        """Analyze a dedicated EEG segment for seizure detection."""
        result = model_service.predict_eeg(data.eeg_data)
        mode = "eeg"

        # Save prediction to DB
        try:
            from app.models.prediction import Prediction
            pred = Prediction(
                user_id=data.user_id,
                device_id=data.device_id,
                seizure_probability=result.get("seizure_probability", 0.0),
                is_seizure=result.get("is_seizure", False),
                confidence=result.get("confidence", 0.0),
                prediction_mode=mode,
                model_version=result.get("model_version", "unknown"),
            )
            self.db.add(pred)
            self.db.commit()
        except Exception as e:
            logger.warning(f"Could not save EEG prediction to DB: {e}")

        # Create alert if seizure detected
        if result.get("is_seizure", False):
            try:
                from app.services.alert_service import create_alert
                await create_alert(
                    self.db,
                    user_id=data.user_id,
                    device_id=data.device_id,
                    alert_type="seizure",
                    severity="critical" if result["seizure_probability"] >= 0.7 else "warning",
                    confidence=result["seizure_probability"],
                    message=f"EEG seizure detected (prob={result['seizure_probability']:.2f}, channel={data.channel})",
                )
            except Exception as e:
                logger.warning(f"Could not create EEG seizure alert: {e}")

        return PredictionResponse(
            seizure_probability=result.get("seizure_probability", 0.0),
            is_seizure=result.get("is_seizure", False),
            confidence=result.get("confidence", 0.0),
            prediction_mode=mode,
            model_version=result.get("model_version", "unknown"),
            risk_factors=result.get("risk_factors"),
        )

    async def batch_analyze(self, data: BatchPredictionRequest) -> BatchPredictionResponse:
        """Batch analyze multiple sensor data points."""
        results = []
        for point in data.data_points:
            result = await self.analyze(point)
            results.append(result)
        return BatchPredictionResponse(results=results)