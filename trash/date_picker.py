# ui/date_picker.py
# Purpose: Date picker for INI files, with year/month/day selectors + helpers for INI format

import tkinter as tk
from tkinter import ttk
from datetime import date


def create_ini_date_picker(parent, label="FromDate", date_string=None):
    """Creates a labeled date picker frame with year/month/day dropdowns."""
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=label).grid(row=0, column=0, columnspan=3, sticky="w")

    today = date.today()

    if date_string and isinstance(date_string, str) and "." in date_string:
        try:
            parts = [int(p) for p in date_string.split(".")]
            default = date(parts[0], parts[1], parts[2])
        except Exception:
            default = today
    else:
        default = today

    year_var = tk.StringVar(value=str(default.year))
    month_var = tk.StringVar(value=str(default.month))
    day_var = tk.StringVar(value=str(default.day))

    ttk.Combobox(
        frame,
        textvariable=year_var,
        width=6,
        values=[str(y) for y in range(2000, 2031)],
    ).grid(row=1, column=0)
    ttk.Combobox(
        frame, textvariable=month_var, width=4, values=[str(m) for m in range(1, 13)]
    ).grid(row=1, column=1)
    ttk.Combobox(
        frame, textvariable=day_var, width=4, values=[str(d) for d in range(1, 32)]
    ).grid(row=1, column=2)

    return frame, {"year": year_var, "month": month_var, "day": day_var}


def assemble_ini_date(var_dict: dict[str, tk.StringVar]) -> str:
    """Converts a dict of year/month/day StringVars into YYYY.MM.DD format."""
    y = var_dict["year"].get()
    m = var_dict["month"].get().zfill(2)
    d = var_dict["day"].get().zfill(2)
    return f"{y}.{m}.{d}"


def split_ini_date(date_str: str) -> tuple[str, str, str]:
    """Splits a YYYY.MM.DD string into (year, month, day)."""
    y, m, d = date_str.split(".")
    return y, str(int(m)), str(int(d))
