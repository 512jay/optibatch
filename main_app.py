# main_app.py

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from core.enums import get_enum_label, enum_label_map, get_value_for_label
from core.input_parser import InputParam, parse_ini_inputs
from core.session import (
    cache_ini_file,
    get_cached_ini_file,
    has_cached_ini,
    save_full_config,
    update_json_tester_inputs,
)
from ini_utils.loader import parse_ini_file
from core.session import update_ini_tester_inputs
from core.state import registry
from ui.config_loader import load_cached_ui_state
from ui.edit_inputs_popup import open_edit_inputs_popup
from ui.ini_loader import load_ini_and_update_ui
from ui.mt5_menu import build_mt5_menu, update_window_title
from ui.symbol_picker import open_symbol_picker
from ui.updaters import populate_ui_from_ini_data
from ui.widgets.date_fields import build_date_fields
from ui.widgets.ea_inputs import build_inputs_section
from ui.widgets.header_fields import build_header_fields
from ui.widgets.optimized_preview import (
    create_optimized_preview_widget,
    update_optimized_preview,
)
from ui.widgets.strategy_config import build_strategy_config
from ui.widgets.options_menu import build_options_menu
from core.main_runner import run_optimizations


def on_run_optimizations_click():
    config_path = Path(".cache/current_config.json")
    run_optimizations(config_path)


def on_pick_symbol_clicked() -> None:
    current = symbol_var.get()
    open_symbol_picker(root, update_symbol_field, preselected=current)


def update_symbol_field(new_symbol: str) -> None:
    symbol_var.set(new_symbol)


def on_save_inputs() -> None:
    try:
        save_full_config(
            parsed_strategy_inputs,
            {
                "symbol": symbol_var.get(),
                "timeframe": timeframe_var.get(),
                "deposit": deposit_var.get(),
                "currency": currency_var.get(),
                "leverage": leverage_var.get(),
                "model": strategy_model_var.get(),
                "optimization": optimization_mode_var.get(),
                "result": result_priority_var.get(),
                "forward": forward_mode_var.get(),
                "from_date": f'{fromdate_var["year"].get()}.{fromdate_var["month"].get()}.{fromdate_var["day"].get()}',
                "to_date": f'{todate_var["year"].get()}.{todate_var["month"].get()}.{todate_var["day"].get()}',
            },
        )
        show_toast("Settings saved!")
    except Exception as e:
        messagebox.showerror("Error saving settings", str(e))


root = tk.Tk()
root.title("Optibatch")
toast_label = None
update_window_title(root)

def show_toast(message: str, duration: int = 2000) -> None:
    global toast_label

    if toast_label is not None:
        toast_label.destroy()

    toast_label_frame = tk.Frame(root, bg="#333", bd=1)
    toast_label = tk.Label(
        toast_label_frame,
        text=message,
        bg="#333",
        fg="white",
        font=("Segoe UI", 9),
        padx=10,
        pady=5,
    )
    toast_label.pack()
    toast_label_frame.place(relx=0.5, rely=1.0, anchor="s", y=-10)

    root.after(duration, lambda: toast_label_frame.destroy())


# Create the top menu bar
menubar = tk.Menu(root)
options_menu, use_discrete_months_var = build_options_menu(menubar)
menubar.add_cascade(label="Options", menu=options_menu)
root.config(menu=menubar)
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
buttons_frame.pack(fill="x", padx=10, pady=10)

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
ttk.Button(inputs_frame, text="💾 Save Settings", command=on_save_inputs).pack(
    pady=(5, 0)
)


# Strategy settings
strategy_vars = build_strategy_config(strategy_frame)
timeframe_var = strategy_vars["timeframe_var"]
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
                "timeframe": timeframe_var,
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


def on_run_optimizations():
    try:
        run_optimizations(Path(".cache/current_config.json"))
    except Exception as e:
        print(f"Run failed: {e}")
        import traceback

        traceback.print_exc()


# UI buttons
build_inputs_section(inputs_frame, on_edit=on_edit_inputs)


# Layout: horizontally packed buttons
ttk.Button(buttons_frame, text="📂 Load INI", command=on_load_ini).pack(
    side="left", padx=5
)
ttk.Button(buttons_frame, text="✏️ Edit Inputs", command=on_edit_inputs).pack(
    side="left", padx=5
)
ttk.Button(buttons_frame, text="📊 Pick Symbols", command=on_pick_symbol_clicked).pack(
    side="left", padx=5
)
ttk.Button(
    buttons_frame,
    text="⏭️ Continue Previous",
    command=lambda: print("Continue Previous"),
).pack(side="left", padx=10)
ttk.Button(
    buttons_frame,
    text="🚀 Run Optimizations",
    command=on_run_optimizations,
).pack(side="left", padx=5)


# Load saved .ini if available
load_cached_ui_state(
    parsed_strategy_inputs,
    context={
        "expert": expert_path_var,
        "symbol": symbol_var,
        "deposit": deposit_var,
        "currency": currency_var,
        "leverage": leverage_var,
        "timeframe": timeframe_var,
        "modeling": strategy_model_var,
        "optimization": optimization_mode_var,
        "result": result_priority_var,
        "forward": forward_mode_var,
        "update_dates": update_dates,
    },
    root=root,
    on_inputs_loaded=update_optimized_inputs_preview,
)

def on_app_exit():
    registry.save()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_app_exit)

root.mainloop()
