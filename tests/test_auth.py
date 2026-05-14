"""Tests for authentication endpoints."""


def test_register(client):
    """Test user registration."""
    import uuid
    unique = "reg_" + str(uuid.uuid4())[:8]
    response = client.post("/api/auth/register", json={
        "email": f"{unique}@test.com",
        "username": f"user_{unique}",
        "password": "Testpass123",
    })
    assert response.status_code in (200, 201)


def test_register_duplicate_email(client):
    """Test registration with duplicate email."""
    import uuid
    unique = "dup_" + str(uuid.uuid4())[:8]
    payload = {
        "email": f"{unique}@test.com",
        "username": f"user_{unique}",
        "password": "Testpass123",
    }
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code in (400, 409)


def test_login(client):
    """Test user login."""
    import uuid
    unique = "log_" + str(uuid.uuid4())[:8]
    client.post("/api/auth/register", json={
        "email": f"{unique}@test.com",
        "username": f"user_{unique}",
        "password": "Testpass123",
    })
    response = client.post("/api/auth/login", json={
        "username": f"{unique}@test.com",
        "password": "Testpass123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    """Test login with wrong password."""
    import uuid
    unique = "wp_" + str(uuid.uuid4())[:8]
    client.post("/api/auth/register", json={
        "email": f"{unique}@test.com",
        "username": f"user_{unique}",
        "password": "Testpass123",
    })
    response = client.post("/api/auth/login", json={
        "username": f"{unique}@test.com",
        "password": "Wrongpass123",
    })
    assert response.status_code in (401, 400)


def test_get_current_user(client, auth_token):
    """Test getting current user info via /api/users/me."""
    response = client.get("/api/users/me", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200


def test_unauthorized_access(client):
    """Test accessing protected route without token."""
    response = client.get("/api/users/me")
    assert response.status_code in (401, 403)
