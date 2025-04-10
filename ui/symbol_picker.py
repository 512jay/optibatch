import tkinter as tk
from tkinter import Toplevel, Scrollbar, Listbox, END, MULTIPLE, messagebox
import json
from core.mt5.symbol_loader import load_symbols
from pathlib import Path
from typing import Callable


def open_symbol_picker(root: tk.Tk, on_symbols_picked: Callable[[str], None]) -> None:    
    try:
        with open("settings.json") as f:
            mt5_info = json.load(f)
    except Exception:
        messagebox.showerror(
            "Missing Selection", "Please choose an MT5 installation first."
        )
        return

    data_path = mt5_info["data_path"]

    picker = Toplevel(root)
    picker.title("Select Symbols")

    main_frame = tk.Frame(picker)
    main_frame.pack(padx=10, pady=10)

    # Left frame - All symbols
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", padx=5)

    tk.Label(left_frame, text="All Symbols").pack()
    scrollbar = Scrollbar(left_frame)
    scrollbar.pack(side="right", fill="y")

    listbox = Listbox(
        left_frame,
        selectmode=MULTIPLE,
        yscrollcommand=scrollbar.set,
        width=35,
        height=20,
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    # Right frame - Selected symbols
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="left", padx=5)

    tk.Label(right_frame, text="Selected Symbols").pack()
    selected_listbox = Listbox(right_frame, width=35, height=20)
    selected_listbox.pack()

    def load_and_populate(force=False):
        listbox.delete(0, END)
        try:
            all_symbols = load_symbols(data_path, force_refresh=force)
            if not all_symbols:
                raise ValueError("Empty symbol list")
        except Exception:
            fallback_path = Path(__file__).parent / "symbols.txt"
            with open(fallback_path, encoding="utf-8") as f:
                all_symbols = [line.strip() for line in f if line.strip()]
            messagebox.showwarning(
                "Fallback", "Loaded default symbol list from symbols.txt"
            )

        for symbol in all_symbols:
            listbox.insert(END, symbol)

    def add_to_selected():
        for i in listbox.curselection():
            symbol = listbox.get(i)
            if symbol not in selected_listbox.get(0, END):
                selected_listbox.insert(END, symbol)

    def remove_selected(event=None):
        selected = selected_listbox.curselection()
        for i in reversed(selected):  # Remove from bottom up
            selected_listbox.delete(i)


    def save_selection() -> None:
        selected = selected_listbox.get(0, END)
        on_symbols_picked(",".join(selected))  # ✅ Call the function passed in
        picker.destroy()

    def refresh():
        load_and_populate(force=True)

    # Controls
    ctrl_frame = tk.Frame(picker)
    ctrl_frame.pack(pady=(5, 0))
    tk.Button(ctrl_frame, text="✅ Use Selected", command=save_selection).pack(
        side="left", padx=5
    )
    tk.Button(ctrl_frame, text="🔄 Refresh Symbols", command=refresh).pack(
        side="left", padx=5
    )
    tk.Button(ctrl_frame, text="➕ Add Selected", command=add_to_selected).pack(
        side="left", padx=5
    )

    selected_listbox.bind("<Double-Button-1>", remove_selected)

    load_and_populate()
