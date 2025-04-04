import json
from datetime import datetime
from pathlib import Path


def interactive_config_generator():
    config = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "report_types": input("Report types (comma-separated, e.g., csv,html): ")
            .strip()
            .split(","),
        },
        "expert": {
            "path": input(
                "Expert path (e.g., Shared Projects\\IndyTSL\\IndyTSL.ex5): "
            ).strip()
        },
        "symbols": input("Symbols (comma-separated, e.g., EURUSD,GBPUSD): ")
        .strip()
        .split(","),
        "date": {
            "start": input("Start date (YYYY-MM-DD): ").strip(),
            "end": input("End date (YYYY-MM-DD): ").strip(),
        },
        "forward": {
            "mode": input("Forward mode (NO, 1/4, 1/2, 1/3, or custom): ").strip()
        },
        "delays": int(input("Delays in ms (0–1000): ").strip()),
        "modelling": input(
            "Modelling method (Every tick, Every tick based on real ticks, 1 minute OHLC, Open prices only, Math calculations): "
        ).strip(),
        "deposit": {
            "amount": float(input("Deposit amount (e.g., 10000): ").strip()),
            "currency": input("Currency (e.g., USD): ").strip(),
            "leverage": input("Leverage (e.g., 1:100): ").strip(),
        },
        "optimization": {
            "mode": input(
                "Optimization mode (disabled, slow, fast, marketwatch): "
            ).strip(),
            "result_priority": input(
                "Result priority (balance max, drawdown min, sharpe ratio max, etc.): "
            ).strip(),
        },
        "custom_criteria": {
            "profit_to_drawdown_ratio": float(
                input("Profit to drawdown ratio threshold (e.g., 3.0): ").strip()
            )
        },
        "strategy_input_parameters": {},
    }

    # Derive expert name from path
    if "\\" in config["expert"]["path"]:
        config["expert"]["name"] = (
            config["expert"]["path"].split("\\")[-1].replace(".ex5", "")
        )
    else:
        config["expert"]["name"] = config["expert"]["path"].replace(".ex5", "")

    print("\n🧠 Enter strategy input parameters (press Enter to stop):")
    while True:
        param = input("\nParameter name: ").strip()
        if not param:
            break
        p_type = input("  Type (bool, enum, int, float): ").strip()
        default = input("  Default value: ").strip()
        optimize = input("  Optimize? (y/n): ").strip().lower() == "y"

        entry = {"type": p_type, "default": eval(default), "optimize": optimize}

        if p_type in ["int", "float", "enum"] and optimize:
            entry["start"] = eval(input("  Start: ").strip())
            entry["step"] = eval(input("  Step: ").strip())
            entry["end"] = eval(input("  End: ").strip())

        config["strategy_input_parameters"][param] = entry

    # Save to config
    config_dir = Path("optibach/config")
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"
    with config_path.open("w") as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Config saved to {config_path.resolve()}")


if __name__ == "__main__":
    interactive_config_generator()
