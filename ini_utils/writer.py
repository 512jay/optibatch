# ini_utils/writer.py

from core.input_parser import InputParam
from pathlib import Path


def update_ini_tester_inputs(path: Path, inputs: list[InputParam]) -> None:
    if not path.exists():
        return

    lines = path.read_text(encoding="utf-16").splitlines()
    output = []
    in_section = False

    for line in lines:
        stripped = line.strip()
        if stripped == "[TesterInputs]":
            output.append(line)
            in_section = True
            for param in inputs:
                parts = [
                    param.default,
                    param.start or "",
                    param.step or "",
                    param.end or "",
                    "Y" if param.optimize else "N",
                ]
                output.append(f"{param.name} = {'||'.join(parts)}")
        elif in_section and stripped.startswith("[") and stripped.endswith("]"):
            in_section = False
            output.append(line)
        elif not in_section:
            output.append(line)

    path.write_text("\n".join(output), encoding="utf-16", newline="\r\n")


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
