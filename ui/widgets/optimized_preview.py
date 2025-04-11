# ui/widgets/optimized_preview.py

import tkinter as tk
from tkinter import ttk
from core.input_parser import InputParam
from typing import NamedTuple, Optional


class OptimizedPreview(NamedTuple):
    frame: tk.Frame
    tree: ttk.Treeview


def create_optimized_preview_widget(parent: tk.Widget) -> OptimizedPreview:
    frame = tk.Frame(parent)

    columns = ("default", "start", "step", "stop")

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="tree headings",
        height=3,
    )

    tree.heading("#0", text="Name", anchor="w")
    tree.column("#0", anchor="w", width=200, stretch=True)

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center", width=100, stretch=True)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame, command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.config(yscrollcommand=scrollbar.set)

    # Bind double-click to enable editing
    tree.bind("<Double-1>", lambda event: edit_cell(tree, event))

    return OptimizedPreview(frame=frame, tree=tree)


from math import ceil
from core.input_parser import InputParam


def count_variants(inputs: list[InputParam]) -> int:
    total = 1
    for param in inputs:
        if param.optimize:
            try:
                # Ensure values are not None before casting
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

    # Update header with total variants
    variant_count = count_variants(inputs)
    tree.heading("#0", text=f"Inputs to Optimize ({variant_count} variations)")


    for param in inputs:
        if param.optimize:
            tree.insert(
                "",
                "end",
                text=param.name,
                values=(param.default, param.start, param.step, param.end),
            )


def edit_cell(tree: ttk.Treeview, event: tk.Event) -> None:
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return

    row_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    if column_id == "#0":
        return  # Don't allow editing of the Name column

    bbox = tree.bbox(row_id, column_id)
    if not bbox:
        return  # Avoid unpacking error if bbox returns ""

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
