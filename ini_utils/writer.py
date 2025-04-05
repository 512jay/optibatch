# File: utils/ini_writer.py

from pathlib import Path
from datetime import datetime


def format_ini(config: dict, symbol: str) -> str:
    tester = config.get("expert", {})
    optimization = config.get("optimization", {})
    forward = config.get("forward", {})
    deposit = config.get("deposit", {})

    lines = [
        "[Tester]",
        f"Expert={tester['path']}",
        f"Symbol={symbol}",
        "Period=H1",
        "Optimization=1",
        "Model=1",
        f"FromDate={config['date']['start'].replace('-', '.')}\nToDate={config['date']['end'].replace('-', '.')}",
    ]

    if forward.get("mode") is not None:
        lines.append(f"ForwardMode={forward['mode']}")
    if "date" in forward:
        lines.append(f"ForwardDate={forward['date']}")

    lines.extend(
        [
            f"Deposit={int(deposit.get('amount', 10000))}",
            f"Currency={deposit.get('currency', 'USD')}",
            "ProfitInPips=0",
            f"Leverage={deposit.get('leverage', '1:100').split(':')[-1]}",
            "ExecutionMode=0",
            f"OptimizationCriterion={optimization.get('result_priority', 0)}",
            "",
            "[TesterInputs]",
        ]
    )

    for k, v in config.get("strategy_input_parameters", {}).items():
        lines.append(f"{k}={v}")

    return "\n".join(lines)
