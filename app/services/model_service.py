"""Smart Guardian - AI Model Service"""

import os
import logging
import numpy as np
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger("smart-guardian")


class ModelService:
    """TensorFlow model loading and inference service"""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def load_model(self) -> None:
        """Load the TensorFlow seizure detection model"""
        if self._model is not None:
            logger.info("Model already loaded, skipping")
            return

        model_path = settings.AI_MODEL_PATH
        if not os.path.exists(model_path):
            logger.warning("Model file not found at %s, using dummy model", model_path)
            self._model = self._create_dummy_model()
            return

        try:
            import tensorflow as tf
            self._model = tf.keras.models.load_model(model_path)
            logger.info("Model loaded from %s", model_path)
        except ImportError:
            logger.warning("TensorFlow not installed, using dummy model")
            self._model = self._create_dummy_model()
        except Exception as e:
            logger.error("Failed to load model: %s", str(e))
            self._model = self._create_dummy_model()

    def _create_dummy_model(self):
        """Create a dummy model for development/testing"""
        return {"type": "dummy", "version": "0.1.0", "threshold": settings.AI_SEIZURE_THRESHOLD}

    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Run inference on the model"""
        if self._model is None:
            self.load_model()

        if isinstance(self._model, dict):
            return self._dummy_predict(features)

        try:
            prediction = self._model.predict(features, verbose=0)
            seizure_prob = float(prediction[0][0])
            return {
                "seizure_probability": seizure_prob,
                "is_seizure": seizure_prob >= settings.AI_SEIZURE_THRESHOLD,
                "confidence": abs(seizure_prob - 0.5) * 2,
                "model_version": settings.AI_MODEL_VERSION,
            }
        except Exception as e:
            logger.error("Prediction failed: %s", str(e))
            return {
                "seizure_probability": 0.0,
                "is_seizure": False,
                "confidence": 0.0,
                "model_version": settings.AI_MODEL_VERSION,
                "error": str(e),
            }

    def _dummy_predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Dummy prediction for development"""
        return {
            "seizure_probability": 0.15,
            "is_seizure": False,
            "confidence": 0.7,
            "model_version": "dummy-0.1.0",
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Return model metadata"""
        if self._model is None:
            self.load_model()

        if isinstance(self._model, dict):
            return {
                "model_type": "dummy",
                "version": "0.1.0",
                "threshold": settings.AI_SEIZURE_THRESHOLD,
                "status": "development",
            }

        return {
            "model_type": "tensorflow",
            "version": settings.AI_MODEL_VERSION,
            "threshold": settings.AI_SEIZURE_THRESHOLD,
            "input_shape": str(self._model.input_shape),
            "output_shape": str(self._model.output_shape),
            "status": "production",
        }


model_service = ModelService()
