"""API metadata and documentation.

This module serves as the single source of truth for documentation returned
by the `/about` endpoint.
"""


def information():
    """Return structured documentation and metadata about the project."""

    return {
        "project": "Weather API",
        "version": "1.0.0",
        "author": "Sairiamu Michael Namuti",
        "description": "A minimal FastAPI application that returns current weather data for a given city using OpenWeatherMap.",
        "license": "MIT (recommended)",
        "endpoints": {
            "/": {
                "method": "GET",
                "description": "Welcome message and list of key endpoints.",
            },
            "/home": {
                "method": "GET",
                "description": "Basic healthcheck/home response.",
            },
            "/weather": {
                "method": "GET",
                "query_parameters": {
                    "name": "City name, e.g. London (optional). If omitted, the service will attempt to infer the caller's city via IP geolocation.",
                },
                "description": "Returns current weather data for a city; if name is not provided, automatically returns weather for the caller’s detected location.",
                "example": "/weather?name=Dar%20es%20Salaam",
            },
            "/about": {
                "method": "GET",
                "description": "Returns this metadata and documentation payload.",
            },
            "/admin": {
                "method": "GET",
                "description": "Returns API usage statistics (requests, users, locations).",
            },
        },
        "environment": {
            "WEATHER_API_KEY": {
                "description": "OpenWeatherMap API key (required).",
                "required": True,
                "example": "YOUR_OPENWEATHER_API_KEY",
            }
        },
        "usage": {
            "setup": [
                "python -m venv .venv",
                "pip install -r requirements.txt",
                "copy .env.example .env  # or create .env and set WEATHER_API_KEY",
            ],
            "run": "python main.py",
            "api_docs": "http://127.0.0.1:8989/docs",
        },
        "examples": {
            "curl": "curl 'http://127.0.0.1:8989/weather?name=London'",
            "python": "import requests\nprint(requests.get('http://127.0.0.1:8989/weather?name=London').json())",
        },
        "debugging": {
            "common_errors": {
                "missing_api_key": {
                    "symptom": "HTTP 500 with message 'WEATHER_API_KEY is not set' or 'Missing WEATHER_API_KEY'",
                    "fix": "Set the environment variable WEATHER_API_KEY (in .env or your environment) and restart the server.",
                },
                "invalid_city": {
                    "symptom": "HTTP 404 from OpenWeatherMap with message 'city not found'",
                    "fix": "Ensure the 'name' query parameter contains a valid city name (e.g., 'London').",
                },
            },
            "tips": [
                "Use /docs (Swagger UI) to test endpoints interactively.",
                "If you encounter rate limiting, upgrade your OpenWeatherMap plan or add caching.",
            ],
        },
        "notes": "This project is a small, extendable foundation for building weather-based services.",
    }
