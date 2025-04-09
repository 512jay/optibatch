# File: main_app.py
# Purpose: Main entry point for Optibach GUI app.

import sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pathlib import Path
from typing import Any
import pyautogui
import subprocess
from core.config import config
from core.logging.logger import logger
from state.app_state import AppState
from ui.symbol_picker import open_symbol_picker
from ui.input_editor import open_input_editor
from ui.date_picker import create_ini_date_picker
from core.jobs_utils.generator import run_optimization
from core.jobs_utils.runner import pick_and_resume_job
from ini_utils.loader import parse_ini_file, parse_tester_inputs_section
from ui.mt5_scanner_ui import scan_and_select_mt5_install
from ui.mt5_menu import build_mt5_menu
from dotenv import load_dotenv
from helpers.enums import (
    optimization_mode_map,
    result_priority_map,
    forward_mode_map,
)

import json
from core.registry import get_last_used_install

load_dotenv()
SETTINGS_FILE = Path("settings.json")
selected_mt5_id = get_last_used_install()


def get_date_from_picker(picker_dict):
    return f"{picker_dict['year'].get()}.{picker_dict['month'].get()}.{picker_dict['day'].get()}"


report_click = config.get("report_click", {"x": 0, "y": 0})
def load_last_settings():
    if SETTINGS_FILE.exists():

        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load settings.json: {e}")
    return {}


def save_current_settings():
    # Load existing settings to avoid overwriting
    existing = config.get("last_settings") or {}

    # Extract values from UI state
    settings_to_save = {
        "expert_path": state.expert_path_var.get(),
        "symbols": state.symbol_var.get(),
        "from_date": get_date_from_picker(state.fromdate_var),
        "to_date": get_date_from_picker(state.todate_var),
        "forward_mode": state.forward_mode_var.get(),
        "forward_date": get_date_from_picker(state.forwarddate_var),
        "optimization_mode": state.optimization_mode_var.get(),
        "result_priority": state.result_priority_var.get(),
        "strategy_inputs": state.parsed_strategy_inputs,
    }

    # Merge existing with new settings
    updated = {**existing, **settings_to_save}
    config.set("last_settings", updated)


# --- GUI Setup ---
root = tk.Tk()
root.title("Optibatch Main Interface - [MT5 Install Name]")

# --- Top Menu Bar ---
menubar = tk.Menu(root)
build_mt5_menu(menubar, root, selected_mt5_id)
root.config(menu=menubar)


# --- Application State ---
state = AppState()
state.report_click_set = tk.StringVar(value="Not Set")
click = config.get("report_click")
if click and "x" in click and "y" in click:
    state.report_click_set.set(f"Loaded ({click['x']}, {click['y']})")

# --- Load Last Settings ---
last = load_last_settings()

# --- Set Simple Vars ---
state.expert_path_var.set(last.get("Expert", ""))
state.symbol_var.set(last.get("Symbol", ""))
state.deposit_var.set(last.get("Deposit", "10000"))
state.currency_var.set(last.get("Currency", "USD"))
state.leverage_var.set(last.get("Leverage", "100"))

state.optimization_mode_var.set(
    next(
        (
            k
            for k, v in optimization_mode_map.items()
            if str(v) == str(last.get("Optimization", 2))
        ),
        "Fast (genetic based algorithm)",
    )
)
state.result_priority_var.set(
    next(
        (
            k
            for k, v in result_priority_map.items()
            if str(v) == str(last.get("OptimizationCriterion", 0))
        ),
        "Balance Max",
    )
)
state.forward_mode_var.set(
    next(
        (
            k
            for k, v in forward_mode_map.items()
            if str(v) == str(last.get("ForwardMode", 0))
        ),
        "NO",
    )
)

# --- Create Date Pickers ---
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

from_frame, state.fromdate_var = create_ini_date_picker(frame, "FromDate")
to_frame, state.todate_var = create_ini_date_picker(frame, "ToDate")
forwarddate_frame, state.forwarddate_var = create_ini_date_picker(frame, "ForwardDate")


# --- Restore Dates ---
def populate_date(picker, date_str, required=True):
    parts = date_str.split(".")
    if len(parts) == 3:
        y, m, d = parts
        picker["year"].set(y)
        picker["month"].set(m.zfill(2))
        picker["day"].set(d.zfill(2))
    elif required:
        logger.warning(f"❗ Required date missing or invalid: '{date_str}'")
    else:
        logger.info(f"Skipping optional date: '{date_str}'")


populate_date(state.fromdate_var, last.get("FromDate", ""))
populate_date(state.todate_var, last.get("ToDate", ""))
populate_date(state.forwarddate_var, last.get("ForwardDate", ""), required=False)


# Streamlit dashboard function
def open_streamlit_dashboard():
    # 🗂️ Open folder picker dialog
    selected_folder = filedialog.askdirectory(title="Select folder of MT5 XML reports")
    if not selected_folder:
        return  # User cancelled

    dashboard_path = Path("visualize_mt5.py").resolve()

    # 🚀 Launch Streamlit with selected folder
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(dashboard_path),
            "--",
            "--folder",
            selected_folder,
        ],
        shell=True,
    )


# --- Set Report Click Point ---
def set_report_click_location():
    logger.info("Setting report click location...")
    countdown_window = tk.Toplevel()
    countdown_window.title("Set Click Location")

    screen_width = countdown_window.winfo_screenwidth()
    screen_height = countdown_window.winfo_screenheight()
    window_width = int(screen_width * 0.2)
    window_height = int(screen_height * 0.2)
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    countdown_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    countdown_window.configure(bg="#ffffff")
    countdown_window.resizable(False, False)

    countdown_window.grid_rowconfigure(0, weight=1)
    countdown_window.grid_rowconfigure(1, weight=2)
    countdown_window.grid_columnconfigure(0, weight=1)

    instruction_label = tk.Label(
        countdown_window,
        text="Move mouse to MT5 report area.\nCapture at zero.",
        font=("Segoe UI", 12),
        bg="#ffffff",
        fg="#111111",
        wraplength=window_width - 40,
        justify="center",
        padx=10,
        pady=10,
    )
    instruction_label.grid(row=0, column=0, sticky="n")

    countdown_font_size = int(window_height * 0.15)
    timer_label = tk.Label(
        countdown_window,
        text="10",
        font=("Segoe UI", countdown_font_size, "bold"),
        fg="#222222",
        bg="#ffffff",
    )
    timer_label.grid(row=1, column=0, sticky="s")

    def update_timer(seconds_left):
        if seconds_left <= 0:
            countdown_window.destroy()
            capture_click_position()
        else:
            timer_label.config(text=f"{seconds_left}")
            countdown_window.after(1000, update_timer, seconds_left - 1)

    def capture_click_position():
        x, y = pyautogui.position()
        config.set("report_click", {"x": x, "y": y})
        state.report_click_set.set(f"Set at ({x}, {y})")
        logger.success(f"Click captured at ({x}, {y})")
        messagebox.showinfo("Click Saved", f"Click location set at ({x}, {y})")

    update_timer(10)


# --- GUI LAYOUT ---
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

fields = [
    ("Expert Path", state.expert_path_var),
    ("Symbols (comma-separated)", state.symbol_var),
    ("Deposit", state.deposit_var),
    ("Currency", state.currency_var),
    ("Leverage", state.leverage_var),
]

for i, (label_text, var) in enumerate(fields):
    tk.Label(frame, text=label_text).grid(row=i, column=0, sticky="e")
    tk.Entry(frame, textvariable=var, width=40).grid(row=i, column=1, sticky="w")

opt_row = len(fields)

tk.Label(frame, text="Optimization Mode").grid(row=opt_row, column=0, sticky="e")
ttk.Combobox(
    frame,
    textvariable=state.optimization_mode_var,
    values=list(optimization_mode_map.keys()),
    width=35,
).grid(row=opt_row, column=1, sticky="w")

tk.Label(frame, text="Result Priority").grid(row=opt_row + 1, column=0, sticky="e")
ttk.Combobox(
    frame,
    textvariable=state.result_priority_var,
    values=list(result_priority_map.keys()),
    width=35,
).grid(row=opt_row + 1, column=1, sticky="w")

from_frame, state.fromdate_var = create_ini_date_picker(frame, "FromDate")
to_frame, state.todate_var = create_ini_date_picker(frame, "ToDate")
from_frame.grid(row=opt_row + 2, column=0, columnspan=2, pady=5)
to_frame.grid(row=opt_row + 3, column=0, columnspan=2, pady=5)

forward_row = opt_row + 4
tk.Label(frame, text="Forward Mode").grid(row=forward_row, column=0, sticky="e")
forward_dropdown = ttk.Combobox(
    frame,
    textvariable=state.forward_mode_var,
    values=list(forward_mode_map.keys()),
    width=20,
)
forward_dropdown.grid(row=forward_row, column=1, sticky="w")

forwarddate_frame, state.forwarddate_var = create_ini_date_picker(frame, "ForwardDate")
forwarddate_frame.grid(row=forward_row + 1, column=0, columnspan=2, pady=5)


def update_forward_visibility(*_):
    value = state.forward_mode_var.get().lower()
    if "custom" in value:
        forwarddate_frame.grid()
    else:
        forwarddate_frame.grid_remove()


forward_dropdown.bind("<<ComboboxSelected>>", update_forward_visibility)
update_forward_visibility()


# --- Load INI ---
def load_ini_ui(state: AppState) -> None:
    file_path = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini")])
    if not file_path:
        return
    data = parse_ini_file(file_path)
    state.expert_path_var.set(data.get("Expert", ""))
    state.symbol_var.set(data.get("Symbol", "EURUSD"))
    state.deposit_var.set(data.get("Deposit", "1000"))
    state.currency_var.set(data.get("Currency", "USD"))
    state.leverage_var.set(data.get("Leverage", "100"))
    state.optimization_mode_var.set(
        next(
            (
                k
                for k, v in optimization_mode_map.items()
                if str(v) == data.get("Optimization", "2")
            ),
            "Fast (genetic based algorithm)",
        )
    )

    # Set result priority with default = Balance Max
    state.result_priority_var.set(
        next(
            (
                k
                for k, v in result_priority_map.items()
                if str(v) == data.get("OptimizationCriterion", "0")
            ),
            "Balance Max",
        )
    )

    # Set forward mode with default = NO
    state.forward_mode_var.set(
        next(
            (
                k
                for k, v in forward_mode_map.items()
                if str(v) == data.get("ForwardMode", "0")
            ),
            "NO",
        )
    )
    def populate_date(picker: dict[str, tk.StringVar], value: str) -> None:
        if value:
            try:
                y, m, d = value.split(".")
                picker["year"].set(y)
                picker["month"].set(m.zfill(2))
                picker["day"].set(d.zfill(2))
            except ValueError:
                pass

    populate_date(state.fromdate_var, data.get("FromDate", ""))
    populate_date(state.todate_var, data.get("ToDate", ""))
    if state.forward_mode_var.get().lower() == "custom":
        populate_date(state.forwarddate_var, data.get("ForwardDate", ""))
    else:
        for part in state.forwarddate_var.values():
            part.set("")

    state.parsed_strategy_inputs = parse_tester_inputs_section(data.get("inputs", {}))
    state.status_var.set(f"Loaded: {Path(file_path).name}")


# --- Buttons ---
btn_row = forward_row + 2
btns = [
    ("📂 Load INI", lambda: load_ini_ui(state), "e", 0),
    ("🖱️ Set Report Click Point", lambda: set_report_click_location(), "w", 0),
    ("🔍 Scan for MT5", lambda: scan_and_select_mt5_install(), "e", 2),
    ("📈 Pick Symbols", lambda: open_symbol_picker(root, state.symbol_var), "w", 2),
    (
        "🛠️ Edit Inputs",
        lambda: open_input_editor(root, state.parsed_strategy_inputs),
        "w",
        3,
    ),
    ("🔁 Resume Previous Job", lambda: pick_and_resume_job(), "e", 3),
    ("📊 Analyze Results", lambda: open_streamlit_dashboard(), "e", 4),
    (
        "▶️ Run Optimizations",
        lambda: [save_current_settings(), run_optimization(state)],
        "w",
        4,
    ),
]

for text, cmd, anchor, col in btns:
    tk.Button(frame, text=text, command=cmd, width=30).grid(
        row=btn_row + col, column=0 if anchor == "e" else 1, pady=5, sticky=anchor
    )

tk.Label(frame, textvariable=state.report_click_set).grid(
    row=btn_row + 5, column=0, columnspan=2, pady=2
)

status_bar = tk.Label(root, textvariable=state.status_var, anchor="e")
status_bar.pack(fill="x", side="bottom")

root.mainloop()
