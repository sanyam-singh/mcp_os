import os
import httpx
from fastapi import HTTPException

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_openweathermap_weather(lat: float, lon: float):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeatherMap API key not configured")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from OpenWeatherMap")

    return response.json()
