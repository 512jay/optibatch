# core/input_hints.py

from typing import Literal, TypedDict, Optional, Union


class InputHint(TypedDict, total=False):
    label: str
    type: Literal["float", "int", "enum"]
    min: Union[int, float]
    max: Union[int, float]
    step: Union[int, float]
    optimize: bool
    allowed_values: list[int]  # Only used for enums


def is_valid_optimization_range(hint: InputHint) -> bool:
    """
    Check if the input hint defines a valid, connected optimization range.
    For enums, the allowed values must be equally spaced.
    """
    if not hint.get("optimize"):
        return False

    if hint["type"] in ("int", "float"):
        return all(k in hint for k in ("min", "max", "step"))

    if hint["type"] == "enum" and "allowed_values" in hint:
        values = sorted(hint["allowed_values"])
        if len(values) < 2:
            return False
        step = values[1] - values[0]
        return all((b - a) == step for a, b in zip(values, values[1:]))

    return False


def detect_enum_like(values: list[str]) -> bool:
    """
    Try to detect if a list of strings represents a small, discrete set.
    Could be used to suggest enum input types.
    """
    return (
        len(values) > 1 and all(v.isdigit() for v in values) and len(set(values)) <= 10
    )


def describe_hint(hint: InputHint) -> str:
    """Generate a human-readable description of an input hint."""
    label = hint.get("label", "(Unnamed)")
    if hint["type"] == "enum":
        return f"{label} [enum: {hint['allowed_values']}]"
    return f"{label} [{hint['type']} {hint['min']}–{hint['max']} step {hint['step']}]"
