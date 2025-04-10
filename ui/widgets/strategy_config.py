# ui/widgets/strategy_config.py

import tkinter as tk
from tkinter import ttk, Misc
from core.enums import (
    OptimizationMode,
    ResultPriority,
    ForwardMode,
    ModelingMode,
    Timeframe,
    get_enum_label,
)


def build_strategy_config(frame: Misc):
    """
    Create strategy configuration dropdowns for Model, Optimization Mode, Result Priority, and Forward Mode.
    Returns a dictionary of StringVar bindings.
    """
    timeframe_var = tk.StringVar()
    strategy_model_var = tk.StringVar()
    optimization_mode_var = tk.StringVar()
    result_priority_var = tk.StringVar()
    forward_mode_var = tk.StringVar()

    row = 0

    ttk.Label(frame, text="Timeframe:").grid(row=row, column=0, sticky="e")
    ttk.OptionMenu(
        frame,
        timeframe_var,
        Timeframe.H1.label,
        *[t.label for t in Timeframe]
    ).grid(row=row, column=1, sticky="w")
    row += 1  # advance row counter after dropdown
    ttk.Label(frame, text="Modeling Mode:").grid(row=row, column=0, sticky="e")
    ttk.Combobox(
        frame,
        textvariable=strategy_model_var,
        values=[get_enum_label(ModelingMode, m.value) for m in ModelingMode],
        width=35,
    ).grid(row=row, column=1, sticky="w")

    row += 1
    ttk.Label(frame, text="Optimization Mode:").grid(row=row, column=0, sticky="e")
    ttk.Combobox(
        frame,
        textvariable=optimization_mode_var,
        values=[get_enum_label(OptimizationMode, m.value) for m in OptimizationMode],
        width=35,
    ).grid(row=row, column=1, sticky="w")

    row += 1
    ttk.Label(frame, text="Result Priority:").grid(row=row, column=0, sticky="e")
    ttk.Combobox(
        frame,
        textvariable=result_priority_var,
        values=[get_enum_label(ResultPriority, m.value) for m in ResultPriority],
        width=35,
    ).grid(row=row, column=1, sticky="w")

    row += 1
    ttk.Label(frame, text="Forward Mode:").grid(row=row, column=0, sticky="e")
    ttk.Combobox(
        frame,
        textvariable=forward_mode_var,
        values=[get_enum_label(ForwardMode, m.value) for m in ForwardMode],
        width=35,
    ).grid(row=row, column=1, sticky="w")

    return {
        "timeframe_var": timeframe_var,  # ✅ Add this
        "strategy_model_var": strategy_model_var,
        "optimization_mode_var": optimization_mode_var,
        "result_priority_var": result_priority_var,
        "forward_mode_var": forward_mode_var,
    }
