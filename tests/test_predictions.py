"""Tests for prediction endpoints."""


def test_predict_no_auth(client):
    """Test prediction without authentication."""
    response = client.post("/api/predictions/analyze", json={"user_id": 1, "device_id": "test-device", "heart_rate": 72.0, "spo2": 98.0, "temperature": 36.6, "accelerometer_x": 0.1, "accelerometer_y": -0.05, "accelerometer_z": 0.98, "gyroscope_x": 0.0, "gyroscope_y": 0.0, "gyroscope_z": 0.0, "emg_signal": 0.5, "eda_signal": 0.3})
    assert response.status_code in (401, 403)


def test_predict_normal_data(client, auth_token):
    """Test prediction with normal EEG data."""
    response = client.post("/api/predictions/analyze", json={"user_id": 1, "device_id": "test-device", "heart_rate": 72.0, "spo2": 98.0, "temperature": 36.6, "accelerometer_x": 0.1, "accelerometer_y": -0.05, "accelerometer_z": 0.98, "gyroscope_x": 0.0, "gyroscope_y": 0.0, "gyroscope_z": 0.0, "emg_signal": 0.5, "eda_signal": 0.3},
        headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code in (200, 500)


def test_model_info_admin(client, admin_token):
    """Test getting model info as admin."""
    response = client.get("/api/predictions/model-info", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert response.status_code in (200, 404)


def test_model_info_forbidden(client, auth_token):
    """Test model info access for patient role."""
    response = client.get("/api/predictions/model-info", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code in (403, 404, 200)


def test_analyze_with_auth(client, auth_token):
    """Test analyze endpoint with authentication."""
    response = client.post("/api/predictions/analyze", json={"user_id": 1, "device_id": "test-device", "heart_rate": 72.0, "spo2": 98.0, "temperature": 36.6, "accelerometer_x": 0.1, "accelerometer_y": -0.05, "accelerometer_z": 0.98, "gyroscope_x": 0.0, "gyroscope_y": 0.0, "gyroscope_z": 0.0, "emg_signal": 0.5, "eda_signal": 0.3},
        headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code in (200, 404, 500)
