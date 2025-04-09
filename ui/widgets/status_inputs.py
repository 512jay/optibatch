# ui/widgets/status_inputs.py

import tkinter as tk
from tkinter import ttk, Misc
from typing import Callable
from core.input_parser import InputParam
from typing import Optional, Any

def build_status_bar(frame: ttk.Frame, status_var: tk.StringVar) -> None:
    ttk.Label(frame, textvariable=status_var, anchor="w").pack(fill="x")


def build_inputs_section(
    frame: Misc,
    parsed_inputs: list[Any],
    on_edit: Optional[Callable[[], None]] = None
):
    """
    Adds a section for displaying parsed inputs with an optional edit button.
    Each input is displayed with its name and value.
    """
    ttk.Label(frame, text="Parsed Inputs:").pack(anchor="w")

    for input_param in parsed_inputs:
        name = input_param.name
        value = input_param.value
        ttk.Label(frame, text=f"{name}: {value}").pack(anchor="w")

    if on_edit:
        ttk.Button(frame, text="Edit Inputs", command=on_edit).pack(pady=(5, 0))