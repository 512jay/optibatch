# File: core/jobs/settings.py
from pathlib import Path
import json

SETTINGS_PATH = Path("settings.json")


def load_settings() -> dict:
    if SETTINGS_PATH.exists():
        with SETTINGS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}
