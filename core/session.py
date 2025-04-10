# core/session.py

import json
from dataclasses import asdict
from pathlib import Path
from core.input_parser import InputParam

CACHE_DIR = Path(".cache")
CURRENT_INI = CACHE_DIR / "current_config.ini"
CURRENT_INI_DATA = CACHE_DIR / "current_config.json"


def update_json_tester_inputs(path: Path, inputs: list[InputParam]) -> None:
    if not path.exists():
        return

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    data["TesterInputs"] = [asdict(param) for param in inputs]

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def cache_ini_file(src: Path, data: dict) -> None:
    """Save both the raw ini text and parsed dictionary."""
    CACHE_DIR.mkdir(exist_ok=True)

    # Save the UTF-16 ini file content
    content = src.read_text(encoding="utf-16")
    CURRENT_INI.write_text(content, encoding="utf-16")

    # Save the parsed data (for faster reload later)
    CURRENT_INI_DATA.write_text(
        json.dumps(
            {
                "path": str(src),
                "tester": data.get("tester", {}),
                "inputs": data.get("inputs", {}),
            },
            indent=2,
        )
    )


def get_cached_ini_file() -> Path:
    return CURRENT_INI


def has_cached_ini() -> bool:
    return CURRENT_INI.exists()


def get_field(data: dict, key: str, default=None):
    """Safe getter with optional default."""
    return data.get(key, default)


def update_date_fields(from_date: str, to_date: str) -> None:
    """Placeholder to be overridden by GUI update logic."""
    # You can hook this into real logic from the UI later
    print(f"[DEBUG] Update GUI from date: {from_date} to {to_date}")
