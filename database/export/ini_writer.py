# File: export/ini_writer.py
# Purpose: Export a clean MT5-compatible .ini file from a given run ID

import os
from pathlib import Path
from datetime import date
from sqlalchemy.orm import Session
from database.models import Run, Job
from database.session import get_engine, get_session


INI_HEADER_ORDER = [
    "Expert",
    "Symbol",
    "Period",
    "Optimization",
    "Model",
    "FromDate",
    "ToDate",
    "ForwardMode",
    "Deposit",
    "Currency",
    "ProfitInPips",
    "Leverage",
    "ExecutionMode",
    "OptimizationCriterion",
]


def write_ini_for_run(run_id: int, output_dir: Path) -> Path:
    """Given a run_id, write a complete MT5 .ini file to disk."""
    engine = get_engine()
    with get_session(engine) as session:
        run: Run = session.query(Run).filter_by(id=run_id).first()
        if not run:
            raise ValueError(f"Run {run_id} not found")

        job: Job = run.job
        ini_lines = []

        # [Tester] section
        ini_lines.append("[Tester]")
        header_values = {
            "Expert": job.expert_path,
            "Symbol": run.symbol,
            "Period": run.timeframe,
            "Optimization": "1",
            "Model": job.modeling_mode,
            "FromDate": run.start_date.strftime("%Y.%m.%d"),
            "ToDate": run.end_date.strftime("%Y.%m.%d"),
            "ForwardMode": "0",
            "Deposit": str(int(job.deposit)),
            "Currency": job.currency,
            "ProfitInPips": "0",
            "Leverage": job.leverage,
            "ExecutionMode": "0",
            "OptimizationCriterion": "0",
        }
        for key in INI_HEADER_ORDER:
            ini_lines.append(f"{key}={header_values[key]}")

        # [TesterInputs] section
        ini_lines.append("[TesterInputs]")
        for param_name, full_line in job.tester_inputs.items():
            override = run.params_json.get(param_name)

            if override is not None and str(override).lower() != "none":
                parts = full_line.split("||")
                parts[0] = str(override)
                full_line = "||".join(parts)

            ini_lines.append(f"{param_name}={full_line}")



        # Write to file (UTF-16 LE)
        filename = f"{job.expert_name}.{run.symbol}.{run.timeframe}.{run.start_date.strftime('%Y%m%d')}_{run.end_date.strftime('%Y%m%d')}.{run.pass_number:03}.ini"
        output_path = output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-16") as f:
            f.write("\n".join(ini_lines))

        return output_path
