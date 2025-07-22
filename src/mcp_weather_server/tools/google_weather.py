import os
import httpx
from fastapi import HTTPException

API_KEY = os.getenv("SERPAPI_API_KEY")
BASE_URL = "https://serpapi.com/search"

async def get_google_weather(query: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="SerpApi API key not configured")

    params = {
        "q": query,
        "engine": "google",
        "api_key": API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from SerpApi")

    return response.json()
