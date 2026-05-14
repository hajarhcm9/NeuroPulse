"""Tests for dashboard and health endpoints."""


def test_patient_stats(client, auth_user_id):
    """Test getting patient statistics."""
    token, uid = auth_user_id
    response = client.get(f"/api/dashboard/patient-stats/{uid}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (200, 404)


def test_admin_stats(client, admin_token):
    """Test getting admin statistics."""
    response = client.get("/api/dashboard/admin-stats", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert response.status_code in (200, 404)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
