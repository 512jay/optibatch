# File: state.py
# Purpose: Centralized application state for GUI and config logic

from pathlib import Path
from typing import Any
from state.app_state import AppState

# Global shared state across UI + helpers
state = AppState()

# Strategy inputs parsed from [TesterInputs] in INI
parsed_strategy_inputs: dict[str, dict[str, Any]] = {}

# Path to persistent user configuration (e.g., terminal path)
SETTINGS_PATH = Path("settings.json")
