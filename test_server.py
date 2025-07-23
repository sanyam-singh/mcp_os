import pytest
from fastapi.testclient import TestClient
from src.mcp_weather_server.server import app

client = TestClient(app)

def test_get_weather_forecast():
    response = client.post("/mcp", json={
        "tool": "get_weather_forecast",
        "parameters": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "days": 7,
            "include_hourly": False
        }
    })
    assert response.status_code == 200
    assert "daily" in response.json()

def test_get_current_weather():
    response = client.post("/mcp", json={
        "tool": "get_current_weather",
        "parameters": {
            "latitude": 52.52,
            "longitude": 13.41
        }
    })
    assert response.status_code == 200
    assert "current_weather" in response.json()

def test_get_historical_weather():
    response = client.post("/mcp", json={
        "tool": "get_historical_weather",
        "parameters": {
            "latitude": 52.52,
            "longitude": 13.41,
            "start_date": "2023-01-01",
            "end_date": "2023-01-02"
        }
    })
    assert response.status_code == 200
    assert "daily" in response.json()

def test_tool_not_found():
    response = client.post("/mcp", json={"tool": "invalid_tool", "parameters": {}})
    assert response.status_code == 404
    assert response.json() == {"detail": "Tool not found"}

def test_predict_weather_alert(monkeypatch):
    class MockChoice:
        def __init__(self, content):
            self.message = self
            self.content = content

    class MockCompletion:
        def __init__(self, content):
            self.choices = [MockChoice(content)]

    def mock_create(*args, **kwargs):
        return MockCompletion("Sunny with a chance of meatballs.")

    monkeypatch.setattr("openai.resources.chat.completions.Completions.create", mock_create)
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    response = client.post("/mcp", json={
        "tool": "predict_weather_alert",
        "parameters": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "crops": ["wheat", "corn"]
        }
    })
    assert response.status_code == 200
    assert "alert" in response.json()
    assert response.json()["alert"] == "Sunny with a chance of meatballs."
