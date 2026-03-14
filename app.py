"""Entry point to expose the FastAPI app for uvicorn and testing.

This module is intentionally small so that deployment tooling can point at
`app:app` and unit tests can import `app` without requiring non-standard paths.

Note: The main application code lives in `.venv/app/main.py` for this repository.
"""

from importlib import util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAIN_PATH = ROOT / ".venv" / "app" / "main.py"

spec = util.spec_from_file_location("weather_app_main", str(MAIN_PATH))
module = util.module_from_spec(spec)
spec.loader.exec_module(module)

app = module.app
