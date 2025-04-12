# ui/widgets/button_row.py

import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
from core.main_runner import run_optimizations
from ui.symbol_picker import open_symbol_picker


def build_button_row(
    parent: tk.Widget,
    root: tk.Tk,
    parsed_inputs: list,
    update_symbol_field_cb,
    on_edit_inputs,
    on_load_ini,
    on_run_optimizations,
) -> tk.Frame:
    """
    Creates the bottom row of action buttons for the main UI.
    Delegates most logic to callbacks provided by main_app.py.
    """
    frame = ttk.Frame(parent)

    def on_pick_symbols():
        current = update_symbol_field_cb()
        open_symbol_picker(root, update_symbol_field_cb, preselected=current)

    def on_continue_previous():
        job_path = filedialog.askdirectory(
            title="Select Previous Job Folder", initialdir="generated"
        )
        if job_path:
            config_path = Path(job_path) / "job_config.json"
            if config_path.exists():
                run_optimizations(config_path, run_folder=Path(job_path))
            else:
                print(f"No job_config.json found in {job_path}")

    # Add buttons horizontally
    ttk.Button(frame, text="📂 Load INI", command=on_load_ini).pack(side="left", padx=5)
    ttk.Button(frame, text="✏️ Edit Inputs", command=on_edit_inputs).pack(
        side="left", padx=5
    )
    ttk.Button(frame, text="📊 Pick Symbols", command=on_pick_symbols).pack(
        side="left", padx=5
    )
    ttk.Button(frame, text="⏭️ Continue Previous", command=on_continue_previous).pack(
        side="left", padx=10
    )
    ttk.Button(frame, text="🚀 Run Optimizations", command=on_run_optimizations).pack(
        side="left", padx=5
    )

    return frame
