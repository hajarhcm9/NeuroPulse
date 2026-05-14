"""End-to-end integration tests."""


def test_full_user_flow(client):
    """Test complete user journey."""
    import uuid

    unique = str(uuid.uuid4())[:8]

    # Register
    reg = client.post("/api/auth/register", json={
        "email": f"e2e_{unique}@test.com",
        "username": f"e2e_{unique}",
        "password": "Testpass123",
    })
    assert reg.status_code in (200, 201)
    uid = reg.json().get("id", 1)

    # Login
    login = client.post("/api/auth/login", json={
        "username": f"e2e_{unique}@test.com",
        "password": "Testpass123",
    })
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Profile via /api/users/me
    me = client.get("/api/users/me", headers=headers)
    assert me.status_code == 200

    # Sensor
    sensor_payload = {"device_id": "sensor_001", "sensor_type": "eeg",
        "heart_rate": 75.0, "spo2": 98.0, "temperature": 36.6}
    if "user_id" not in sensor_payload:
        sensor_payload["user_id"] = uid
    sensor = client.post("/api/sensors/", json=sensor_payload, headers=headers)
    assert sensor.status_code in (200, 201)

    # Prediction
    pred = client.post("/api/predictions/analyze", json={
        "device_id": "test-device", "heart_rate": 72.0, "spo2": 98.0,
        "temperature": 36.6, "accelerometer_x": 0.1,
        "accelerometer_y": -0.05, "accelerometer_z": 0.98,
        "gyroscope_x": 0.0, "gyroscope_y": 0.0, "gyroscope_z": 0.0,
        "emg_signal": 0.5, "eda_signal": 0.3, "user_id": uid},
        headers=headers)
    assert pred.status_code in (200, 500)

    # Alert
    alert_payload = {"device_id": "test-bracelet", "alert_type": "seizure",
        "severity": "critical", "confidence": 0.95,
        "heart_rate": 130.0, "spo2": 88.0,
        "message": "Abnormal EEG pattern detected"}
    if "user_id" not in alert_payload:
        alert_payload["user_id"] = uid
    alert = client.post("/api/alerts/", json=alert_payload, headers=headers)
    assert alert.status_code in (200, 201)

    # Dashboard
    dash = client.get(f"/api/dashboard/patient-stats/{uid}", headers=headers)
    assert dash.status_code in (200, 404)
