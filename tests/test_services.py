"""Smart Guardian - Service-level integration tests"""

import pytest
import numpy as np
from app.services.preprocessing_service import preprocessing_service
from app.services.model_service import model_service
from app.core.security import hash_password, verify_password, create_access_token, decode_token


class TestPreprocessingIntegration:
    """Integration tests for preprocessing -> model pipeline"""

    def test_full_preprocessing_pipeline(self):
        raw_data = {
            "heart_rate": 120.0,
            "spo2": 90.0,
            "temperature": 37.5,
            "accelerometer_x": 2.5,
            "accelerometer_y": -1.8,
            "accelerometer_z": 8.2,
            "gyroscope_x": 50.0,
            "gyroscope_y": -30.0,
            "gyroscope_z": 45.0,
            "emg_signal": 0.75,
            "eda_signal": 0.65,
        }
        features = preprocessing_service.preprocess_for_model(raw_data)
        assert isinstance(features, np.ndarray)
        assert features.shape == (len(preprocessing_service.RANGES),)
        assert all(0.0 <= v <= 1.0 for v in features)

    def test_preprocessed_data_feeds_model(self):
        raw_data = {"heart_rate": 120.0, "spo2": 90.0}
        features = preprocessing_service.preprocess_for_model(raw_data)
        model_input = features.reshape(1, -1)
        service = model_service.__class__()
        service._model = service._create_dummy_model()
        result = service.predict(model_input)
        assert "seizure_probability" in result
        assert isinstance(result['seizure_probability'], float)

    def test_batch_preprocessing_pipeline(self):
        data_list = [
            {"heart_rate": 75.0, "spo2": 98.0, "temperature": 36.6},
            {"heart_rate": 120.0, "spo2": 90.0, "temperature": 37.5},
            {"heart_rate": 150.0, "spo2": 85.0, "temperature": 38.0},
        ]
        batch = preprocessing_service.preprocess_batch(data_list)
        assert batch.shape == (3, len(preprocessing_service.RANGES))
        service = model_service.__class__()
        service._model = service._create_dummy_model()
        result = service.predict(batch)
        assert "seizure_probability" in result


class TestSecurityIntegration:
    """Integration tests for security workflow"""

    def test_full_auth_workflow(self):
        password = "MySecurePass123!"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
        token = create_access_token({"sub": "42", "role": "patient"})
        payload = decode_token(token)
        assert payload['sub'] == "42"
        assert payload['role'] == "patient"

    def test_token_with_different_roles(self):
        for role in ["patient", "doctor", "admin"]:
            token = create_access_token({"sub": "1", "role": role})
            payload = decode_token(token)
            assert payload['role'] == role


class TestSlidingWindowIntegration:
    """Integration tests for sliding window + feature extraction"""

    def test_window_to_features_pipeline(self):
        data = np.random.randn(200, 11).astype(np.float32)
        windows = preprocessing_service.create_sliding_windows(data, window_size=50, stride=25)
        assert len(windows) > 0
        for window in windows:
            features = preprocessing_service.extract_statistical_features(window)
            assert features.shape == (11 * 6,)
            assert not np.any(np.isnan(features))

    def test_normalized_data_windowing(self):
        data_list = [{"heart_rate": 75.0 + i * 0.5, "spo2": 98.0 - i * 0.1} for i in range(50)]
        batch = preprocessing_service.preprocess_batch(data_list)
        assert batch.shape == (50, len(preprocessing_service.RANGES))
        windows = preprocessing_service.create_sliding_windows(batch, window_size=20, stride=5)
        assert len(windows) > 0
        for window in windows:
            features = preprocessing_service.extract_statistical_features(window)
            assert not np.any(np.isnan(features))
