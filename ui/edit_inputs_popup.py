# File: ui/edit_inputs_popup.py

import tkinter as tk
from tkinter import ttk
from core.input_parser import InputParam


def open_edit_inputs_popup(inputs: list[InputParam]) -> None:
    popup = tk.Toplevel()
    popup.title("Edit Strategy Inputs")
    popup.minsize(570, 400)
    popup.resizable(True, True)

    canvas = tk.Canvas(popup)
    scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Header Row
    headers = ["Name", "Default", "Start", "Step", "End", "Optimize?"]
    for col, title in enumerate(headers):
        ttk.Label(scrollable_frame, text=title, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=col, padx=4, pady=4, sticky="w"
        )

    widgets = []

    for i, param in enumerate(inputs, start=1):
        row_data = {}

        ttk.Label(scrollable_frame, text=param.name).grid(
            row=i, column=0, sticky="w", padx=4, pady=2
        )

        default_var = tk.StringVar(value=str(param.default))
        start_var = tk.StringVar(value=str(param.start or ""))
        step_var = tk.StringVar(value=str(param.step or ""))
        end_var = tk.StringVar(value=str(param.end or ""))
        optimize_var = tk.BooleanVar(value=param.optimize)

        ttk.Entry(scrollable_frame, textvariable=default_var, width=10).grid(
            row=i, column=1, padx=2
        )
        ttk.Entry(scrollable_frame, textvariable=start_var, width=8).grid(
            row=i, column=2
        )
        ttk.Entry(scrollable_frame, textvariable=step_var, width=8).grid(
            row=i, column=3
        )
        ttk.Entry(scrollable_frame, textvariable=end_var, width=8).grid(row=i, column=4)
        ttk.Checkbutton(scrollable_frame, variable=optimize_var).grid(row=i, column=5)

        row_data.update(
            {
                "param": param,
                "default_var": default_var,
                "start_var": start_var,
                "step_var": step_var,
                "end_var": end_var,
                "optimize_var": optimize_var,
            }
        )
        widgets.append(row_data)

    def save_and_close():
        for widget in widgets:
            p = widget["param"]
            p.default = widget["default_var"].get()
            p.start = widget["start_var"].get() or None
            p.step = widget["step_var"].get() or None
            p.end = widget["end_var"].get() or None
            p.optimize = widget["optimize_var"].get()
        popup.destroy()

    # Bottom frame for the Save button
    button_frame = ttk.Frame(popup)
    button_frame.pack(fill="x", padx=10, pady=(0, 10))

    ttk.Button(button_frame, text="Save", command=save_and_close).pack(side="right")
