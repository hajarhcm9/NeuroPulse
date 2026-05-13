"""Smart Guardian - API integration tests"""

import pytest


def get_auth_headers(client, email="testapi@smartguardian.com", username="testapiuser", password="TestPass123!"):
    """Helper to register a user and return auth headers"""
    client.post("/api/auth/register", json={
        "email": email,
        "username": username,
        "password": password,
        "first_name": "Test",
        "last_name": "API",
    })
    response = client.post("/api/auth/login", json={"username": email, "password": password})
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}


class TestUserAPI:
    """Tests for user API endpoints"""

    def test_get_current_user(self, client):
        headers = get_auth_headers(client)
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "username" in data

    def test_update_current_user(self, client):
        headers = get_auth_headers(client)
        response = client.put("/api/users/me", headers=headers, json={"first_name": "Updated"})
        assert response.status_code == 200
        assert response.json()['first_name'] == "Updated"

    def test_unauthorized_access(self, client):
        response = client.get("/api/users/me")
        assert response.status_code == 403

    def test_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 401


class TestSensorAPI:
    """Tests for sensor data API endpoints"""

    def test_create_sensor_data(self, client, sample_sensor_data):
        headers = get_auth_headers(client, email="sensor@test.com", username="sensoruser")
        response = client.post("/api/sensors/", headers=headers, json=sample_sensor_data)
        assert response.status_code == 201
        data = response.json()
        assert data['device_id'] == sample_sensor_data['device_id']
        assert data['heart_rate'] == sample_sensor_data['heart_rate']

    def test_get_user_sensor_data(self, client):
        headers = get_auth_headers(client, email="sensor2@test.com", username="sensoruser2")
        client.post("/api/sensors/", headers=headers, json={
            "user_id": 1, "device_id": "DEV-002", "sensor_type": "heart_rate", "heart_rate": 72.0,
        })
        response = client.get("/api/sensors/user/1", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAlertAPI:
    """Tests for alert API endpoints"""

    def test_create_alert(self, client, sample_alert_data):
        headers = get_auth_headers(client, email="alert@test.com", username="alertuser")
        response = client.post("/api/alerts/", headers=headers, json=sample_alert_data)
        assert response.status_code == 201
        data = response.json()
        assert data['alert_type'] == "seizure_detection"
        assert data['severity'] == "warning"

    def test_get_user_alerts(self, client):
        headers = get_auth_headers(client, email="alert2@test.com", username="alertuser2")
        client.post("/api/alerts/", headers=headers, json={
            "user_id": 1, "device_id": "DEV-003", "alert_type": "seizure_detection", "severity": "critical",
        })
        response = client.get("/api/alerts/user/1", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_alert(self, client, sample_alert_data):
        headers = get_auth_headers(client, email="alert3@test.com", username="alertuser3")
        create_resp = client.post("/api/alerts/", headers=headers, json=sample_alert_data)
        alert_id = create_resp.json()['id']
        response = client.put(f"/api/alerts/{alert_id}", headers=headers, json={"is_read": True})
        assert response.status_code == 200
        assert response.json()['is_read'] is True


class TestNotificationAPI:
    """Tests for notification API endpoints"""

    def test_create_notification(self, client):
        headers = get_auth_headers(client, email="notif@test.com", username="notifuser")
        response = client.post("/api/notifications/", headers=headers, json={
            "user_id": 1, "channel": "in_app", "title": "Test Notification", "body": "Hello",
        })
        assert response.status_code == 401

    def test_get_unread_count(self, client):
        headers = get_auth_headers(client, email="notif2@test.com", username="notifuser2")
        response = client.get("/api/notifications/unread-count/1", headers=headers)
        assert response.status_code == 200
        assert "unread_count" in response.json()


class TestExportAPI:
    """Tests for export API endpoints"""

    def test_export_alerts_json(self, client):
        headers = get_auth_headers(client, email="export@test.com", username="exportuser")
        response = client.get("/api/export/alerts/json/1", headers=headers)
        assert response.status_code == 200

    def test_export_sensors_json(self, client):
        headers = get_auth_headers(client, email="export2@test.com", username="exportuser2")
        response = client.get("/api/export/sensors/json/1", headers=headers)
        assert response.status_code == 200

    def test_export_full_report(self, client):
        headers = get_auth_headers(client, email="export3@test.com", username="exportuser3")
        response = client.get("/api/export/full-report/1", headers=headers)
        assert response.status_code == 200
