# File: core/jobs/generator.py

from datetime import datetime
from pathlib import Path
import json
from tkinter import messagebox

from core.jobs_utils.validator import validate_config
from core.jobs_utils.runner import auto_resume_job
from core.jobs_utils.settings import load_settings

from helpers.enums import (
    optimization_mode_map,
    result_priority_map,
    forward_mode_map,
)
from helpers.path_utils import get_next_job_path
from ui.date_picker import assemble_ini_date
from state.app_state import AppState


def run_optimization(state: AppState):
    """Trigger an optimization run from the GUI state."""

    # ✅ 1. Validate GUI state first
    errors = validate_config(state)
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return

    # ✅ 2. Extract form data from the UI
    expert_path = state.expert_path_var.get()
    expert_name = Path(expert_path).stem
    symbols = state.symbol_var.get().split(",")
    label = f"{expert_name} - {symbols[0]}"

    # ✅ 3. Build the job config dict (what we’ll save as .json)
    config = {
        "label": label,
        "metadata": {
            "created_at": datetime.now().isoformat(),
        },
        "expert": {
            "path": expert_path,
            "name": expert_name,
        },
        "symbols": symbols,
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
            "mode": optimization_mode_map[state.optimization_mode_var.get()],
            "result_priority": result_priority_map[state.result_priority_var.get()],
        },
        "strategy_input_parameters": {},  # Populated elsewhere
    }

    # ✅ Add optional forward date
    if state.forward_mode_var.get() == "Custom (date specified)":
        config["forward"]["date"] = assemble_ini_date(state.forwarddate_var)

    # ✅ 4. Create a new job folder like jobs/job_20250408_003
    job_dir = get_next_job_path()
    job_dir.mkdir(parents=True, exist_ok=True)

    # ✅ 5. Save job.json inside that folder (not outside it!)
    job_json_path = job_dir / f"{job_dir.name}.json"
    with job_json_path.open("w", encoding="utf-16") as f:
        json.dump(config, f, indent=2)

    # ✅ 6. Load MT5 terminal path
    settings = load_settings()
    terminal_path = Path(settings.get("terminal_path", ""))
    if not terminal_path.exists():
        messagebox.showerror("Error", "Terminal path not found.")
        return

    # ✅ 7. Fire off the rest of the workflow
    # This function:
    # - Parses the .json file
    # - Generates INI files inside this same folder
    # - Runs MT5
    # - Monitors logs
    # - Triggers report export
    auto_resume_job(job_json_path, terminal_path)
