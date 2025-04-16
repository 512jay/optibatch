# main_app.py (Refactored for clarity and mypy compatibility)
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from core.main_runner import run_optimizations
from core.state import registry
from core.session import save_full_config
from core.input_parser import InputParam

from ui.mt5_menu import build_mt5_menu, update_window_title
from ui.symbol_picker import open_symbol_picker
from ui.ini_loader import load_ini_and_update_ui
from ui.config_loader import load_cached_ui_state
from ui.edit_inputs_popup import open_edit_inputs_popup
from ui.widgets.button_row import build_button_row
from ui.widgets.date_fields import build_date_fields
from ui.widgets.ea_inputs import build_inputs_section
from ui.widgets.header_fields import build_header_fields
from ui.widgets.optimized_preview import (
    create_optimized_preview_widget,
    update_optimized_preview,
    autosize_columns,
)
from ui.widgets.strategy_config import build_strategy_config
from ui.widgets.options_menu import build_options_menu
from ui.database_menu import build_database_menu
from ui.updaters import populate_ui_from_ini_data

# UI setup
root = tk.Tk()
root.title("Optibatch")
toast_label = None



def show_toast(message: str, duration: int = 2000) -> None:
    global toast_label
    if toast_label:
        toast_label.destroy()

    frame = tk.Frame(root, bg="#333", bd=1)
    toast_label = tk.Label(
        frame,
        text=message,
        bg="#333",
        fg="white",
        font=("Segoe UI", 9),
        padx=10,
        pady=5,
    )
    toast_label.pack()
    frame.place(relx=0.5, rely=1.0, anchor="s", y=-10)
    root.after(duration, lambda: frame.destroy())


def on_continue_previous() -> None:
    job_path = filedialog.askdirectory(
        title="Select Previous Job Folder", initialdir="generated"
    )
    if job_path:
        config_path = Path(job_path) / "job_config.json"
        if config_path.exists():
            run_optimizations(config_path, run_folder=Path(job_path))
        else:
            messagebox.showerror(
                "Missing File", f"No job_config.json found in {job_path}"
            )


# Logic Functions
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


def update_optimized_inputs_preview() -> None:
    update_optimized_preview(optimized_preview, parsed_strategy_inputs)
    optimized_preview.tree.after(0, lambda: autosize_columns(optimized_preview.tree))


def on_edit_inputs() -> None:
    popup = open_edit_inputs_popup(parsed_strategy_inputs)
    popup.wait_window()
    update_optimized_inputs_preview()


def on_load_ini() -> None:
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


def on_run_optimizations() -> None:
    try:
        # ✅ Persist current live UI state
        on_save_inputs()

        # ✅ Now run from the saved config
        run_optimizations(Path(".cache/current_config.json"))
    except Exception as e:
        print(f"Run failed: {e}")
        import traceback

        traceback.print_exc()


def update_symbol_field(new_symbol: str) -> None:
    symbol_var.set(new_symbol)


def on_first_load_and_resize() -> None:
    update_optimized_inputs_preview()
    optimized_preview.tree.after(0, lambda: autosize_columns(optimized_preview.tree))



update_window_title(root)
menubar = tk.Menu(root)

# Options
options_menu, use_discrete_months_var = build_options_menu(menubar)
menubar.add_cascade(label="Options", menu=options_menu)


# Actions Menu (matches button_row functionality)
actions_menu = tk.Menu(menubar, tearoff=0)
actions_menu.add_command(label="📂 Load INI", command=on_load_ini)
actions_menu.add_command(label="✏️ Edit Inputs", command=on_edit_inputs)
actions_menu.add_command(label="⏭️ Continue Previous", command=on_continue_previous)
actions_menu.add_command(label="🚀 Run Optimizations", command=on_run_optimizations)
menubar.add_cascade(label="Actions", menu=actions_menu)


# MT5
build_mt5_menu(menubar, root)

root.config(menu=menubar)


# Build UI sections
header_frame = ttk.LabelFrame(root, text="Header")
strategy_frame = ttk.LabelFrame(root, text="Strategy")
date_frame = ttk.LabelFrame(root, text="Date Range")
inputs_frame = ttk.LabelFrame(root, text="Inputs to Optimize")
for frame in [header_frame, strategy_frame, date_frame, inputs_frame]:
    frame.pack(fill="x", padx=10, pady=5)

parsed_strategy_inputs: list[InputParam] = []
header_vars = build_header_fields(header_frame)
strategy_vars = build_strategy_config(strategy_frame)
fromdate_var = build_date_fields(date_frame, 0, "From Date")
todate_var = build_date_fields(date_frame, 1, "To Date")

expert_path_var = header_vars["expert_var"]
symbol_var = header_vars["symbol_var"]
deposit_var = header_vars["deposit_var"]
currency_var = header_vars["currency_var"]
leverage_var = header_vars["leverage_var"]
timeframe_var = strategy_vars["timeframe_var"]
strategy_model_var = strategy_vars["strategy_model_var"]
optimization_mode_var = strategy_vars["optimization_mode_var"]
result_priority_var = strategy_vars["result_priority_var"]
forward_mode_var = strategy_vars["forward_mode_var"]


# Widget Construction (after callbacks defined)
optimized_preview = create_optimized_preview_widget(
    parent=inputs_frame,
    on_save_click=on_save_inputs,
)
optimized_preview.frame.pack(fill="x", padx=10, pady=(5, 0))

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

build_inputs_section(inputs_frame, on_edit=on_edit_inputs)

bottom_frame = ttk.Frame(root)
bottom_frame.pack(fill="x", padx=10, pady=10)

buttons_frame = build_button_row(
    parent=bottom_frame,
    root=root,
    parsed_inputs=parsed_strategy_inputs,
    get_symbol_cb=lambda: symbol_var.get(),
    set_symbol_cb=lambda value: symbol_var.set(value),
    on_edit_inputs=on_edit_inputs,
    on_load_ini=on_load_ini,
    on_run_optimizations=on_run_optimizations,
)

buttons_frame.pack(fill="x", padx=10, pady=10)


def on_app_exit() -> None:
    registry.save()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_app_exit)
root.mainloop()
