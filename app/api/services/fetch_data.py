import os

import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
IP_GEO_URL = "https://ip-api.com/json"  # Free lookup for IP -> location (no API key)


class WeatherRequest(BaseModel):
    city: str
    api_key: str = ""
    units: str = "metric"  # metric | imperial | standard


async def get_location_from_ip(ip: str) -> dict:
    """Return location data (city, lat/lon, etc.) by IP address."""

    url = f"{IP_GEO_URL}/{ip}" if ip and ip not in ("127.0.0.1", "::1", "localhost") else IP_GEO_URL

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to resolve location from IP")

    data = response.json()

    if data.get("status") == "fail":
        raise HTTPException(status_code=400, detail=f"IP lookup failed: {data.get('message')}")

    return {
        "ip": data.get("query"),
        "city": data.get("city"),
        "region": data.get("regionName"),
        "country": data.get("country"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
    }


async def get_weather_by_coords(lat: float, lon: float, units: str = "metric") -> dict:
    """Fetch weather for a specific latitude/longitude."""

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing WEATHER_API_KEY. Set it via environment variables or in a .env file.",
        )

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OPENWEATHER_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("message", "Failed to fetch weather data"),
        )

    data = response.json()

    return {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temperature": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "description": data.get("weather", [{}])[0].get("description"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "units": units,
    }


async def get_weather(payload: WeatherRequest):
    """Fetch current weather from OpenWeatherMap.

    The OpenWeatherMap API key is taken from the payload first and falls back to
    the `WEATHER_API_KEY` environment variable.
    """

    api_key = payload.api_key or os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing WEATHER_API_KEY. Set it via environment variables or in a .env file.",
        )

    params = {
        "q": payload.city,
        "appid": api_key,
        "units": payload.units,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OPENWEATHER_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("message", "Failed to fetch weather data"),
        )

    data = response.json()

    return {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temperature": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "description": data.get("weather", [{}])[0].get("description"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "units": payload.units,
    }
