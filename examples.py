import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_example(tool, parameters):
    try:
        response = requests.post(f"{BASE_URL}/mcp", json={"tool": tool, "parameters": parameters})
        response.raise_for_status()
        print(f"--- {tool} Example ---")
        print(json.dumps(response.json(), indent=2))
        print("-" * 20)
    except requests.exceptions.RequestException as e:
        print(f"Error running {tool} example: {e}")

if __name__ == "__main__":
    # OpenMeteo Examples
    run_example("get_weather_forecast", {"latitude": 40.7128, "longitude": -74.0060, "days": 3})
    run_example("get_current_weather", {"latitude": 52.52, "longitude": 13.41})
    run_example("get_historical_weather", {"latitude": 52.52, "longitude": 13.41, "start_date": "2023-01-01", "end_date": "2023-01-02"})

    # Tomorrow.io Examples (requires API key)
    # Note: These will fail if the TOMORROW_IO_API_KEY is not set in a .env file
    run_example("get_tomorrow_weather", {"location": "New York, NY"})
    run_example("get_weather_alerts", {"location": "New York, NY"})

    # Google Weather Example
    run_example("get_google_weather_current_conditions", {"latitude": 37.4220, "longitude": -122.0841})

    # OpenWeatherMap Example
    run_example("get_openweathermap_weather", {"lat": 35, "lon": 139})

    # AccuWeather Example
    # Note: This requires a location key. You can get one from the AccuWeather API.
    run_example("get_accuweather_current_conditions", {"location_key": "349727"})
