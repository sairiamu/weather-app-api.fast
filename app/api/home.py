from dotenv import load_dotenv

load_dotenv()


def home():
    """A simple heartbeat/home response.

    This function is used by the `/home` endpoint and is intended to quickly
    verify that the service is running.
    """

    return {
        "status": "ok",
        "message": "Weather API is running.",
        "endpoints": {
            "/weather": "GET query param name=<city>",
            "/about": "GET API metadata and documentation",
            "/": "GET welcome message",
        },
    }
