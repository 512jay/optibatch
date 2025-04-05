import tkinter as tk
from tkinter import Toplevel, Scrollbar, Listbox, END, MULTIPLE, messagebox
import json
from core.mt5.symbol_loader import load_symbols


def open_symbol_picker(root, symbol_var):
    try:
        with open("settings.json") as f:
            mt5_info = json.load(f)
    except Exception:
        messagebox.showerror(
            "Missing Selection", "Please choose an MT5 installation first."
        )
        return

    data_path = mt5_info["data_path"]

    def load_and_populate(force=False):
        listbox.delete(0, END)
        all_symbols = load_symbols(data_path, force_refresh=force)
        for symbol in all_symbols:
            listbox.insert(END, symbol)

    picker = Toplevel(root)
    picker.title("Select Symbols")

    frame = tk.Frame(picker)
    frame.pack(padx=10, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = Listbox(
        frame, selectmode=MULTIPLE, yscrollcommand=scrollbar.set, width=40, height=20
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    def save_selection():
        selected = [listbox.get(i) for i in listbox.curselection()]
        symbol_var.set(",".join(selected))
        picker.destroy()

    def refresh():
        load_and_populate(force=True)

    btn_frame = tk.Frame(picker)
    btn_frame.pack(pady=(5, 0))

    tk.Button(btn_frame, text="✅ Use Selected", command=save_selection).pack(
        side="left", padx=5
    )
    tk.Button(btn_frame, text="🔄 Refresh Symbols", command=refresh).pack(
        side="left", padx=5
    )

    load_and_populate()
