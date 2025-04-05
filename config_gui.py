import os
import configparser
import json
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import BooleanVar, Toplevel, filedialog, messagebox
from typing import Any
from core.mt5.scanner import scan_mt5_from_origin


# Global storage
parsed_strategy_inputs: Any = {}
SETTINGS_PATH = Path("settings.json")
selected_terminal = tk.StringVar()


def safe_eval(val):
    if val.lower() == "true":
        return True
    elif val.lower() == "false":
        return False
    try:
        return eval(val)
    except:
        return val


def parse_tester_inputs_section(inputs):
    parsed = {}
    for key, value in inputs.items():
        parts = value.split("||")
        if len(parts) < 2:
            continue

        default_val = safe_eval(parts[0])
        optimize_flag = parts[-1] == "Y"

        param_entry = {
            "default": default_val,
            "start": safe_eval(parts[1]),
            "step": safe_eval(parts[2]),
            "end": safe_eval(parts[3]),
            "optimize": optimize_flag,
        }

        parsed[key] = param_entry
    return parsed


def open_input_editor(root):
    if not parsed_strategy_inputs:
        messagebox.showerror("No inputs", "You must load an INI file first.")
        return

    editor = Toplevel(root)
    editor.title("Edit Strategy Inputs")
    entries = {}

    tk.Label(editor, text="Parameter").grid(row=0, column=0)
    tk.Label(editor, text="Default").grid(row=0, column=1)
    tk.Label(editor, text="Start").grid(row=0, column=2)
    tk.Label(editor, text="Step").grid(row=0, column=3)
    tk.Label(editor, text="End").grid(row=0, column=4)
    tk.Label(editor, text="Optimize").grid(row=0, column=4)

    for row, (param, values) in enumerate(parsed_strategy_inputs.items(), start=1):
        entries[param] = {}

        tk.Label(editor, text=param).grid(row=row, column=0)

        for col, field in zip(range(2, 6), ["default", "start", "step", "end"]):
            val = values.get(field, "")
            entry = tk.Entry(editor)
            entry.insert(0, str(val))
            entry.grid(row=row, column=col)
            entries[param][field] = entry

        optimize_var = BooleanVar(value=values.get("optimize", False))
        chk = tk.Checkbutton(editor, variable=optimize_var)
        chk.grid(row=row, column=4)
        entries[param]["optimize"] = optimize_var

    def save_and_close():
        for param, widgets in entries.items():
            parsed_strategy_inputs[param]["default"] = safe_eval(
                widgets["default"].get()
            )
            parsed_strategy_inputs[param]["optimize"] = widgets["optimize"].get()
            for field in ["start", "step", "end"]:
                val = widgets[field].get().strip()
                if val:
                    parsed_strategy_inputs[param][field] = safe_eval(val)
                elif field in parsed_strategy_inputs[param]:
                    del parsed_strategy_inputs[param][field]
        editor.destroy()

    tk.Button(editor, text="Save Inputs", command=save_and_close).grid(
        row=row + 1, column=0, columnspan=7, pady=10
    )


def parse_ini_file(filepath):
    parser = configparser.ConfigParser()
    try:
        with open(filepath, encoding="utf-8") as f:
            parser.read_file(f)
    except UnicodeDecodeError:
        with open(filepath, encoding="utf-16") as f:
            parser.read_file(f)

    tester = parser["Tester"]
    inputs = parser["TesterInputs"]

    return {
        "expert_path": tester.get("Expert", ""),
        "symbol": tester.get("Symbol", ""),
        "leverage": tester.get("Leverage", "100"),
        "currency": tester.get("Currency", "USD"),
        "deposit": tester.get("Deposit", "10000"),
        "optimization": tester.get("Optimization", "0"),
        "optimization_criterion": tester.get("OptimizationCriterion", "0"),
        "inputs": inputs,
    }


def save_config():
    expert_path = expert_path_var.get()
    expert_name = Path(expert_path).stem
    symbol = symbol_var.get()
    deposit = float(deposit_var.get())
    currency = currency_var.get()
    leverage = f"1:{leverage_var.get()}"
    report_types = report_var.get().split(",")

    optimization_map = {"0": "disabled", "1": "slow", "2": "fast", "3": "marketwatch"}
    criterion_map = {
        "0": "balance max",
        "1": "profit factor max",
        "2": "expected payoff max",
        "3": "drawdown min",
        "4": "recovery factor max",
        "5": "sharpe ratio max",
        "6": "custom max",
        "7": "complex criterion max",
    }

    config = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "report_types": report_types,
        },
        "expert": {"path": expert_path, "name": expert_name},
        "symbols": [symbol],
        "date": {"start": "2024-01-01", "end": "2025-01-01"},
        "forward": {"mode": "NO"},
        "delays": 0,
        "modelling": "Every tick",
        "deposit": {"amount": deposit, "currency": currency, "leverage": leverage},
        "optimization": {
            "mode": optimization_map.get(opt_mode_var.get(), "disabled"),
            "result_priority": criterion_map.get(opt_crit_var.get(), "balance max"),
        },
        "custom_criteria": {"profit_to_drawdown_ratio": 3.0},
        "strategy_input_parameters": parsed_strategy_inputs,
    }

    out_path = Path("optibach/config/config.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(config, f, indent=2)

    messagebox.showinfo("Saved", f"✅ Config saved to:\n{out_path.resolve()}")


def load_ini():
    file_path = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini")])
    if not file_path:
        return
    data = parse_ini_file(file_path)
    global parsed_strategy_inputs
    parsed_strategy_inputs = parse_tester_inputs_section(data["inputs"])
    expert_path_var.set(data["expert_path"])
    symbol_var.set(data["symbol"])
    leverage_var.set(data["leverage"])
    currency_var.set(data["currency"])
    deposit_var.set(data["deposit"])
    opt_mode_var.set(data["optimization"])
    opt_crit_var.set(data["optimization_criterion"])
    status_var.set(f"Loaded: {Path(file_path).name}")


def load_settings():
    if SETTINGS_PATH.exists():
        try:
            with SETTINGS_PATH.open() as f:
                data = json.load(f)
                selected_terminal.set(data.get("terminal_path", ""))
                if selected_terminal.get():
                    status_var.set(f"Last MT5: {selected_terminal.get()}")
        except Exception as e:
            print(f"⚠️ Failed to load settings: {e}")


def choose_mt5_install():
    installs = scan_mt5_from_origin(
        Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal"
    )
    if not installs:
        messagebox.showerror("No installs", "No MT5 installations found.")
        return

    win = Toplevel(root)
    win.title("Choose MT5 Installation")
    local_var = tk.StringVar(value=selected_terminal.get())
    local_paths = {}

    for idx, install in enumerate(installs):
        val = install["terminal_path"]
        local_paths[val] = install["data_path"]
        tk.Radiobutton(
            win,
            text=f"{Path(val).name}  [{install['data_path']}]",
            variable=local_var,
            value=val,
            anchor="w",
            justify="left",
        ).pack(anchor="w")

    def confirm():
        selected_terminal.set(local_var.get())
        SETTINGS_PATH.write_text(
            json.dumps(
                {
                    "terminal_path": selected_terminal.get(),
                    "data_path": local_paths[selected_terminal.get()],
                },
                indent=2,
            )
        )
        status_var.set(f"Selected MT5: {selected_terminal.get()}")
        win.destroy()

    tk.Button(win, text="OK", command=confirm).pack(pady=5)


# GUI setup
root = tk.Tk()
root.title("Optibach Config Generator")
load_settings()
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

status_var = tk.StringVar()
expert_path_var = tk.StringVar()
symbol_var = tk.StringVar()
leverage_var = tk.StringVar(value="100")
currency_var = tk.StringVar(value="USD")
deposit_var = tk.StringVar(value="10000")
opt_mode_var = tk.StringVar(value="0")
opt_crit_var = tk.StringVar(value="0")
report_var = tk.StringVar(value="csv,html")

tk.Button(frame, text="📂 Load INI File", command=load_ini).grid(
    row=0, column=0, columnspan=2, pady=(0, 10)
)

fields = [
    ("Expert Path", expert_path_var),
    ("Symbol", symbol_var),
    ("Deposit", deposit_var),
    ("Currency", currency_var),
    ("Leverage", leverage_var),
    ("Optimization Mode (0-3)", opt_mode_var),
    ("Result Priority (0-7)", opt_crit_var),
    ("Report Types (csv,html)", report_var),
]

for i, (label, var) in enumerate(fields, start=1):
    tk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
    tk.Entry(frame, textvariable=var, width=40).grid(row=i, column=1)

tk.Button(frame, text="🛠 Edit Inputs…", command=lambda: open_input_editor(root)).grid(
    row=i + 1, column=0, columnspan=2, pady=5
)
tk.Button(frame, text="💾 Save Config", command=save_config).grid(
    row=i + 2, column=0, columnspan=2, pady=10
)
tk.Label(frame, textvariable=status_var, fg="blue").grid(
    row=i + 3, column=0, columnspan=2
)

root.mainloop()
