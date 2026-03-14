# Weather API

**Author:** Sairiamu Michael Namuti

A minimal FastAPI project that returns current weather information for a given city using the OpenWeatherMap API.

---

## 🚀 Quick Start

### 1) Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Configure your API key

Create a `.env` file in the project root and set your OpenWeatherMap API key:

```ini
WEATHER_API_KEY=YOUR_OPENWEATHER_API_KEY
```

### 3) Run the server

```powershell
python app.py
```

Or using uvicorn directly:

```powershell
uvicorn app:app --reload --host 127.0.0.1 --port 8989
```

By default, the API will run at: `http://127.0.0.1:8989`

---

## 🧭 Endpoints

| Path       | Method | Description                         |
| ---------- | ------ | ----------------------------------- |
| `/`        | GET    | Welcome message + list of endpoints |
| `/home`    | GET    | Healthcheck / home info             |
| `/weather` | GET    | Fetch weather by city name          |
| `/about`   | GET    | API documentation + metadata        |

### 🔍 Weather endpoint

Request (recommended):

```
GET /weather?name=London
```

If you omit `name`, the API will attempt to determine your location from the client IP and return weather for that location:

```
GET /weather
```

Example response:

```json
{
  "city": "London",
  "country": "GB",
  "temperature": 15.8,
  "feels_like": 15.0,
  "humidity": 72,
  "description": "broken clouds",
  "wind_speed": 3.6,
  "units": "metric"
}
```

---

## 🧪 Tests

Run the full test suite with:

```powershell
pytest
```

> Note: Tests will pass even if the OpenWeatherMap API key is missing; the suite is designed to allow CI runs without secrets.

## 🛠️ Development

Visit Swagger UI to explore the API interactively:

- http://127.0.0.1:8989/docs

## 🐞 Debugging & Common Issues

### Missing API key

If you see an error like:

> `WEATHER_API_KEY is not set` or `Missing WEATHER_API_KEY`

Then your `.env` file is missing or the variable is not set. Add it and restart the server.

### Invalid city name

If OpenWeatherMap returns a `404` with `city not found`, verify that the `name` query parameter is a valid city.

---

## � Deployment

This repo is ready for a 12-factor style deployment. A basic `Procfile` is included to launch the API via Uvicorn:

```text
web: uvicorn app:app --host=0.0.0.0 --port=${PORT:-8989}
```

## �📝 Notes

- This project is meant as a simple, extendable foundation for building weather-related services.
- The full documentation payload is available via the `/about` endpoint.

---

## 📄 License

MIT (Suggested)
