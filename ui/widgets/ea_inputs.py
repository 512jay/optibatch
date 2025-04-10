# Rename the file to match this cleaner version:
# ui/widgets/ea_inputs.py

import tkinter as tk
from tkinter import ttk, Misc
from typing import Callable, Optional


def build_inputs_section(
    frame: Misc, on_edit: Optional[Callable[[], None]] = None
) -> None:
    """
    Adds only the Edit Inputs button to the frame.
    The actual input display is handled by optimized_preview.
    """
    if on_edit:
        ttk.Button(frame, text="Edit Inputs", command=on_edit).pack(pady=(5, 0))
