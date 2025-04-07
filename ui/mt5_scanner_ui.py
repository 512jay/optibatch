from tkinter import (
    Toplevel,
    Listbox,
    Button,
    messagebox,
    Frame,
    Scrollbar,
    VERTICAL,
    RIGHT,
    Y,
    LEFT,
    BOTH,
)
from tkinter.ttk import Separator
from core.mt5.scanner import scan_mt5_from_origin
from core.config import config
from os import getenv
from pathlib import Path


def scan_and_select_mt5_install():
    base = Path(getenv("APPDATA")) / "MetaQuotes" / "Terminal"
    found = scan_mt5_from_origin(base)

    if not found:
        messagebox.showerror("No MT5 Found", "No valid MetaTrader 5 installs found.")
        return

    selection_window = Toplevel()
    selection_window.title("🧭 Select MetaTrader 5 Installation")
    selection_window.geometry("800x500")
    selection_window.resizable(False, False)

    # --- Root layout frame ---
    root_frame = Frame(selection_window)
    root_frame.pack(fill="both", expand=True)

    # --- Listbox area ---
    list_frame = Frame(root_frame)
    list_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    lb = Listbox(list_frame, font=("Segoe UI", 10), width=120, height=5)
    lb.pack(side=LEFT, fill="both", expand=True)

    scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=lb.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    lb.config(yscrollcommand=scrollbar.set)

    for i, install in enumerate(found):
        label = f"{install['broker_name']} — {install['terminal_path']}"
        lb.insert(i, label)

    # --- Separator + Button area ---
    bottom_frame = Frame(root_frame)
    bottom_frame.pack(fill="x", pady=(5, 10))

    Separator(bottom_frame, orient="horizontal").pack(fill="x", padx=10)

    Button(
        bottom_frame,
        text="✅ Use Selected Install",
        font=("Segoe UI", 10, "bold"),
        command=lambda: select(lb, found, selection_window),
    ).pack(pady=10)


def select(lb, found, selection_window):
    index = lb.curselection()
    if not index:
        messagebox.showwarning("No Selection", "Please select an install.")
        return
    selected = found[index[0]]
    config.set("terminal_path", selected["terminal_path"])
    config.set("data_path", selected["data_path"])
    messagebox.showinfo("✅ MT5 Set", f"MT5 path saved:\n{selected['terminal_path']}")
    selection_window.destroy()
