# File: utils/ini_loader.py
# Purpose: Load and parse MT5 .ini strategy configuration files and strategy input parameters.

import configparser


def parse_tester_inputs_section(inputs):
    """
    Parses the [TesterInputs] section of the INI file into a structured dictionary.
    Assumes format: key=value||start||step||end||Y/N
    """
    parsed = {}
    for key, value in inputs.items():
        parts = value.split("||")
        if len(parts) < 5:
            continue

        param_entry = {
            "default": float(parts[0]),
            "start": float(parts[1]),
            "step": float(parts[2]),
            "end": float(parts[3]),
            "optimize": parts[4] == "Y",
        }

        parsed[key] = param_entry

    return parsed


def parse_ini_file(filepath):
    """
    Parses the INI file, preserving the original case of keys.
    Returns a dictionary including both [Tester] and [TesterInputs] sections.
    """
    parser = configparser.ConfigParser()
    parser.optionxform = str  # preserve case
    with open(filepath, encoding="utf-16") as f:
        parser.read_file(f)

    tester = dict(parser["Tester"])
    inputs = dict(parser["TesterInputs"])

    # Optional convenience shortcut
    tester["expert_path"] = tester.get("Expert", "")
    tester["inputs"] = inputs  # attach separately for downstream use

    return tester
