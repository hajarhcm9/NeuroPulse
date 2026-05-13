"""Smart Guardian - Auth unit tests"""

import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token


class TestPasswordHashing:
    """Tests for password hashing and verification"""

    def test_hash_password(self):
        hashed = hash_password("TestPass123!")
        assert hashed is not None
        assert hashed != "TestPass123!"
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        hashed = hash_password("TestPass123!")
        assert verify_password("TestPass123!", hashed) is True

    def test_verify_password_incorrect(self):
        hashed = hash_password("TestPass123!")
        assert verify_password("WrongPass!", hashed) is False


class TestJWTTokens:
    """Tests for JWT token creation and decoding"""

    def test_create_access_token(self):
        token = create_access_token({"sub": "1", "role": "patient"})
        assert token is not None
        assert isinstance(token, str)

    def test_decode_token(self):
        token = create_access_token({"sub": "1", "role": "patient"})
        payload = decode_token(token)
        assert payload is not None
        assert payload['sub'] == "1"
        assert payload['role'] == "patient"

    def test_decode_invalid_token(self):
        payload = decode_token("invalid.token.here")
        assert payload is None


class TestAuthAPI:
    """Tests for auth API endpoints"""

    def test_register_user(self, client, sample_user_data):
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data['email'] == sample_user_data['email']
        assert data['username'] == sample_user_data['username']
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client, sample_user_data):
        client.post("/api/auth/register", json=sample_user_data)
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 400

    def test_login_success(self, client, sample_user_data, sample_login_data):
        client.post("/api/auth/register", json=sample_user_data)
        response = client.post("/api/auth/login", json=sample_login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data['token_type'] == "bearer"

    def test_login_wrong_password(self, client, sample_user_data):
        client.post("/api/auth/register", json=sample_user_data)
        response = client.post("/api/auth/login", json={"username": "test@smartguardian.com", "password": "WrongPass!"})
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post("/api/auth/login", json={"username": "nobody@test.com", "password": "TestPass123!"})
        assert response.status_code == 401

    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == "running"

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == "healthy"
