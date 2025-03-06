# tests/test_app.py
import json
import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_analyze_endpoint(client):
    # A simple test to check if the endpoint returns a valid response.
    test_data = {"contract_text": "This is a sample clause text for testing."}
    response = client.post("/analyze", json=test_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "risk_score" in data
    assert "flagged" in data
    assert "explanation" in data


def test_missing_payload(client):
    response = client.post("/analyze", json={})
    assert response.status_code == 400
