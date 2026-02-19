import os
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2] / "src" / "dashboard" / "backend"
sys.path.insert(0, str(BACKEND_DIR))

# Required by app.config.Settings at import time
os.environ.setdefault("HA_TOKEN", "test-ha-token")
os.environ.setdefault("DASHBOARD_API_KEY", "test-api-key")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://dashboard_user:test@localhost/homedb?options=-csearch_path%3Ddashboard",
)
