# ui/startup_loader.py

from pathlib import Path
from core.loader import load_ini_file
from core.input_parser import parse_ini_inputs
from ui.updaters import populate_ui_from_ini_data
import tkinter as tk


def show_timed_toast(root: tk.Tk, message: str, duration_ms: int = 3000) -> None:
    """Display a temporary toast message at the bottom of the app window."""
    toast = tk.Label(root, text=message, bg="#333", fg="white", padx=10, pady=5)
    toast.place(relx=0.5, rely=1.0, anchor="s")

    root.after(duration_ms, toast.destroy)


def load_cached_config_if_available(
    parsed_inputs: list,
    context: dict,
    root=None,
    on_inputs_loaded: callable = None,
) -> None:

    """Load .cache/current_config.ini if it exists and update the UI."""
    cached_path = Path(".cache/current_config.ini")
    if not cached_path.exists():
        return

    try:
        ini_data = load_ini_file(cached_path)
        parsed_inputs.clear()
        parsed_inputs.extend(parse_ini_inputs(ini_data["inputs"]))

        if on_inputs_loaded:
            on_inputs_loaded()

        populate_ui_from_ini_data(ini_data, context)

        if root is not None:
            show_timed_toast(root, "✅ Loaded cached config.")

    except Exception as e:
        if root is not None:
            show_timed_toast(root, f"⚠️ Failed to load cached config: {e}")
