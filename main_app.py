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
from ui.symbol_picker import open_symbol_picker
from ui.input_editor import open_input_editor
from ui.date_picker import create_ini_date_picker
from core.jobs_utils.runner import pick_and_resume_job
from ui.mt5_scanner_ui import scan_and_select_mt5_install
from ui.mt5_menu import build_mt5_menu
from dotenv import load_dotenv
from ui.ini_loader import load_ini_ui, try_load_cached_ini

import json
from core.registry import get_last_used_install
from core.input_parser import InputParam
from core.enums import (
    OptimizationMode,
    ResultPriority,
    ForwardMode,
    get_enum_label,)


load_dotenv()
SETTINGS_FILE = Path("settings.json")
selected_mt5_id = get_last_used_install()


def get_date_from_picker(picker_dict):
    return f"{picker_dict['year'].get()}.{picker_dict['month'].get()}.{picker_dict['day'].get()}"


report_click = config.get("report_click", {"x": 0, "y": 0})


# --- GUI Setup ---
root = tk.Tk()
root.title("Optibatch Main Interface - [MT5 Install Name]")

# --- Top Menu Bar ---
menubar = tk.Menu(root)
build_mt5_menu(menubar, root, selected_mt5_id)
root.config(menu=menubar)


# --- Application State ---
expert_path_var = tk.StringVar()
symbol_var = tk.StringVar()
deposit_var = tk.StringVar()
currency_var = tk.StringVar()
leverage_var = tk.StringVar()

optimization_mode_var = tk.StringVar()
result_priority_var = tk.StringVar()
forward_mode_var = tk.StringVar()

fromdate_var = {"year": tk.StringVar(), "month": tk.StringVar(), "day": tk.StringVar()}
todate_var = {"year": tk.StringVar(), "month": tk.StringVar(), "day": tk.StringVar()}
forwarddate_var = {
    "year": tk.StringVar(),
    "month": tk.StringVar(),
    "day": tk.StringVar(),
}

report_click_set = tk.StringVar(value="Not Set")
parsed_strategy_inputs: list[InputParam] = []
status_var = tk.StringVar()


report_click_set = tk.StringVar(value="Not Set")
click = config.get("report_click")
if click and "x" in click and "y" in click:
    report_click_set.set(f"Loaded ({click['x']}, {click['y']})")


# --- Create Date Pickers ---
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

from_frame, fromdate_var = create_ini_date_picker(frame, "FromDate")
to_frame, todate_var = create_ini_date_picker(frame, "ToDate")
forwarddate_frame, forwarddate_var = create_ini_date_picker(frame, "ForwardDate")


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
        report_click_set.set(f"Set at ({x}, {y})")
        logger.success(f"Click captured at ({x}, {y})")
        messagebox.showinfo("Click Saved", f"Click location set at ({x}, {y})")

    update_timer(10)


# --- GUI LAYOUT ---
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

fields = [
    ("Expert Path", expert_path_var),
    ("Symbols (comma-separated)", symbol_var),
    ("Deposit", deposit_var),
    ("Currency", currency_var),
    ("Leverage", leverage_var),
]

for i, (label_text, var) in enumerate(fields):
    tk.Label(frame, text=label_text).grid(row=i, column=0, sticky="e")
    tk.Entry(frame, textvariable=var, width=40).grid(row=i, column=1, sticky="w")

opt_row = len(fields)

tk.Label(frame, text="Optimization Mode").grid(row=opt_row, column=0, sticky="e")
ttk.Combobox(
    frame,
    textvariable=optimization_mode_var,
    values=[get_enum_label(OptimizationMode, e.value) for e in OptimizationMode],
    width=35,
).grid(row=opt_row, column=1, sticky="w")

tk.Label(frame, text="Result Priority").grid(row=opt_row + 1, column=0, sticky="e")
ttk.Combobox(
    frame,
    textvariable=result_priority_var,
    values=[get_enum_label(ResultPriority, e.value) for e in ResultPriority],
    width=35,
).grid(row=opt_row + 1, column=1, sticky="w")

from_frame, fromdate_var = create_ini_date_picker(frame, "FromDate")
to_frame, todate_var = create_ini_date_picker(frame, "ToDate")
from_frame.grid(row=opt_row + 2, column=0, columnspan=2, pady=5)
to_frame.grid(row=opt_row + 3, column=0, columnspan=2, pady=5)

forward_row = opt_row + 4
ttk.Combobox(
    frame,
    textvariable=forward_mode_var,
    values=[get_enum_label(ForwardMode, e.value) for e in ForwardMode],
    width=20,
).grid(row=forward_row, column=1, sticky="w")

forwarddate_frame, forwarddate_var = create_ini_date_picker(frame, "ForwardDate")
forwarddate_frame.grid(row=forward_row + 1, column=0, columnspan=2, pady=5)




# --- Load INI ---
# Refactored version of load_ini_ui using session-based cache

try_load_cached_ini(
    expert_var=expert_path_var,
    symbol_var=symbol_var,
    deposit_var=deposit_var,
    currency_var=currency_var,
    leverage_var=leverage_var,
    optimization_var=optimization_mode_var,
    result_priority_var=result_priority_var,
    forward_mode_var=forward_mode_var,
    from_picker=fromdate_var,
    to_picker=todate_var,
    forward_picker=forwarddate_var,
    parsed_inputs_holder=parsed_strategy_inputs,
    status_var=status_var,
)


# --- Buttons ---
btn_row = forward_row + 2
btns = [
    (
        "📂 Load INI",
        lambda: load_ini_ui(
            expert_var=expert_path_var,
            symbol_var=symbol_var,
            deposit_var=deposit_var,
            currency_var=currency_var,
            leverage_var=leverage_var,
            optimization_var=optimization_mode_var,
            result_priority_var=result_priority_var,
            forward_mode_var=forward_mode_var,
            from_picker=fromdate_var,
            to_picker=todate_var,
            forward_picker=forwarddate_var,
            parsed_inputs_holder=parsed_strategy_inputs,
            status_var=status_var,
        ),
        "e",
        0,
    ),
    ("🖱️ Set Report Click Point", lambda: set_report_click_location(), "w", 0),
    ("🔍 Scan for MT5", lambda: scan_and_select_mt5_install(), "e", 2),
    ("📈 Pick Symbols", lambda: open_symbol_picker(root, symbol_var), "w", 2),
    (
        "🛠️ Edit Inputs",
        lambda: open_input_editor(root, parsed_strategy_inputs),
        "w",
        3,
    ),
    ("🔁 Resume Previous Job", lambda: pick_and_resume_job(), "e", 3),
    ("📊 Analyze Results", lambda: open_streamlit_dashboard(), "e", 4),
    (
        "▶️ Run Optimizations",
        lambda: [],
        "w",
        4,
    ),
]

for text, cmd, anchor, col in btns:
    tk.Button(frame, text=text, command=cmd, width=30).grid(
        row=btn_row + col, column=0 if anchor == "e" else 1, pady=5, sticky=anchor
    )

tk.Label(frame, textvariable=report_click_set).grid(
    row=btn_row + 5, column=0, columnspan=2, pady=2
)

status_bar = tk.Label(root, textvariable=status_var, anchor="e")
status_bar.pack(fill="x", side="bottom")

root.mainloop()
