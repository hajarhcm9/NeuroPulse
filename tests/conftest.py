from app.core.database import Base
"""Smart Guardian - Pytest configuration and shared fixtures"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import DeclarativeBase, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test_smart_guardian.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with DB session override"""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Sample user data for registration tests"""
    return {
        "email": "test@smartguardian.com",
        "username": "testuser",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
    }


@pytest.fixture
def sample_login_data():
    """Sample login data"""
    return {
        "username": "test@smartguardian.com",
        "password": "TestPass123!",
    }


@pytest.fixture
def sample_sensor_data():
    """Sample sensor data for testing"""
    return {
        "user_id": 1,
        "device_id": "BK-M01-DEVICE-001",
        "sensor_type": "multi",
        "heart_rate": 75.0,
        "spo2": 98.0,
        "temperature": 36.6,
        "accelerometer_x": 0.1,
        "accelerometer_y": -0.05,
        "accelerometer_z": 9.81,
        "gyroscope_x": 0.0,
        "gyroscope_y": 0.0,
        "gyroscope_z": 0.0,
        "emg_signal": 0.15,
        "eda_signal": 0.3,
    }


@pytest.fixture
def sample_alert_data():
    """Sample alert data for testing"""
    return {
        "user_id": 1,
        "device_id": "BK-M01-DEVICE-001",
        "alert_type": "seizure_detection",
        "severity": "warning",
        "confidence": 0.85,
        "heart_rate": 120.0,
        "spo2": 90.0,
        "message": "Potential seizure detected",
    }


@pytest.fixture
def sample_prediction_data():
    """Sample prediction request data"""
    return {
        "user_id": 1,
        "device_id": "BK-M01-DEVICE-001",
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
