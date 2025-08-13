# backend/app/tests/test_auth_me.py
from fastapi.testclient import TestClient
from app.main.app import app

client = TestClient(app)

def test_me_unauthorized():
    r = client.get("/auth/me")
    assert r.status_code == 401

def test_me_ok():
    from app.core.security import get_current_user
    class U:
        id = 1; email = "u@e.com"; name = None
    app.dependency_overrides[get_current_user] = lambda: U()
    try:
        r = client.get("/auth/me")
        assert r.status_code == 200
        assert r.json()["id"] == 1
    finally:
        app.dependency_overrides.clear()
