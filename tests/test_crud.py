"""Tests for CRUD operations."""


def test_create_sensor(client, auth_user_id):
    """Test creating a sensor reading."""
    token, uid = auth_user_id
    payload = {"device_id": "sensor_001", "heart_rate": 75, "blood_pressure": 120, "oxygen_level": 98.5, "temperature": 36.6}
    # Add user_id if not present
    if "user_id" not in payload:
        payload["user_id"] = uid
    response = client.post("/api/sensors/", json=payload,
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 201)


def test_get_sensors_by_user(client, auth_user_id):
    """Test getting sensor readings by user."""
    token, uid = auth_user_id
    response = client.get(f"/api/sensors/user/{uid}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200


def test_create_alert(client, auth_user_id):
    """Test creating an alert."""
    token, uid = auth_user_id
    payload = {"device_id": "test-bracelet", "alert_type": "seizure", "severity": "critical", "confidence": 0.95, "heart_rate": 130.0, "spo2": 88.0, "message": "Abnormal EEG pattern detected"}
    if "user_id" not in payload:
        payload["user_id"] = uid
    response = client.post("/api/alerts/", json=payload,
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 201)


def test_get_alerts_by_user(client, auth_user_id):
    """Test getting alerts by user."""
    token, uid = auth_user_id
    response = client.get(f"/api/alerts/user/{uid}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200


def test_create_notification(client, admin_user_id):
    """Test creating a notification (admin only)."""
    token, uid = admin_user_id
    payload = {"alert_id": None, "channel": "push", "title": "System Update", "body": "Test notification"}
    if "user_id" not in payload:
        payload["user_id"] = uid
    response = client.post("/api/notifications/", json=payload,
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 201)


def test_get_notifications_by_user(client, auth_user_id):
    """Test getting notifications by user."""
    token, uid = auth_user_id
    response = client.get(f"/api/notifications/user/{uid}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
