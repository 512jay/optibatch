# main_app.py

from core.enums import get_enum_label
from core.session import cache_ini_file, has_cached_ini, get_cached_ini_file
from ini_utils.loader import parse_ini_file
from core.input_parser import InputParam
from core.input_parser import parse_ini_inputs
from tkinter import filedialog, messagebox
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from ui.widgets.strategy_config import build_strategy_config
from ui.widgets.date_fields import build_date_fields
from ui.widgets.header_fields import build_header_fields
from ui.widgets.ea_inputs import build_inputs_section
from ui.actions.ini_buttons import build_ini_buttons
from ui.mt5_menu import build_mt5_menu
from ui.ini_loader import load_ini_and_update_ui
from ui.updaters import populate_ui_from_ini_data
from ui.edit_inputs_popup import open_edit_inputs_popup
from ui.startup_loader import load_cached_config_if_available
from ui.widgets.optimized_preview import (
    create_optimized_preview_widget,
    update_optimized_preview,
)

root = tk.Tk()
root.title("Optibatch")

menubar = tk.Menu(root)
build_mt5_menu(menubar, root)
root.config(menu=menubar)

# Layout sections
header_frame = ttk.LabelFrame(root, text="Header")
header_frame.pack(fill="x", padx=10, pady=(10, 5))
strategy_frame = ttk.LabelFrame(root, text="Strategy")
strategy_frame.pack(fill="x", padx=10, pady=5)
date_frame = ttk.LabelFrame(root, text="Date Range")
date_frame.pack(fill="x", padx=10, pady=5)
inputs_frame = ttk.LabelFrame(root, text="Inputs to Optimize")
inputs_frame.pack(fill="x", padx=10, pady=5)
buttons_frame = ttk.Frame(root)
buttons_frame.pack(side="left", fill="y", padx=(10, 5), pady=5)

# Header fields
header_vars = build_header_fields(header_frame)
expert_path_var = header_vars["expert_var"]
symbol_var = header_vars["symbol_var"]
deposit_var = header_vars["deposit_var"]
currency_var = header_vars["currency_var"]
leverage_var = header_vars["leverage_var"]

report_click_set = tk.StringVar(value="Not Set")
parsed_strategy_inputs: list[InputParam] = []

# Optimized preview widget
optimized_preview = create_optimized_preview_widget(inputs_frame)
optimized_preview.frame.pack(fill="x", padx=10, pady=(5, 0))

# Strategy settings
strategy_vars = build_strategy_config(strategy_frame)
strategy_model_var = strategy_vars["strategy_model_var"]
optimization_mode_var = strategy_vars["optimization_mode_var"]
result_priority_var = strategy_vars["result_priority_var"]
forward_mode_var = strategy_vars["forward_mode_var"]

# Date fields
fromdate_var = build_date_fields(date_frame, 0, "From Date")
todate_var = build_date_fields(date_frame, 1, "To Date")


def _split_date(date_str: str) -> dict[str, str]:
    try:
        y, m, d = date_str.split(".")
        return {"year": y, "month": m, "day": d}
    except Exception:
        return {"year": "", "month": "", "day": ""}


def update_stringvars(target: dict[str, tk.StringVar], values: dict[str, str]) -> None:
    for k, v in values.items():
        target[k].set(v)


def update_dates(f: str, t: str) -> None:
    update_stringvars(fromdate_var, _split_date(f))
    update_stringvars(todate_var, _split_date(t))


def update_optimized_inputs_preview():
    update_optimized_preview(optimized_preview, parsed_strategy_inputs)


def on_edit_inputs():
    popup = open_edit_inputs_popup(parsed_strategy_inputs)
    popup.wait_window()  # ✅ Waits for Save or window close
    update_optimized_inputs_preview()  # ✅ Now safely refreshes after edit


def on_load_ini():
    def after_load(data):
        populate_ui_from_ini_data(
            data,
            context={
                "expert": expert_path_var,
                "symbol": symbol_var,
                "deposit": deposit_var,
                "currency": currency_var,
                "leverage": leverage_var,
                "modeling": strategy_model_var,
                "optimization": optimization_mode_var,
                "result": result_priority_var,
                "forward": forward_mode_var,
                "update_dates": update_dates,
            },
        )
        update_optimized_inputs_preview()

    load_ini_and_update_ui(
        root,
        parsed_strategy_inputs,
        update_fields_callback=after_load,
        post_input_callback=update_optimized_inputs_preview,
    )


# UI buttons
build_inputs_section(inputs_frame, on_edit=on_edit_inputs)

build_ini_buttons(
    buttons_frame,
    [
        ("📂 Load INI", on_load_ini, "e", 0),
        ("✏️ Edit Inputs", on_edit_inputs, "i", 2),
        ("📊 Pick Symbols", lambda: print("Pick Symbols"), "s", 2),
    ],
)

# Load saved .ini if available
load_cached_config_if_available(
    parsed_strategy_inputs,
    context={
        "expert": expert_path_var,
        "symbol": symbol_var,
        "deposit": deposit_var,
        "currency": currency_var,
        "leverage": leverage_var,
        "modeling": strategy_model_var,
        "optimization": optimization_mode_var,
        "result": result_priority_var,
        "forward": forward_mode_var,
        "update_dates": update_dates,
    },
    root=root,
    on_inputs_loaded=update_optimized_inputs_preview,
)

root.mainloop()
