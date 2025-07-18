import httpx
from fastapi import HTTPException

BASE_URL = "https://api.open-meteo.com/v1/forecast"

async def get_weather_forecast(latitude: float, longitude: float, days: int = 7, include_hourly: bool = False):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "forecast_days": days,
    }
    if include_hourly:
        params["hourly"] = "temperature_2m,relativehumidity_2m,weathercode"

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from OpenMeteo")

    return response.json()

async def get_current_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from OpenMeteo")

    return response.json()

async def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum",
    }
    historical_url = "https://archive-api.open-meteo.com/v1/era5"

    async with httpx.AsyncClient() as client:
        response = await client.get(historical_url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from OpenMeteo")

    return response.json()
