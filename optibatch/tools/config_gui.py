import tkinter as tk
from tkinter import filedialog, messagebox
import configparser
import json
from datetime import datetime
from pathlib import Path


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
        "strategy_input_parameters": {},  # Skipping detailed input parsing for v1
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
    expert_path_var.set(data["expert_path"])
    symbol_var.set(data["symbol"])
    leverage_var.set(data["leverage"])
    currency_var.set(data["currency"])
    deposit_var.set(data["deposit"])
    opt_mode_var.set(data["optimization"])
    opt_crit_var.set(data["optimization_criterion"])
    status_var.set(f"Loaded: {Path(file_path).name}")


# --- GUI ---

root = tk.Tk()
root.title("Optibach Config Generator")

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

tk.Button(frame, text="💾 Save Config", command=save_config).grid(
    row=i + 1, column=0, columnspan=2, pady=10
)
tk.Label(frame, textvariable=status_var, fg="blue").grid(
    row=i + 2, column=0, columnspan=2
)

root.mainloop()
