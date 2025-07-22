import os
import httpx
from fastapi import HTTPException

BASE_URL = "https://serpapi.com/search"

async def get_google_weather(query: str, api_key: str):
    if not api_key:
        raise HTTPException(status_code=500, detail="SerpApi API key not configured")

    params = {
        "q": query,
        "engine": "google",
        "api_key": api_key,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from SerpApi")

    return response.json()