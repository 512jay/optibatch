# ui/widgets/optimized_preview.py

import tkinter as tk
from tkinter import ttk
from core.input_parser import InputParam
from typing import NamedTuple, Optional, Callable
from math import ceil
import tkinter.font as tkFont

class OptimizedPreview(NamedTuple):
    frame: tk.Frame
    tree: ttk.Treeview
    save_button: ttk.Button


def autosize_columns(tree: ttk.Treeview) -> None:
    """
    Auto-resizes Treeview columns based on max content width.
    """
    style = ttk.Style()
    font_name = style.lookup("Treeview", "font")
    font = tkFont.nametofont("TkDefaultFont")

    for col in tree["columns"]:
        max_width = font.measure(col.capitalize()) + 20  # Start with heading
        for iid in tree.get_children():
            val = tree.set(iid, col)
            max_width = max(max_width, font.measure(val) + 20)
        tree.column(col, width=max_width)


def create_optimized_preview_widget(
    parent: tk.Widget,
    on_save_click: Optional[Callable[[], None]] = None,
) -> OptimizedPreview:
    frame = tk.Frame(parent)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Treeview styling
    style = ttk.Style()
    style.configure("Treeview", rowheight=36, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    columns = ("default", "start", "step", "stop")
    tree = ttk.Treeview(frame, columns=columns, show="tree headings")

    tree.heading("#0", text="Name", anchor="w")
    tree.column("#0", anchor="w", width=200, stretch=True)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center", width=100, stretch=True)

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.config(yscrollcommand=scrollbar.set)

    tree.bind("<Double-1>", lambda event: edit_cell(tree, event))

    # 💾 Save Button
    save_button = ttk.Button(frame, text="💾 Save Inputs")
    save_button.grid(row=1, column=0, columnspan=2, sticky="e", padx=10, pady=5)

    if on_save_click:
        save_button.config(command=on_save_click)

    return OptimizedPreview(frame=frame, tree=tree, save_button=save_button)


def count_variants(inputs: list[InputParam]) -> int:
    total = 1
    for param in inputs:
        if param.optimize:
            try:
                if (
                    param.start is not None
                    and param.end is not None
                    and param.step is not None
                ):
                    start = float(param.start)
                    end = float(param.end)
                    step = float(param.step)
                    if step > 0 and end >= start:
                        steps = ceil((end - start) / step) + 1
                        total *= steps
            except (ValueError, ZeroDivisionError):
                continue
    return total


def update_optimized_preview(
    widget: OptimizedPreview, inputs: list[InputParam]
) -> None:
    tree = widget.tree
    tree.delete(*tree.get_children())

    variant_count = count_variants(inputs)
    tree.heading("#0", text=f"   ({variant_count} variations)")

    for param in inputs:
        if param.optimize:
            tree.insert(
                "",
                "end",
                text=param.name,
                values=(param.default, param.start, param.step, param.end),
            )

    autosize_columns(tree)


def edit_cell(tree: ttk.Treeview, event: tk.Event) -> None:
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return

    row_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    if column_id == "#0":
        return

    bbox = tree.bbox(row_id, column_id)
    if not bbox:
        return

    x, y, width, height = bbox
    value = tree.set(row_id, column_id)

    entry = tk.Entry(tree)
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, value)
    entry.focus_set()

    def save_edit(event: tk.Event) -> None:
        new_val = entry.get().strip()
        if new_val:
            tree.set(row_id, column_id, new_val)
        entry.destroy()

    def cancel_edit(event: tk.Event) -> None:
        entry.destroy()

    entry.bind("<Return>", save_edit)
    entry.bind("<Escape>", cancel_edit)
    entry.bind("<FocusOut>", lambda e: save_edit(e))
