import asyncio
from src.mcp_weather_server.tools import geographic_tools, crop_calendar_tools, open_meteo, alert_generation_tools
from unittest.mock import patch

async def main():
    with patch('src.mcp_weather_server.tools.openai_llm.predict_weather_alert') as mock_predict_weather_alert:
        # Mock the alert generation
        mock_predict_weather_alert.return_value = {
            "alert": "Heavy rainfall expected",
            "impact": "High risk of waterlogging in fields.",
            "recommendations": "Ensure proper drainage in fields."
        }

        # 1. Location Processing
        state = "bihar"
        district = "Patna"
        print(f"Fetching villages for {district}, {state}...")
        villages_response = await geographic_tools.list_villages(state=state, district=district)
        if "error" in villages_response:
            print(f"Error: {villages_response['error']}")
            return

        village = villages_response["villages"][0]
        print(f"Selected village: {village}")

        print(f"Getting coordinates for {village}...")
        coordinates_response = await geographic_tools.reverse_geocode(location_name=village)
        if "error" in coordinates_response:
            print(f"Error: {coordinates_response['error']}")
            return

        lat = coordinates_response["latitude"]
        lon = coordinates_response["longitude"]
        print(f"Coordinates: {lat}, {lon}")

        # 2. Crop Assessment
        season = "Rabi"
        print(f"Finding prominent crops for {season} season in {state}...")
        prominent_crops_response = await crop_calendar_tools.get_prominent_crops(region=state, season=season)
        if "error" in prominent_crops_response:
            print(f"Error: {prominent_crops_response['error']}")
            return

        crop = prominent_crops_response["crops"][0]
        print(f"Selected crop: {crop}")

        plant_date = "2023-11-01"
        current_date = "2024-02-15"
        print(f"Estimating crop stage for {crop} planted on {plant_date}...")
        crop_stage_response = await crop_calendar_tools.estimate_crop_stage(crop=crop, plant_date=plant_date, current_date=current_date)
        if "error" in crop_stage_response:
            print(f"Error: {crop_stage_response['error']}")
            return

        growth_stage = crop_stage_response["stage"]
        print(f"Estimated growth stage: {growth_stage}")

        # 3. Weather Analysis
        print("Fetching 7-day weather forecast...")
        weather_forecast_response = await open_meteo.get_weather_forecast(latitude=lat, longitude=lon)
        if "error" in weather_forecast_response:
            print(f"Error: {weather_forecast_response['error']}")
            return
        print("Weather forecast received.")

        # 4. Alert Generation
        print("Generating weather alert...")
        api_key = "test_api_key"
        alert_response = await alert_generation_tools.generate_weather_alert(crop=crop, weather_data=weather_forecast_response, growth_stage=growth_stage, api_key=api_key, latitude=lat, longitude=lon)

        if "error" in alert_response:
            print(f"Error: {alert_response['error']}")
            return

        print("\n--- Generated Weather Alert ---")
        print(f"Alert: {alert_response['alert']}")
        print(f"Impact: {alert_response['impact']}")
        print(f"Recommendations: {alert_response['recommendations']}")
        print("-----------------------------")

if __name__ == "__main__":
    asyncio.run(main())