# core/loader.py

from pathlib import Path
from configparser import ConfigParser
from typing import Any


def load_ini_file(path: Path) -> dict[str, Any]:
    config = ConfigParser()
    config.optionxform = str  # type: ignore[assignment]
    config.read(path, encoding="utf-16")

    tester = dict(config.items("Tester")) if config.has_section("Tester") else {}
    inputs = (
        dict(config.items("TesterInputs")) if config.has_section("TesterInputs") else {}
    )

    return {
        "path": str(path),
        "tester": tester,  # raw [Tester] key-value pairs
        "inputs": inputs,  # raw [TesterInputs] key-value pairs
        "raw": config,  # full ConfigParser object (for round-tripping if needed)
    }
