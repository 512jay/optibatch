# core/validation.py

from typing import Any
from pathlib import Path


REQUIRED_TESTER_FIELDS = {
    "Expert",
    "Symbol",
    "Deposit",
    "Currency",
    "Leverage",
    "Model",
    "Optimization",
    "OptimizationCriterion",
    "ForwardMode",
    "FromDate",
    "ToDate",
}


def validate_optibatch_config(
    data: dict[str, Any], source: Path | str = ""
) -> list[str]:
    """Returns a list of error messages if validation fails. Empty list = OK."""
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["Config root is not a dictionary"]

    if "tester" not in data:
        errors.append("Missing 'tester' section")
    else:
        tester = data["tester"]
        for field in REQUIRED_TESTER_FIELDS:
            if field not in tester:
                errors.append(f"Missing tester.{field}")

    if "inputs" not in data or not isinstance(data["inputs"], dict):
        errors.append("Missing or invalid 'inputs' section")

    if "meta" in data:
        meta = data["meta"]
        if not isinstance(meta.get("saved_at", ""), str):
            errors.append("meta.saved_at must be a string")
        if meta.get("created_by") != "Optibatch":
            errors.append("meta.created_by must be 'Optibatch'")
        if not isinstance(meta.get("optibatch_version", ""), str):
            errors.append("meta.optibatch_version must be a string")

    return errors
