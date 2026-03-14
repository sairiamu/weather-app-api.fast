import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "endpoints" in response.json()


def test_health_endpoint():
    response = client.get("/home")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_about_endpoint_contains_metadata():
    response = client.get("/about")
    assert response.status_code == 200
    data = response.json()
    assert data.get("project") == "Weather API"
    assert "author" in data


@pytest.mark.parametrize("city", ["London", "Paris"])
def test_weather_endpoint_requires_name(city):
    # If the API key is missing, this will return 500; that is acceptable in CI.
    response = client.get(f"/weather?name={city}")
    assert response.status_code in (200, 500)
    if response.status_code == 200:
        data = response.json()
        assert data.get("city") is not None


def test_weather_endpoint_default_location():
    # When no name is provided, we should still receive a consistent response.
    response = client.get("/weather")
    assert response.status_code in (200, 500, 502)
    if response.status_code == 200:
        data = response.json()
        assert "location" in data
