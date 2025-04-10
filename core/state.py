# core/state.py

import json
from pathlib import Path
from typing import Any


STATE_FILE = Path(".cache/app_state.json")


class StateRegistry:
    def __init__(self) -> None:
        self._state: dict[str, Any] = {}

    def register(self, key: str, value: Any) -> None:
        self._state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._state[key] = value

    def all(self) -> dict[str, Any]:
        return self._state.copy()

    def update(self, data: dict[str, Any]) -> None:
        self._state.update(data)

    def export_json(self) -> str:
        return json.dumps(self._state, indent=2)

    def save(self, path: Path = STATE_FILE) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def load(self, path: Path = STATE_FILE) -> None:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                self._state = json.load(f)
        else:
            self._state = {}

registry = StateRegistry()
registry.load()
