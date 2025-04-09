# ui/widgets/header_fields.py

import tkinter as tk
from tkinter import ttk, Misc


def build_header_fields(frame: Misc) -> dict[str, tk.StringVar]:
    """
    Build basic fields for expert, symbol, deposit, currency, leverage.
    Returns a dict of StringVar bindings.
    """
    expert_var = tk.StringVar()
    symbol_var = tk.StringVar()
    deposit_var = tk.StringVar()
    currency_var = tk.StringVar()
    leverage_var = tk.StringVar()

    labels = ["Expert Path:", "Symbol:", "Deposit:", "Currency:", "Leverage:"]
    vars = [expert_var, symbol_var, deposit_var, currency_var, leverage_var]

    for i, (label, var) in enumerate(zip(labels, vars)):
        ttk.Label(frame, text=label).grid(row=i, column=0, sticky="e")
        ttk.Entry(frame, textvariable=var, width=40).grid(row=i, column=1, sticky="w")

    return {
        "expert_var": expert_var,
        "symbol_var": symbol_var,
        "deposit_var": deposit_var,
        "currency_var": currency_var,
        "leverage_var": leverage_var,
    }
