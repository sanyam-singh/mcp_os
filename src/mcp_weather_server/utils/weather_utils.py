TOOL_CONFIG = {
    "get_weather_forecast": {"module": "open_meteo"},
    "get_current_weather": {"module": "open_meteo"},
    "get_historical_weather": {"module": "open_meteo"},
    "get_tomorrow_weather": {"module": "tomorrow_io"},
    "get_weather_alerts": {"module": "tomorrow_io"},
    "get_google_weather_current_conditions": {"module": "google_weather"},
    "get_openweathermap_weather": {"module": "openweathermap"},
    "get_accuweather_current_conditions": {"module": "accuweather"},
}

def get_tool_config(tool_name: str):
    return TOOL_CONFIG.get(tool_name)
