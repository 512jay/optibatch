import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from core.state import registry


def open_symbol_picker(root, on_save_callback, preselected=None):
    window = tk.Toplevel(root)
    window.title("Symbol Picker")

    symbol_file_path = registry.get("symbol_file_path")
    if not symbol_file_path:
        symbol_file_path = find_symbol_file_from_log_path()
        if symbol_file_path:
            registry.set("symbol_file_path", symbol_file_path)
            registry.save()

    symbols = read_symbols_from_file(symbol_file_path) if symbol_file_path else []

    if isinstance(preselected, str):
        selected_symbols = [s.strip() for s in preselected.split(",") if s.strip()]
    elif isinstance(preselected, (list, tuple)):
        selected_symbols = list(preselected)
    else:
        selected_symbols = []

    search_var = tk.StringVar()
    search_entry = tk.Entry(window, textvariable=search_var)
    search_entry.pack(fill="x")

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True)

    all_listbox = tk.Listbox(frame, selectmode="extended")
    all_listbox.pack(side="left", fill="both", expand=True)
    update_listbox(all_listbox, symbols)

    selected_listbox = tk.Listbox(frame)
    selected_listbox.pack(side="left", fill="both", expand=True)
    for s in selected_symbols:
        selected_listbox.insert("end", s)

    def filter_list(*_):
        query = search_var.get().lower()
        filtered = [s for s in symbols if query in s.lower()]
        update_listbox(all_listbox, filtered)

    search_var.trace_add("write", filter_list)

    # Buttons
    controls = tk.Frame(window)
    controls.pack()

    sort_var = tk.BooleanVar()
    sort_check = tk.Checkbutton(
        controls, text="Sort selected alphabetically", variable=sort_var
    )
    sort_check.grid(row=0, column=0, columnspan=2)

    tk.Button(
        controls,
        text="Add Selected →",
        command=lambda: move_items(all_listbox, selected_listbox),
    ).grid(row=1, column=0)
    tk.Button(
        controls,
        text="← Remove Selected",
        command=lambda: remove_items(selected_listbox),
    ).grid(row=1, column=1)
    tk.Button(
        controls,
        text="Save",
        command=lambda: save_selection(
            window, selected_listbox, sort_var.get(), on_save_callback
        ),
    ).grid(row=2, column=0)
    tk.Button(controls, text="Cancel", command=window.destroy).grid(row=2, column=1)
    tk.Button(
        controls,
        text="📁 Pick Symbol List File",
        command=lambda: pick_custom_file(window, all_listbox),
    ).grid(row=3, column=0, columnspan=2)


def update_listbox(listbox, items):
    listbox.delete(0, "end")
    for item in items:
        listbox.insert("end", item)


def move_items(source, target):
    items = [source.get(i) for i in source.curselection()]
    for item in items:
        if item not in target.get(0, "end"):
            target.insert("end", item)


def remove_items(listbox):
    for i in reversed(listbox.curselection()):
        listbox.delete(i)


def save_selection(window, listbox, sort, callback):
    items = list(listbox.get(0, "end"))
    if sort:
        items.sort()
    callback(",".join(items))
    window.destroy()


def find_symbol_file_from_log_path():
    log_path = registry.get("tester_log_path")
    if not log_path:
        return None
    term_path = Path(log_path).parent.parent
    sym_file = term_path / "MQL5" / "Files" / "symbols.txt"
    return str(sym_file) if sym_file.exists() else None


def pick_custom_file(window, listbox):
    path = filedialog.askopenfilename(
        title="Select Symbol List", filetypes=[("Text Files", "*.txt")]
    )
    if not path:
        return
    registry.set("symbol_file_path", path)
    registry.save()
    new_symbols = read_symbols_from_file(path)
    update_listbox(listbox, new_symbols)


def read_symbols_from_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read symbol file:\n{e}")
        return []
