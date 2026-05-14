import os, sys, json
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
os.environ["DATABASE_URL"] = "sqlite://test.db"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "false"
os.environ["MQTT_BROKER_HOST"] = "localhost"
os.environ["MQTT_BROKER_PORT"] ="1883"
from fastapi.testclient import TestClient
try:
    from main import app
except ImportError:
    from app.main import app
from app.core.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
test_engine = create_engine("sqllite://test.db", echo=False)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
Base.metadata.create_all(bind=test_engine)
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
print("==" * 40)
print("STEP 1: Register + Login")
print("==" * 40)
=reg = client.post("/api/auth/register", json={"email": "debug@test.com", "username": "debuguser", "password": "Debugpass123"})
print(f"  Register: {reg.status_code} -> {reg.json()}")
login = client.post("/api/auth/login", json={"username": "debug@test.com", "password": "Debugpass123"})
print(f"  Login: {login.status_code}")
token = ""
if login.status_code == 200:
    token = login.json().get("access_token", "")
    print(f"  Token: {token[30]}...")
else:
    print(f"  Login failed: {login.text}")
headers = {"Authorization": f"Bearer {token}"}
print("\n" + "=" * 40 + "\nSTEP 2: Test alert creation")
print("==" * 40)
resp = client.post("/api/alerts/", json={"user_id": 1, "device_id": "test-bracelet", "alert_type": "seizure", "severity": "critical", "confidence": 0.95, "heart_rate": 130.0, "spo2": 88.0, "message": "Test seizure alert"}, headers=headers)
print(f"  Alert: {resp.status_code}")
print(f"  Response: {json.dumps(resp.json(), indent=2)}")
print("\n" + "=" * 40 + "\nSTEP 3: Test notification creation")
print("==" * 40)
resp = client.post("/api/notifications/", json={"user_id": 1, "channel": "push", "title": "Test Alert", "body": "This is a test"}, headers=headers)
print(f"  Notification: {resp.status_code}")
print(f"  Response: {json.dumps(resp.json(), indent=2)}")
print("\n" + "=" * 40 + "\nSTEP 4: Test /api/test/predict")
print("=" * 40)
resp = client.post("/api/test/predict", json={"features": [0.1] * 178})
print(f"  Predict: {resp.status_code}")
print(f"  Response: {json.dumps(resp.json(), indent=2)[:500]}")
print("\n" + "=" * 40 + "\nSTEP 5: Test /api/predictions/analyze")
print("=" * 40)
resp = client.post("/api/predictions/analyze", json={"user_id": 1, "device_id": "test-device", "heart_rate": 72.0, "spo2": 98.0}, headers=headers)
print(f"  Analyze: {resp.status_code}")
print(f"  Response: {json.dumps(resp.json(), indent=2)}")
print("\n" + "=" * 40 + "\nSTEP 6: OpenAPI schemas")
print("=" * 40)
schema = app.openapi()
components = schema.get("components", {}).get("schemas", {})
for name in sorted(components.keys()):
    lower = name.lower()
    if any(kw in lower for kw in ["alert", "notification", "predict", "sensor", "analy", "create"]):
        defn = components[name]
        required = defn.get("required", [])
        props = defn.get("properties", {})
        print(f"\n  Schema: {name}")
        print(f"    Required: {required}")
        for pname, pdef in props.items():
            ptype = pdef.get("type", "?")
            enum = pdef.get("enum", None)
            default = pdef.get("default", "none")
            print(f"    {pname}: type={ptype} enum={enum} default={default}")
print("\nDone.")