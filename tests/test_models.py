"""Smart Guardian - Model and service unit tests"""

import pytest
import numpy as np
from app.services.preprocessing_service import preprocessing_service
from app.services.model_service import model_service


class TestPreprocessingService:
    """Tests for the preprocessing service"""

    def test_normalize_heart_rate(self):
        result = preprocessing_service.normalize(125.0, "heart_rate")
        assert 0.0 <= result <= 1.0
        assert result == pytest.approx((125.0 - 30.0) / (220.0 - 30.0), abs=0.01)

    def test_normalize_spo2(self):
        result = preprocessing_service.normalize(98.0, "spo2")
        assert 0.0 <= result <= 1.0

    def test_normalize_out_of_range_clamps(self):
        result = preprocessing_service.normalize(300.0, "heart_rate")
        assert result == 1.0

    def test_normalize_zero_range(self):
        result = preprocessing_service.normalize(0.5, "emg_signal")
        assert 0.0 <= result <= 1.0

    def test_denormalize(self):
        normalized = preprocessing_service.normalize(75.0, "heart_rate")
        denormalized = preprocessing_service.denormalize(normalized, "heart_rate")
        assert denormalized == pytest.approx(75.0, abs=0.1)

    def test_normalize_vector(self):
        data = {"heart_rate": 75.0, "spo2": 98.0, "temperature": 36.6}
        result = preprocessing_service.normalize_vector(data)
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float32
        assert len(result) == len(preprocessing_service.RANGES)

    def test_normalize_vector_with_missing(self):
        data = {"heart_rate": 75.0}
        result = preprocessing_service.normalize_vector(data)
        assert isinstance(result, np.ndarray)
        assert result[0] > 0  # heart_rate normalized
        assert result[1] == 0.0  # spo2 missing -> 0

    def test_extract_statistical_features(self):
        window = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=np.float32)
        features = preprocessing_service.extract_statistical_features(window)
        assert isinstance(features, np.ndarray)
        assert len(features) == 12  # 2 channels * 6 stats
        assert features[0] == pytest.approx(3.0, abs=0.01)  # mean of col 0

    def test_create_sliding_windows(self):
        data = np.random.randn(100, 3).astype(np.float32)
        windows = preprocessing_service.create_sliding_windows(data, window_size=50, stride=10)
        assert len(windows) > 0
        assert windows[0].shape == (50, 3)

    def test_create_sliding_windows_padding(self):
        data = np.random.randn(10, 3).astype(np.float32)
        windows = preprocessing_service.create_sliding_windows(data, window_size=50)
        assert len(windows) == 1
        assert windows[0].shape == (50, 3)

    def test_detect_artifacts_none_value(self):
        data = {"heart_rate": None, "spo2": 98.0}
        artifacts = preprocessing_service.detect_artifacts(data)
        assert artifacts["heart_rate"] is True
        assert artifacts["spo2"] is False

    def test_detect_artifacts_out_of_range(self):
        data = {"heart_rate": 300.0, "spo2": 98.0}
        artifacts = preprocessing_service.detect_artifacts(data)
        assert artifacts["heart_rate"] is True
        assert artifacts["spo2"] is False

    def test_preprocess_for_model(self):
        data = {"heart_rate": 75.0, "spo2": 98.0, "temperature": 36.6}
        result = preprocessing_service.preprocess_for_model(data)
        assert isinstance(result, np.ndarray)
        assert all(0.0 <= v <= 1.0 for v in result)

    def test_preprocess_batch(self):
        data_list = [
            {"heart_rate": 75.0, "spo2": 98.0},
            {"heart_rate": 90.0, "spo2": 95.0},
        ]
        result = preprocessing_service.preprocess_batch(data_list)
        assert result.shape == (2, len(preprocessing_service.RANGES))


class TestModelService:
    """Tests for the AI model service"""

    def test_model_not_loaded_initially(self):
        service = model_service.__class__()
        service._model = None
        assert service.is_loaded is False

    def test_dummy_predict(self):
        service = model_service.__class__()
        service._model = service._create_dummy_model()
        features = np.zeros((1, 11), dtype=np.float32)
        result = service.predict(features)
        assert "seizure_probability" in result
        assert "is_seizure" in result
        assert "confidence" in result
        assert "model_version" in result

    def test_dummy_model_info(self):
        service = model_service.__class__()
        service._model = service._create_dummy_model()
        info = service.get_model_info()
        assert info["model_type"] == "dummy"
        assert info["status"] == "development"
        assert "threshold" in info
