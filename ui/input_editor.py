import tkinter as tk
from tkinter import Toplevel, BooleanVar, messagebox


def safe_eval(val):
    if val.lower() == "true":
        return True
    elif val.lower() == "false":
        return False
    try:
        return eval(val)
    except:
        return val


def open_input_editor(root, parsed_strategy_inputs):
    if not parsed_strategy_inputs:
        messagebox.showerror("No inputs", "You must load an INI file first.")
        return

    editor = Toplevel(root)
    editor.title("Edit Strategy Inputs")
    entries = {}

    header_font = ("Arial", 11, "bold")
    entry_font = ("Consolas", 11)

    container = tk.Frame(editor)
    container.pack(padx=10, pady=10)

    # Header Row
    headers = [
        ("Parameter", 34),  # widened for better visibility
        ("Default", 12),
        ("Start", 12),
        ("Step", 12),
        ("End", 12),
        ("Optimize", 9),
    ]
    for col, (text, width) in enumerate(headers):
        tk.Label(
            container,
            text=text,
            font=header_font,
            anchor="center",
            width=width,
            padx=10,
        ).grid(row=0, column=col)

    def update_row_style(row_widgets, var, toggle):
        color = "#e0f7ff" if var.get() else editor.cget("bg")
        for widget in row_widgets:
            widget.config(bg=color)
        toggle.config(text="✓" if var.get() else "✗")

    # Dynamic Rows
    for row_index, (param, values) in enumerate(
        parsed_strategy_inputs.items(), start=1
    ):
        row_widgets = []

        # Parameter label
        label = tk.Label(container, text=param, font=entry_font, width=34, anchor="w")
        label.grid(row=row_index, column=0, padx=5, pady=3)
        row_widgets.append(label)

        entries[param] = {}

        # Default, Start, Step, End fields
        for col, field in zip(range(1, 5), ["default", "start", "step", "end"]):
            val = values.get(field, "")
            entry = tk.Entry(container, font=entry_font, width=12, justify="right")
            entry.insert(0, str(val))
            entry.grid(row=row_index, column=col, padx=5, pady=3)
            entries[param][field] = entry
            row_widgets.append(entry)

        # Optimize toggle
        optimize_var = BooleanVar(value=values.get("optimize", False))
        toggle = tk.Checkbutton(
            container,
            variable=optimize_var,
            indicatoron=False,
            width=3,
            selectcolor="#4caf50",
            font=("Arial", 12, "bold"),
        )
        toggle.grid(row=row_index, column=5, padx=5, pady=3)
        entries[param]["optimize"] = optimize_var
        row_widgets.append(toggle)

        # Now bind the proper command after the widget is created
        toggle.config(
            command=lambda rw=row_widgets, v=optimize_var, t=toggle: update_row_style(rw, v, t)
        )

        # Initialize style
        update_row_style(row_widgets, optimize_var, toggle)

    # Save button
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

    tk.Button(
        editor,
        text="Save Inputs",
        command=save_and_close,
        font=("Arial", 12),
        padx=10,
        pady=5,
    ).pack(pady=(5, 15))
