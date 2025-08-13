# app/tests/test_auth.py
from app.core.security import get_current_user

def test_me_unauthorized(client):
    r = client.get("/auth/me")
    assert r.status_code == 401

def test_me_ok(client):
    class U: id=1; email="u@e.com"; name=None
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: U()
    try:
        r = client.get("/auth/me")
        assert r.status_code == 200 and r.json()["id"] == 1
    finally:
        app.dependency_overrides.clear()
