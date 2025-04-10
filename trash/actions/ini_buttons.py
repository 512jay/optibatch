# ui/actions/ini_buttons.py

import tkinter as tk
from tkinter import ttk
from typing import Callable


def build_ini_buttons(
    frame: ttk.Frame, actions: list[tuple[str, Callable[[], None], str, int]]
) -> None:
    """
    Adds a vertical column of buttons with hotkeys.
    Each tuple is: (label, command, hotkey, pad)
    """
    for i, (label, command, hotkey, pady) in enumerate(actions):
        ttk.Button(frame, text=label, command=command).pack(fill="x", pady=(pady, 0))
