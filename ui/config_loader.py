# ui/startup_loader.py

import tkinter as tk
from pathlib import Path

from core.input_parser import parse_ini_inputs
from core.loader import load_ini_file
from ui.updaters import populate_ui_from_ini_data


def show_timed_toast(root: tk.Tk, message: str, duration_ms: int = 3000) -> None:
    """Display a temporary toast message at the bottom of the app window."""
    toast = tk.Label(root, text=message, bg="#333", fg="white", padx=10, pady=5)
    toast.place(relx=0.5, rely=1.0, anchor="s")

    root.after(duration_ms, toast.destroy)


from core.session import get_cached_ini_file, load_full_config


def load_cached_ui_state(
    parsed_inputs: list,
    context: dict,
    root=None,
    on_inputs_loaded: callable = None,
) -> None:
    ini_path = get_cached_ini_file()
    if not ini_path.exists():
        return

    try:
        updated_context = load_full_config(parsed_inputs, ini_path)

        # Push updates into existing StringVar context
        for k, v in updated_context.items():
            if k in context and hasattr(context[k], "set"):
                context[k].set(v)

        if context.get("update_dates"):
            context["update_dates"](
                updated_context["from_date"], updated_context["to_date"]
            )

        if on_inputs_loaded:
            on_inputs_loaded()

        populate_ui_from_ini_data(load_ini_file(ini_path), context)

        if root:
            show_timed_toast(root, "✅ Loaded cached config.")

    except Exception as e:
        if root:
            show_timed_toast(root, f"⚠️ Failed to load cached config: {e}")
