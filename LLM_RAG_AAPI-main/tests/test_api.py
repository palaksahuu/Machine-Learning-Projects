from fastapi.testclient import TestClient
from api.main import app
import pytest

client = TestClient(app)

# Happy Path Tests
def test_valid_requests():
    test_cases = [
        ("Open Chrome", "open_chrome"),
        ("Show CPU usage", "get_cpu_usage"),
        ("Launch calculator", "open_calculator")
    ]
    
    for prompt, expected_func in test_cases:
        response = client.post("/execute", json={"prompt": prompt})
        assert response.status_code == 200
        assert response.json()["function"] == expected_func
        assert response.json()["status"] == "success"

# Edge Cases
def test_invalid_requests():
    # Unknown function
    response = client.post("/execute", json={"prompt": "Fly to Mars"})
    assert response.status_code == 404
    assert response.json()["status"] == "error"
    
    # Empty prompt
    response = client.post("/execute", json={"prompt": ""})
    assert response.status_code == 404