# core/input_parser.py

from typing import List, Dict, TypedDict


class InputParam(TypedDict):
    name: str
    default: float
    start: float
    step: float
    stop: float
    optimize: bool


def parse_ini_inputs(inputs_section: Dict[str, str]) -> List[Dict]:
    """
    Parses [TesterInputs] section into a structured list of input dictionaries.
    """
    results = []

    for name, line in inputs_section.items():
        parts = line.split("||")
        if len(parts) != 5:
            continue

        default, start, step, stop, flag = parts
        try:
            entry = {
                "name": name,
                "default": float(default),
                "start": float(start),
                "step": float(step),
                "stop": float(stop),
                "optimize": flag.upper() == "Y",
            }
            results.append(entry)
        except ValueError:
            # Skip invalid number formats silently
            continue

    return results
