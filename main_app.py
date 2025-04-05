# File: main_app.py
# Purpose: Main Optibach GUI — delegates layout to this script, logic/enums split into helpers.

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pathlib import Path
from typing import Any

# GUI components
from ui.symbol_picker import open_symbol_picker
from ui.input_editor import open_input_editor
from ui.date_picker import create_ini_date_picker

# Core logic
from core.jobs.generator import run_optimization
from core.jobs.runner import pick_and_resume_job
from core.jobs.settings import load_settings
from ini_utils.loader import parse_ini_file, parse_tester_inputs_section
from helpers.enums import (
    optimization_options,
    result_priority_options,
    forward_mode_map,
)
from state.app_state import AppState

# Init App and State
root = tk.Tk()
root.title("Optibach Main Interface")
state = AppState()

# Layout setup
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

fields = [
    ("Expert Path", state.expert_path_var),
    ("Symbols (comma-separated)", state.symbol_var),
    ("Deposit", state.deposit_var),
    ("Currency", state.currency_var),
    ("Leverage", state.leverage_var),
    ("Report Types (csv,html)", state.report_var),
]

for i, (label_text, var) in enumerate(fields):
    tk.Label(frame, text=label_text).grid(row=i, column=0, sticky="e")
    tk.Entry(frame, textvariable=var, width=40).grid(row=i, column=1, sticky="w")

opt_row = len(fields)

# Optimization Mode dropdown
tk.Label(frame, text="Optimization Mode").grid(row=opt_row, column=0, sticky="e")
ttk.Combobox(
    frame,
    textvariable=state.optimization_mode_var,
    values=list(optimization_options.keys()),
    width=35,
).grid(row=opt_row, column=1, sticky="w")

# Result Priority dropdown
tk.Label(frame, text="Result Priority").grid(row=opt_row + 1, column=0, sticky="e")
ttk.Combobox(
    frame,
    textvariable=state.result_priority_var,
    values=list(result_priority_options.keys()),
    width=35,
).grid(row=opt_row + 1, column=1, sticky="w")

# Date pickers
from_frame, state.fromdate_var = create_ini_date_picker(frame, "FromDate")
to_frame, state.todate_var = create_ini_date_picker(frame, "ToDate")
from_frame.grid(row=opt_row + 2, column=0, columnspan=2, pady=5)
to_frame.grid(row=opt_row + 3, column=0, columnspan=2, pady=5)

# Forward Mode
tk.Label(frame, text="Forward Mode").grid(row=opt_row + 4, column=0, sticky="e")
ttkw = ttk.Combobox(
    frame,
    textvariable=state.forward_mode_var,
    values=list(forward_mode_map.keys()),
    width=25,
)
ttkw.grid(row=opt_row + 4, column=1, sticky="w")

# Forward Date (conditionally visible)
forwarddate_frame, state.forwarddate_var = create_ini_date_picker(frame, "ForwardDate")
forwarddate_frame.grid(row=opt_row + 5, column=0, columnspan=2, pady=5)


def toggle_forward_date(*_):
    selected = state.forward_mode_var.get()
    (
        forwarddate_frame.grid()
        if "custom" in selected.lower()
        else forwarddate_frame.grid_remove()
    )


state.forward_mode_var.trace_add("write", toggle_forward_date)
toggle_forward_date()


# --- Load INI handler ---
def load_ini_ui():
    file_path = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini")])
    if not file_path:
        return

    data = parse_ini_file(file_path)
    state.parsed_strategy_inputs = parse_tester_inputs_section(data["inputs"])

    state.expert_path_var.set(data.get("Expert", ""))
    state.symbol_var.set(data.get("Symbol", ""))
    state.leverage_var.set(data.get("Leverage", ""))
    state.currency_var.set(data.get("Currency", ""))
    state.deposit_var.set(data.get("Deposit", ""))
    state.optimization_mode_var.set("Slow (complete algorithm)")
    state.result_priority_var.set("Balance Max")
    state.forward_mode_var.set(
        "Custom (date specified)" if "ForwardDate" in data else "NO"
    )

    for key, var in zip(
        ["FromDate", "ToDate", "ForwardDate"],
        [state.fromdate_var, state.todate_var, state.forwarddate_var],
    ):
        if key in data:
            y, m, d = map(int, data[key].split("."))
            var["year"].set(str(y))
            var["month"].set(str(m))
            var["day"].set(str(d))

    state.status_var.set(f"Loaded: {Path(file_path).name}")


# --- Buttons ---
btn_row = opt_row + 6

tk.Button(frame, text="📂 Load INI", command=load_ini_ui, width=42).grid(
    row=btn_row, column=0, columnspan=2, pady=(10, 5)
)
tk.Button(frame, text="📈 Pick Symbols", command=open_symbol_picker, width=20).grid(
    row=btn_row + 1, column=0, pady=(0, 5), sticky="e"
)
tk.Button(frame, text="🔧 Edit Inputs", command=open_input_editor, width=20).grid(
    row=btn_row + 1, column=1, pady=(0, 5), sticky="w"
)
tk.Button(
    frame, text="🔁 Resume Previous Job", command=pick_and_resume_job, width=20
).grid(row=btn_row + 2, column=0, pady=(0, 10), sticky="e")
tk.Button(
    frame, text="▶️ Run Optimizations", command=lambda: run_optimization(state), width=20
).grid(row=btn_row + 2, column=1, pady=(0, 10), sticky="w")

# Status bar
tk.Label(root, textvariable=state.status_var, anchor="w").pack(fill="x", side="bottom")

# Run the application
root.mainloop()
