"""Smart Guardian - Data Preprocessing & Feature Extraction Service"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from app.core.config import settings

logger = logging.getLogger("smart-guardian")


class PreprocessingService:
    """Service for preprocessing sensor data and extracting features"""

    # Physiological value ranges for normalization
    RANGES = {
        "heart_rate": (30.0, 220.0),
        "spo2": (50.0, 100.0),
        "temperature": (34.0, 42.0),
        "accelerometer_x": (-20.0, 20.0),
        "accelerometer_y": (-20.0, 20.0),
        "accelerometer_z": (-20.0, 20.0),
        "gyroscope_x": (-500.0, 500.0),
        "gyroscope_y": (-500.0, 500.0),
        "gyroscope_z": (-500.0, 500.0),
        "emg_signal": (0.0, 1.0),
        "eda_signal": (0.0, 1.0),
    }

    def normalize(self, value: float, key: str) -> float:
        """Min-max normalize a value to [0, 1] range"""
        min_val, max_val = self.RANGES.get(key, (0.0, 1.0))
        if max_val == min_val:
            return 0.0
        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))

    def denormalize(self, value: float, key: str) -> float:
        """Convert a normalized [0,1] value back to original range"""
        min_val, max_val = self.RANGES.get(key, (0.0, 1.0))
        return value * (max_val - min_val) + min_val

    def normalize_vector(self, data: Dict[str, Optional[float]]) -> np.ndarray:
        """Normalize a full sensor data dict into a feature vector"""
        features = []
        for key in self.RANGES:
            value = data.get(key)
            if value is None:
                features.append(0.0)
            else:
                features.append(self.normalize(float(value), key))
        return np.array(features, dtype=np.float32)

    def extract_statistical_features(self, window: np.ndarray) -> np.ndarray:
        """Extract statistical features from a sliding window of data.
        
        For each sensor channel, computes:
        - mean, std, min, max, range, median
        
        Input shape: (window_size, num_channels)
        Output shape: (num_channels * 6,)
        """
        if window.ndim != 2:
            raise ValueError(f"Expected 2D array, got {window.ndim}D")

        features = []
        for col in range(window.shape[1]):
            channel = window[:, col]
            features.extend([
                np.mean(channel),
                np.std(channel),
                np.min(channel),
                np.max(channel),
                np.max(channel) - np.min(channel),
                np.median(channel),
            ])
        return np.array(features, dtype=np.float32)

    def create_sliding_windows(self, data: np.ndarray, window_size: int = 50, stride: int = 10) -> List[np.ndarray]:
        """Create overlapping sliding windows from time-series data.
        
        Input shape: (num_samples, num_channels)
        Output: list of arrays each with shape (window_size, num_channels)
        """
        if data.ndim != 2:
            raise ValueError(f"Expected 2D array, got {data.ndim}D")

        num_samples = data.shape[0]
        if num_samples < window_size:
            logger.warning("Data length %d < window_size %d, padding with zeros", num_samples, window_size)
            pad = np.zeros((window_size - num_samples, data.shape[1]), dtype=np.float32)
            data = np.concatenate([data, pad], axis=0)
            return [data]

        windows = []
        for start in range(0, num_samples - window_size + 1, stride):
            windows.append(data[start:start + window_size])
        return windows

    def detect_artifacts(self, data: Dict[str, Optional[float]]) -> Dict[str, bool]:
        """Detect sensor artifacts and out-of-range values.
        
        Returns dict of field -> is_artifact
        """
        artifacts = {}
        for key, value in data.items():
            if value is None:
                artifacts[key] = True
                continue
            if key in self.RANGES:
                min_val, max_val = self.RANGES[key]
                if float(value) < min_val or float(value) > max_val:
                    artifacts[key] = True
                else:
                    artifacts[key] = False
        return artifacts

    def preprocess_for_model(self, data: Dict[str, Optional[float]]) -> np.ndarray:
        """Full preprocessing pipeline for a single data point.
        
        1. Detect artifacts
        2. Normalize values
        3. Return feature vector ready for model
        """
        artifacts = self.detect_artifacts(data)
        artifact_count = sum(1 for v in artifacts.values() if v)
        if artifact_count > len(artifacts) // 2:
            logger.warning("Too many artifacts (%d/%d), data may be unreliable", artifact_count, len(artifacts))

        return self.normalize_vector(data)

    def preprocess_batch(self, data_list: List[Dict[str, Optional[float]]]) -> np.ndarray:
        """Preprocess a batch of sensor readings.
        
        Returns array of shape (num_samples, num_features)
        """
        feature_vectors = []
        for data in data_list:
            fv = self.preprocess_for_model(data)
            feature_vectors.append(fv)
        return np.array(feature_vectors, dtype=np.float32)


preprocessing_service = PreprocessingService()
