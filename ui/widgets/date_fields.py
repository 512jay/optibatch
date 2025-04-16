# ui/widgets/date_fields.py

import tkinter as tk
from tkinter import ttk, Misc


def build_date_fields(frame: Misc, row: int, label: str) -> dict[str, tk.StringVar]:
    """
    Adds labeled Year/Month/Day fields in a single row.
    Returns a dictionary of StringVar bindings.
    """
    ttk.Label(frame, text=label).grid(row=row, column=0, padx=(5, 10), sticky="e")

    year_var = tk.StringVar()
    month_var = tk.StringVar()
    day_var = tk.StringVar()

    year_entry = ttk.Entry(frame, textvariable=year_var, width=6)
    year_entry.grid(row=row, column=1, padx=(0, 5), sticky="w")

    month_entry = ttk.Entry(frame, textvariable=month_var, width=4)
    month_entry.grid(row=row, column=2, padx=(0, 5), sticky="w")

    day_entry = ttk.Entry(frame, textvariable=day_var, width=4)
    day_entry.grid(row=row, column=3, padx=(0, 5), sticky="w")

    return {"year": year_var, "month": month_var, "day": day_var}
