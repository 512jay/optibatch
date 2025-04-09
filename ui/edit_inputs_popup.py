# File: ui/edit_inputs_popup.py

import tkinter as tk
from tkinter import ttk
from core.input_parser import InputParam


def open_edit_inputs_popup(inputs: list[InputParam]) -> None:
    popup = tk.Toplevel()
    popup.title("Edit Strategy Inputs")
    popup.minsize(480,280)
    popup.grab_set()  # Make the popup modal
    popup.resizable(True, True)

    # Layout containers
    content_frame = ttk.Frame(popup)
    content_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(content_frame)
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
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

        default_var = tk.StringVar(value=str(param.default))
        start_var = tk.StringVar(value=str(param.start or ""))
        step_var = tk.StringVar(value=str(param.step or ""))
        end_var = tk.StringVar(value=str(param.end or ""))
        optimize_var = tk.BooleanVar(value=param.optimize)

        row_widgets: list[tk.Widget] = []

        # Use tk widgets so we can change background color
        label = tk.Label(scrollable_frame, text=param.name, anchor="w")
        label.grid(row=i, column=0, sticky="w", padx=4, pady=2)
        row_widgets.append(label)

        default_entry = tk.Entry(scrollable_frame, textvariable=default_var, width=10)
        default_entry.grid(row=i, column=1, padx=2)
        row_widgets.append(default_entry)

        start_entry = tk.Entry(scrollable_frame, textvariable=start_var, width=8)
        start_entry.grid(row=i, column=2)
        row_widgets.append(start_entry)

        step_entry = tk.Entry(scrollable_frame, textvariable=step_var, width=8)
        step_entry.grid(row=i, column=3)
        row_widgets.append(step_entry)

        end_entry = tk.Entry(scrollable_frame, textvariable=end_var, width=8)
        end_entry.grid(row=i, column=4)
        row_widgets.append(end_entry)

        def make_apply_bg(var: tk.BooleanVar, widgets: list[tk.Widget]):
            def _apply():
                color = "#cce7ff" if var.get() else "#ffffff"
                for widget in widgets:
                    widget.configure(background=color)
            return _apply

        apply_bg = make_apply_bg(optimize_var, row_widgets)

        optimize_check = tk.Checkbutton(
            scrollable_frame, variable=optimize_var, command=apply_bg
        )

        optimize_check.grid(row=i, column=5)
        row_widgets.append(optimize_check)

        apply_bg()  # Apply initial color based on optimize flag

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

    # Bottom bar
    button_frame = ttk.Frame(popup)
    button_frame.pack(fill="x", padx=10, pady=(0, 10))

    ttk.Button(button_frame, text="Save", command=save_and_close).pack(side="right")
