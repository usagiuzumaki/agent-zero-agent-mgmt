import pytest
from fastapi.testclient import TestClient
from python.api.aria_fastapi import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Aria is breathing."}

def test_get_chapters():
    response = client.get("/project/1/chapters")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
