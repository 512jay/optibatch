# core/input_parser.py

from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class InputParam:
    name: str
    default: str
    start: Optional[str] = None
    step: Optional[str] = None
    end: Optional[str] = None
    optimize: bool = False


def parse_ini_inputs(inputs_section: Dict[str, str]) -> List[InputParam]:
    """
    Parses [TesterInputs] section into a list of InputParam instances.
    """
    results: List[InputParam] = []

    for name, line in inputs_section.items():
        parts = line.split("||")
        if len(parts) != 5:
            continue

        default, start, step, stop, flag = parts

        # No type coercion here – we treat all as strings for consistency
        results.append(
            InputParam(
                name=name,
                default=default,
                start=start or None,
                step=step or None,
                end=stop or None,
                optimize=flag.strip().upper() == "Y",
            )
        )

    return results
