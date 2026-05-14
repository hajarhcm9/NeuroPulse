"""Smart Guardian - Model Service with Real TensorFlow Model"""

import os
import json
import logging
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelService:
    """Singleton service for seizure detection model inference."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.model = None
        self.model_version = "0.0.0"
        self.norm_mean = 0.0
        self.norm_std = 1.0
        self._load_model()

    def _load_model(self):
        """Load the trained Keras model and normalization params."""
        try:
            import tensorflow as tf

            model_paths = [
                Path("models/seizure_detector.h5"),
                Path("ml/models/seizhure_detector.h5"),
                Path("ml/training/models/seizure_detector.h5"),
                Path(__file__).parent.parent.parent / "models" / "seizure_detector.h5",
                Path(__file__).parent.parent.parent / "ml" / "training" / "models" / "seizure_detector.h5",
            ]

            model_path = None
            for path in model_paths:
                if path.exists():
                    model_path = path
                    break

            if model_path is None:
                logger.warning("No trained model found. Using dummy model.")
                self.model = None
                return

            self.model = tf.keras.models.load_model(str(model_path))
            logger.info(f"Model loaded from {model_path}")

            metadata_paths = [
                Path("models/model_metadata.json"),
                Path("ml/models/model_metadata.json"),
                Path("ml/training/models/model_metadata.json"),
                Path(__file__).parent.parent.parent / "models" / "model_metadata.json",
                Path(__file__).parent.parent.parent / "ml" / "training" / "models" / "model_metadata.json",
            ]

            for meta_path in metadata_paths:
                if meta_path.exists():
                    with open(meta_path, "r") as f:
                        metadata = json.load(f)
                    self.model_version = metadata.get("model_version", "1.0.0")
                    norm = metadata.get("normalization", {})
                    self.norm_mean = norm.get("mean", 0.0)
                    self.norm_std = norm.get("std", 1.0)
                    logger.info(
                        f"Model v{self.model_version} | "
                        f"norm_mean={self.norm_mean:.4f}, norm_std={self.norm_std:.4f}"
                    )
                    break

        except ImportError:
            logger.warning("TensorFlow not installed. Using dummy model.")
            self.model = None
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None

    @property
    def is_loaded(self):
        return self.model is not None

    def load_model(self):
        self._load_model()

    def predict(self, features: np.ndarray) -> dict:
        """
        Run seizhure detection on input features.

        Args:
            features: numpy array of shape (178,) or (1, 178) or (1, 178, 1)

        Returns:
            dict with seizure_probability, is_seizure, confidence, model_version
        """
        if self.model is None:
            return {
                "seizure_probability": 0.0,
                "is_seizhure": False,
                "confidence": 0.0,
                "model_version": "dummy",
            }

        x = np.array(features, dtype=np.float32)
        if x.ndim == 1:
            x = x.reshape(1, 178, 1)
        elif x.ndim == 2 and x.shape[0] == 1:
            x = x.reshape(1, x.shape[1], 1)
        elif x.ndim == 2:
            x = x.reshape(x.shape[0], 178, 1)

        x = (x - self.norm_mean) / self.norm_std

        prediction = self.model.predict(x, verbose=0)
        prob = float(prediction[0][0])

        threshold = 0.5
        is_seizure = prob >= threshold
        confidence = prob if is_seizure else (1.0 - prob)

        return {
            "seizure_probability": round(prob, 4),
            "is_seizure": is_seizure,
            "confidence": round(confidence, 4),
            "model_version": self.model_version,
        }


model_service = ModelService()
