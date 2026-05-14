"""Smart Guardian - Test fixtures (sync SQLAlchemy)"""

import os
import sys
import uuid
import pytest
from fastapi.testclient import TestClient

# Project root on PATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Override env *before* importing app
os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "false"
os.environ["MQTT_BROKER_HOST"] = "localhost"
os.environ["MQTT_BROKER_PORT"] = "1883"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from main import app

# Test engine & session (sync SQLite)
test_engine = create_engine("sqlite:///test.db", echo=False)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Yield a test DB session."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Setup / teardown

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


# Auth helpers

@pytest.fixture
def auth_token(client):
    unique = str(uuid.uuid4())[:8]
    client.post("/api/auth/register", json={
        "email": f"test_{unique}@test.com",
        "username": f"testuser_{unique}",
        "password": "Testpass123",
    })
    resp = client.post("/api/auth/login", json={
        "username": f"test_{unique}@test.com",
        "password": "Testpass123",
    })
    return resp.json()["access_token"]


@pytest.fixture
def auth_user_id(client):
    """Register, login, return (token, user_id)."""
    from app.models.user import User
    unique = str(uuid.uuid4())[:8]
    client.post("/api/auth/register", json={
        "email": f"uid_{unique}@test.com",
        "username": f"uiduser_{unique}",
        "password": "Testpass123",
    })
    resp = client.post("/api/auth/login", json={
        "username": f"uid_{unique}@test.com",
        "password": "Testpass123",
    })
    token = resp.json()["access_token"]
    # Get user id from DB
    db = TestSessionLocal()
    user = db.query(User).filter(User.email == f"uid_{unique}@test.com").first()
    uid = user.id if user else 1
    db.close()
    return token, uid


@pytest.fixture
def admin_token(client):
    from app.models.user import User
    from sqlalchemy import update
    unique = str(uuid.uuid4())[:8]
    client.post("/api/auth/register", json={
        "email": f"admin_{unique}@test.com",
        "username": f"admin_{unique}",
        "password": "Adminpass123",
    })
    db = TestSessionLocal()
    stmt = update(User).where(User.username == f"admin_{unique}").values(
        role="admin", is_superuser=True
    )
    db.execute(stmt)
    db.commit()
    db.close()
    resp = client.post("/api/auth/login", json={
        "username": f"admin_{unique}@test.com",
        "password": "Adminpass123",
    })
    return resp.json()["access_token"]


@pytest.fixture
def admin_user_id(client):
    """Register admin, return (token, user_id)."""
    from app.models.user import User
    from sqlalchemy import update
    unique = str(uuid.uuid4())[:8]
    client.post("/api/auth/register", json={
        "email": f"admu_{unique}@test.com",
        "username": f"admu_{unique}",
        "password": "Adminpass123",
    })
    db = TestSessionLocal()
    stmt = update(User).where(User.username == f"admu_{unique}").values(
        role="admin", is_superuser=True
    )
    db.execute(stmt)
    db.commit()
    user = db.query(User).filter(User.username == f"admu_{unique}").first()
    uid = user.id if user else 1
    db.close()
    resp = client.post("/api/auth/login", json={
        "username": f"admu_{unique}@test.com",
        "password": "Adminpass123",
    })
    return resp.json()["access_token"], uid


# Cleanup

def pytest_sessionfinish(session, exitstatus):
    db_path = os.path.join(PROJECT_ROOT, "test.db")
    if os.path.exists(db_path):
        os.remove(db_path)
