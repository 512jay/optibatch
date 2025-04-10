# core/session.py

import json
from dataclasses import asdict
from pathlib import Path
from configparser import ConfigParser
from core.input_parser import InputParam
from dataclasses import asdict
from core.loader import load_ini_file
from core.loader import load_ini_file
from core.input_parser import parse_ini_inputs
from ini_utils.writer import update_ini_tester_inputs
from core.enums import ModelingMode, OptimizationMode, ResultPriority, ForwardMode

CACHE_DIR = Path(".cache")
CURRENT_INI = CACHE_DIR / "current_config.ini"
CURRENT_INI_DATA = CACHE_DIR / "current_config.json"


def load_full_config(parsed_inputs: list[InputParam], ini_path: Path) -> dict:
    """Load the full config from a given INI file and return context dictionary."""
    ini_data = load_ini_file(ini_path)
    parsed_inputs.clear()
    parsed_inputs.extend(parse_ini_inputs(ini_data["inputs"]))

    tester = ini_data["tester"]
    return {
        "expert": tester.get("Expert", ""),
        "symbol": tester.get("Symbol", ""),
        "deposit": tester.get("Deposit", ""),
        "currency": tester.get("Currency", ""),
        "leverage": tester.get("Leverage", ""),
        "modeling": tester.get("Model", ""),
        "optimization": tester.get("Optimization", ""),
        "result": tester.get("OptimizationCriterion", ""),
        "forward": tester.get("ForwardMode", ""),
        "from_date": tester.get("FromDate", ""),
        "to_date": tester.get("ToDate", ""),
    }


def save_full_config(
    parsed_inputs: list[InputParam],
    context: dict[str, str],
) -> None:
    if not CURRENT_INI.exists():
        raise FileNotFoundError("No current_config.ini found")

    parsed_ini = load_ini_file(CURRENT_INI)
    tester = parsed_ini["tester"]
    inputs = parsed_ini["inputs"]
    config = parsed_ini["raw"]

    # Header & strategy
    tester["Symbol"] = context["symbol"]
    tester["Deposit"] = context["deposit"]
    tester["Currency"] = context["currency"]
    tester["Leverage"] = context["leverage"]
    # These are StringVars storing labels (like "Every tick")
    # Convert them to values before saving
    tester["Model"] = ModelingMode.from_label(context["model"]).value
    tester["Optimization"] = OptimizationMode.from_label(context["optimization"]).value
    tester["OptimizationCriterion"] = ResultPriority.from_label(context["result"]).value
    tester["ForwardMode"] = ForwardMode.from_label(context["forward"]).value
    tester["FromDate"] = context["from_date"]
    tester["ToDate"] = context["to_date"]

    # Update [TesterInputs]
    update_ini_tester_inputs(CURRENT_INI, parsed_inputs)

    # Update JSON
    CURRENT_INI_DATA.write_text(
        json.dumps(
            {
                "path": str(CURRENT_INI),
                "tester": tester,
                "inputs": {p.name: asdict(p) for p in parsed_inputs},
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Overwrite INI
    if not config.has_section("Tester"):
        config.add_section("Tester")
    for k, v in tester.items():
        config.set("Tester", k, v)
    with CURRENT_INI.open("w", encoding="utf-16") as f:
        config.write(f)


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
