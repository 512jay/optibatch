# File: settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / ".optibatch"
DATA_DIR.mkdir(exist_ok=True)

_raw_url = os.getenv("DATABASE_URL")

# Ensure type is always str (not str | None)
if _raw_url and _raw_url.strip():
    DATABASE_URL: str = _raw_url.strip()
    print(f"🔌 Using PostgreSQL from {DATABASE_URL}")
else:
    sqlite_path = DATA_DIR / "optibatch.db"
    DATABASE_URL = f"sqlite:///{sqlite_path.resolve()}"
    print(f"⚠️  DATABASE_URL not set. Using SQLite fallback at {DATABASE_URL}")
