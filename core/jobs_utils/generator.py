# File: core/jobs/generator.py
from datetime import datetime
from pathlib import Path
import json
from tkinter import messagebox

from core.jobs_utils.validator import validate_config
from core.jobs_utils.runner import auto_resume_job
from core.jobs_utils.settings import load_settings

from helpers.enums import (
    optimization_options,
    result_priority_options,
    forward_mode_map,
)
from helpers.path_utils import get_next_job_path

from ui.date_picker import assemble_ini_date
from state.app_state import AppState


def run_optimization(state: AppState):
    errors = validate_config(state)
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return

    expert_name = Path(state.expert_path_var.get()).stem
    label = f"{expert_name} - {state.symbol_var.get().split(',')[0]}"

    config = {
        "label": label,
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "report_types": state.report_var.get().split(","),
        },
        "expert": {
            "path": state.expert_path_var.get(),
            "name": expert_name,
        },
        "symbols": state.symbol_var.get().split(","),
        "date": {
            "start": assemble_ini_date(state.fromdate_var),
            "end": assemble_ini_date(state.todate_var),
        },
        "forward": {
            "mode": forward_mode_map[state.forward_mode_var.get()],
        },
        "modelling": "Every tick",
        "deposit": {
            "amount": float(state.deposit_var.get()),
            "currency": state.currency_var.get(),
            "leverage": f"1:{state.leverage_var.get()}",
        },
        "optimization": {
            "mode": optimization_options[state.optimization_mode_var.get()],
            "result_priority": result_priority_options[state.result_priority_var.get()],
        },
        "strategy_input_parameters": {},  # Filled externally
    }

    if state.forward_mode_var.get() == "Custom (date specified)":
        config["forward"]["date"] = assemble_ini_date(state.forwarddate_var)

    job_path = get_next_job_path()
    with job_path.open("w") as f:
        json.dump(config, f, indent=2)

    # 🧠 Load terminal path from settings
    settings = load_settings()
    terminal_path = Path(settings.get("terminal_path", ""))
    if not terminal_path.exists():
        messagebox.showerror("Error", "Terminal path not found.")
        return

    auto_resume_job(job_path, terminal_path)
