# File: tests/test_ini_loader.py

import json
import random
from pathlib import Path
from ini_utils.loader import parse_ini_file, parse_tester_inputs_section

SETTINGS_PATH = Path("settings.json")


def get_random_optimization_ini():
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)

    profile_dir = Path(settings["data_path"]) / "MQL5" / "Profiles" / "Tester"
    ini_files = list(profile_dir.glob("*.ini"))

    optimization_inis = []
    for ini in ini_files:
        try:
            text = ini.read_text(encoding="utf-16")
            if (
                "FromDate=" in text
                and "Optimization=" in text
                and "TesterInputs" in text
            ):
                optimization_inis.append(ini)
        except Exception:
            continue

    if optimization_inis:
        return random.choice(optimization_inis)

    return None


def test_parse_ini_file_reads_main_keys():
    ini_file = get_random_optimization_ini()
    assert (
        ini_file is not None
    ), "No optimization INI file found in MQL5/Profiles/Tester directory"

    ini_data = parse_ini_file(ini_file)
    assert "Expert" in ini_data
    assert "FromDate" in ini_data
    assert "ToDate" in ini_data
    assert "ForwardMode" in ini_data
    assert "expert_path" in ini_data
    assert "inputs" in ini_data


def test_parse_tester_inputs_section_parses_values():
    ini_file = get_random_optimization_ini()
    assert (
        ini_file is not None
    ), "No optimization INI file found in MQL5/Profiles/Tester directory"

    ini_data = parse_ini_file(ini_file)
    parsed_inputs = parse_tester_inputs_section(ini_data["inputs"])

    for key, value in parsed_inputs.items():
        assert set(value.keys()) == {"default", "start", "step", "end", "optimize"}
        assert isinstance(value["default"], float)
