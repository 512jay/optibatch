# optibach/core/registry.py

import os
import json
from pathlib import Path
from typing import Optional, Any
from dotenv import load_dotenv
from core.types import WindowGeometry  

load_dotenv()  # Load environment variables from .env


def get_last_used_install() -> Optional[str]:
    reg = load_registry()
    return reg.get("last_used")


def set_last_used_install(install_id: str):
    reg = load_registry()
    if install_id in reg:
        reg["last_used"] = install_id
        save_registry(reg)


def get_registry_path() -> Path:
    """Determine the correct path for the registry file based on the current environment."""
    env = os.getenv("OPTIBACH_ENV", "dev").lower()

    if env == "prod":
        path = Path.home() / ".optibach" / "mt5_registry.json"
    else:
        path = Path(__file__).resolve().parent.parent / "data" / "mt5_registry.json"

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_registry() -> dict:
    """Load the MT5 registry from disk."""
    path = get_registry_path()
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_registry(registry: dict):
    """Save the MT5 registry to disk."""
    path = get_registry_path()
    with path.open("w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def update_geometry(
    mt5_path: Path, geometry: WindowGeometry, install_id: Optional[str] = None
):

    """
    Update window geometry for a specific MT5 install.
    If install_id is provided, use it as the registry key.
    Otherwise, fall back to using the resolved path.
    """
    registry = load_registry()

    key = install_id if install_id else str(mt5_path.resolve())
    if key not in registry:
        registry[key] = {"path": str(mt5_path.resolve())}

    registry[key]["geometry"] = geometry
    save_registry(registry)


def get_geometry(install_id: str) -> Optional[WindowGeometry]:
    """Retrieve stored geometry using the install ID."""
    registry = load_registry()
    return registry.get(install_id, {}).get("geometry")


def update_click_position(install_id: str, position: tuple[int, int]):
    registry = load_registry()
    if install_id not in registry:
        raise ValueError(f"Install '{install_id}' not found.")
    registry[install_id]["click_position"] = position
    save_registry(registry)


def get_click_position(install_id: str) -> Optional[tuple[int, int]]:
    registry = load_registry()
    if install_id in registry:
        return tuple(registry[install_id].get("click_position", ()))
    return None
