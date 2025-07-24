import pytest
from fastapi.testclient import TestClient
from src.mcp_weather_server.server import app

client = TestClient(app)

def test_list_villages():
    response = client.post("/mcp", json={"tool": "list_villages", "parameters": {"state": "bihar"}})
    assert response.status_code == 200
    assert response.json() == {"districts": ["Patna", "Gaya", "Muzaffarpur"]}

def test_reverse_geocode():
    response = client.post("/mcp", json={"tool": "reverse_geocode", "parameters": {"location_name": "patna"}})
    assert response.status_code == 200
    assert response.json() == {"latitude": 25.5941, "longitude": 85.1376}

def test_get_administrative_bounds():
    response = client.post("/mcp", json={"tool": "get_administrative_bounds", "parameters": {"village_id": "patna"}})
    assert response.status_code == 200
    assert response.json() == {"type": "Polygon", "coordinates": [[[85.0, 25.5], [85.2, 25.5], [85.2, 25.7], [85.0, 25.7], [85.0, 25.5]]]}

def test_get_crop_calendar():
    response = client.post("/mcp", json={"tool": "get_crop_calendar", "parameters": {"region": "bihar"}})
    assert response.status_code == 200
    assert response.json() == {"crops": ["rice", "wheat", "maize"]}

def test_get_prominent_crops():
    response = client.post("/mcp", json={"tool": "get_prominent_crops", "parameters": {"region": "bihar", "season": "kharif"}})
    assert response.status_code == 200
    assert response.json() == {"crops": ["rice", "maize"]}

def test_estimate_crop_stage():
    response = client.post("/mcp", json={"tool": "estimate_crop_stage", "parameters": {"crop": "rice", "plant_date": "2023-06-01", "current_date": "2023-07-01"}})
    assert response.status_code == 200
    assert response.json() == {"stage": "vegetative"}

def test_analyze_weather_trends():
    response = client.post("/mcp", json={"tool": "analyze_weather_trends", "parameters": {"latitude": 25.5941, "longitude": 85.1376, "period": "7-day"}})
    assert response.status_code == 200
    assert response.json() == {"trend": "clear", "confidence": 0.8}
