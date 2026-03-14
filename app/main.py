import os

from fastapi import FastAPI, HTTPException, Request
import uvicorn
from dotenv import load_dotenv

from api.core.info import information
from api.home import home
from api.services.fetch_data import (
    get_location_from_ip,
    get_weather,
    get_weather_by_coords,
    WeatherRequest,
)
from api.management import track_request, get_stats

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI(
    title="Weather API",
    description="A lightweight FastAPI service that returns current weather information for a given city using OpenWeatherMap.",
    version="1.0.0",
)

@app.get("/")
def root(request: Request):
    client_ip = request.headers.get("X-Forwarded-For", request.client.host).split(",")[0].strip()
    track_request("/", client_ip)
    return {
        "message": "Welcome to the Weather API",
        "endpoints": ["/weather?name=<city>", "/about", "/home", "/admin"],
    }


@app.get("/home")
def home_show(request: Request):
    client_ip = request.headers.get("X-Forwarded-For", request.client.host).split(",")[0].strip()
    track_request("/home", client_ip)
    return home()


@app.get("/weather")
async def weather(request: Request, name: str | None = None):
    """Get weather by city name or by inferred client location (default)."""

    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="WEATHER_API_KEY is not set. Please set it in your environment or in a .env file.",
        )

    client_ip = request.headers.get("X-Forwarded-For", request.client.host).split(",")[0].strip()

    if name:
        result = await get_weather(WeatherRequest(city=name, api_key=API_KEY))
        track_request("/weather", client_ip)
        return result

    # No name provided → use client IP to infer location and use that as default search
    location = await get_location_from_ip(client_ip)

    weather_data = await get_weather_by_coords(
        lat=location["lat"], lon=location["lon"], units="metric"
    )
    track_request("/weather", client_ip, location)
    return {
        "message": "No city provided; returning weather for your detected location.",
        "location": location,
        "weather": weather_data,
    }


@app.get("/about")
def get_information(request: Request):
    client_ip = request.headers.get("X-Forwarded-For", request.client.host).split(",")[0].strip()
    track_request("/about", client_ip)
    return information()


@app.get("/admin")
def admin_stats(request: Request):
    """Admin endpoint to view API usage statistics."""
    client_ip = request.headers.get("X-Forwarded-For", request.client.host).split(",")[0].strip()
    track_request("/admin", client_ip)
    return get_stats()


if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8989,reload=True)