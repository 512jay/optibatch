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

    tk.Label(editor, text="Parameter").grid(row=0, column=0)
    tk.Label(editor, text="Default").grid(row=0, column=1)
    tk.Label(editor, text="Start").grid(row=0, column=2)
    tk.Label(editor, text="Step").grid(row=0, column=3)
    tk.Label(editor, text="End").grid(row=0, column=4)
    tk.Label(editor, text="Optimize").grid(row=0, column=5)

    for row, (param, values) in enumerate(parsed_strategy_inputs.items(), start=1):
        entries[param] = {}
        tk.Label(editor, text=param).grid(row=row, column=0)

        for col, field in zip(range(1, 5), ["default", "start", "step", "end"]):
            val = values.get(field, "")
            entry = tk.Entry(editor)
            entry.insert(0, str(val))
            entry.grid(row=row, column=col)
            entries[param][field] = entry

        optimize_var = BooleanVar(value=values.get("optimize", False))
        chk = tk.Checkbutton(editor, variable=optimize_var)
        chk.grid(row=row, column=5)
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
