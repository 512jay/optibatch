import json
from datetime import datetime
from pathlib import Path
import configparser


def parse_tester_inputs(inputs):
    parsed = {}
    for name, raw in inputs.items():
        parts = raw.split("||")
        if len(parts) < 2:
            continue
        default = eval(parts[0])
        optimize_flag = parts[-1] == "Y"
        entry = {"default": default, "optimize": optimize_flag}

        if optimize_flag and len(parts) >= 5:
            try:
                entry["start"] = eval(parts[1])
                entry["step"] = eval(parts[2])
                entry["end"] = eval(parts[3])
                entry["type"] = "float" if isinstance(default, float) else "int"
            except:
                pass
        elif isinstance(default, bool):
            entry["type"] = "bool"
        elif isinstance(default, int):
            entry["type"] = "int"
        elif isinstance(default, float):
            entry["type"] = "float"
        else:
            entry["type"] = "enum"
        parsed[name] = entry
    return parsed


def prompt(field, default=None, cast=str):
    val = input(f"{field}{f' [{default}]' if default is not None else ''}: ").strip()
    return cast(val) if val else default


def interactive_from_ini(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)

    tester = config["Tester"]
    inputs = config["TesterInputs"]

    expert_path = tester.get("Expert", "")
    expert_name = expert_path.split("\\")[-1].replace(".ex5", "")

    json_config = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "report_types": prompt("Report types (comma-separated)", "csv,html").split(
                ","
            ),
        },
        "expert": {"path": expert_path, "name": expert_name},
        "symbols": [prompt("Symbol", tester.get("Symbol", "EURUSD"))],
        "date": {
            "start": prompt("Start date (YYYY-MM-DD)", "2024-01-01"),
            "end": prompt("End date (YYYY-MM-DD)", "2025-01-01"),
        },
        "forward": {
            "mode": prompt("Forward mode (NO, 1/4, 1/2, 1/3, or custom)", "NO")
        },
        "delays": int(prompt("Delays in ms", "0")),
        "modelling": prompt("Modelling method", "Every tick"),
        "deposit": {
            "amount": float(prompt("Deposit amount", tester.get("Deposit", "10000"))),
            "currency": prompt("Currency", tester.get("Currency", "USD")),
            "leverage": prompt("Leverage", f"1:{tester.get('Leverage', '100')}"),
        },
        "optimization": {
            "mode": prompt(
                "Optimization mode",
                {"0": "disabled", "1": "slow", "2": "fast", "3": "marketwatch"}.get(
                    tester.get("Optimization", "0"), "disabled"
                ),
            ),
            "result_priority": prompt(
                "Result priority",
                {
                    "0": "balance max",
                    "1": "profit factor max",
                    "2": "expected payoff max",
                    "3": "drawdown min",
                    "4": "recovery factor max",
                    "5": "sharpe ratio max",
                    "6": "custom max",
                    "7": "complex criterion max",
                }.get(tester.get("OptimizationCriterion", "0"), "balance max"),
            ),
        },
        "custom_criteria": {
            "profit_to_drawdown_ratio": float(
                prompt("Profit to drawdown ratio threshold", "3.0")
            )
        },
        "strategy_input_parameters": parse_tester_inputs(inputs),
    }

    config_dir = Path("optibach/config")
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"
    with config_path.open("w") as f:
        json.dump(json_config, f, indent=2)

    print(f"\n✅ Config saved to {config_path.resolve()}")


if __name__ == "__main__":
    path = input("Enter path to MT5 .ini file: ").strip()
    interactive_from_ini(path)
