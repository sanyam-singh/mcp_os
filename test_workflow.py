import pytest
from unittest.mock import patch
from src.mcp_weather_server.tools import geographic_tools, crop_calendar_tools, open_meteo, alert_generation_tools

@pytest.mark.asyncio
@patch('src.mcp_weather_server.tools.openai_llm.predict_weather_alert')
async def test_alert_generation_workflow(mock_predict_weather_alert):
    # Mock the alert generation
    mock_predict_weather_alert.return_value = {
        "alert": "Heavy rainfall expected",
        "impact": "High risk of waterlogging in fields.",
        "recommendations": "Ensure proper drainage in fields."
    }

    # 1. Location Processing
    state = "bihar"
    district = "Patna"
    villages_response = await geographic_tools.list_villages(state=state, district=district)
    assert "error" not in villages_response, f"Failed to get villages: {villages_response.get('error')}"

    village = villages_response["villages"][0]

    coordinates_response = await geographic_tools.reverse_geocode(location_name=village)
    assert "error" not in coordinates_response, f"Failed to get coordinates: {coordinates_response.get('error')}"

    lat = coordinates_response["latitude"]
    lon = coordinates_response["longitude"]

    # 2. Crop Assessment
    season = "Rabi"
    prominent_crops_response = await crop_calendar_tools.get_prominent_crops(region=state, season=season)
    assert "error" not in prominent_crops_response, f"Failed to get prominent crops: {prominent_crops_response.get('error')}"

    crop = prominent_crops_response["crops"][0]

    plant_date = "2023-11-01"
    current_date = "2024-02-15"
    crop_stage_response = await crop_calendar_tools.estimate_crop_stage(crop=crop, plant_date=plant_date, current_date=current_date)
    assert "error" not in crop_stage_response, f"Failed to estimate crop stage: {crop_stage_response.get('error')}"

    growth_stage = crop_stage_response["stage"]

    # 3. Weather Analysis
    weather_forecast_response = await open_meteo.get_weather_forecast(latitude=lat, longitude=lon)
    assert "error" not in weather_forecast_response, f"Failed to get weather forecast: {weather_forecast_response.get('error')}"

    # 4. Alert Generation
    api_key = "test_api_key"
    alert_response = await alert_generation_tools.generate_weather_alert(crop=crop, weather_data=weather_forecast_response, growth_stage=growth_stage, api_key=api_key, latitude=lat, longitude=lon)

    assert alert_response is not None, "Failed to generate alert"
    assert "error" not in alert_response, f"Alert generation failed: {alert_response.get('error')}"

    print("Generated Alert:", alert_response)
