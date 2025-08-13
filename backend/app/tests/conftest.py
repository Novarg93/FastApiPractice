import os
os.environ["PYTHONPATH"] = "."
from fastapi.testclient import TestClient
from app.main.app import app
import pytest

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
