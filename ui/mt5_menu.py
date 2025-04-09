# ui/mt5_menu.py

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from pathlib import Path
from mt5.controller import get_mt5_window_geometry
from core.registry import update_geometry, load_registry, save_registry, get_click_position, update_click_position
from core.types import WindowGeometry  # adjust if needed
from typing import Optional
from typing_extensions import TypedDict
import pynput

# Store selected install ID in memory
_selected_install_id = None
_root_window = None  # Reference to root for title updates


def build_mt5_menu(
    menubar: tk.Menu, root: tk.Tk, selected_mt5_id: Optional[str] = None
):
    global _selected_install_id, _root_window
    _selected_install_id = selected_mt5_id
    _root_window = root

    mt5_menu = tk.Menu(menubar, tearoff=0)

    mt5_menu.add_command(
        label="📐 Save Window Geometry",
        command=lambda: save_geometry(_selected_install_id),
    )
    mt5_menu.add_separator()
    mt5_menu.add_command(label="📁 Add MT5 Install", command=lambda: add_install(root))
    mt5_menu.add_command(
        label="🗂 Select MT5 Install", command=lambda: select_install(root)
    )
    mt5_menu.add_command(
        label="🖱 Set Click Position",
        command=lambda: set_click_position(_selected_install_id),
    )

    menubar.add_cascade(label="MT5", menu=mt5_menu)
    _update_window_title()


def save_geometry(install_id: Optional[str]):
    if not install_id:
        messagebox.showwarning("Missing Install", "No MT5 install selected.")
        return

    registry = load_registry()
    install = registry.get(install_id)
    if not install:
        messagebox.showerror("Error", f"Install '{install_id}' not found in registry.")
        return

    mt5_path = Path(install["path"])
    geometry = get_mt5_window_geometry(mt5_path)
    if geometry:
        update_geometry(mt5_path, geometry, install_id)
        messagebox.showinfo("Success", f"Window geometry saved for: {install_id}")
    else:
        messagebox.showerror("Error", "Could not capture MT5 window position.")


def add_install(root):
    selected_folder = filedialog.askdirectory(title="Select MT5 Folder")
    if not selected_folder:
        return

    install_id = simpledialog.askstring(
        "Install Name", "Enter a short name (e.g. 'forex_demo'):"
    )
    if not install_id:
        return

    registry = load_registry()
    if install_id in registry:
        messagebox.showwarning(
            "Duplicate Install ID", f"'{install_id}' is already registered."
        )
        return

    resolved_path = str(Path(selected_folder).resolve())
    registry[install_id] = {
        "path": resolved_path,
        "label": install_id.replace("_", " ").title(),
    }
    save_registry(registry)
    messagebox.showinfo("Install Added", f"Registered install: {install_id}")


def select_install(root):
    global _selected_install_id
    registry = load_registry()
    if not registry:
        messagebox.showwarning("No Installs", "No MT5 installs registered.")
        return

    options = list(registry.keys())
    install_id = simpledialog.askstring(
        "Select MT5 Install",
        f"Available installs:\n{chr(10).join(options)}\n\nEnter install ID:",
    )
    from core.registry import set_last_used_install

    if install_id and install_id in registry:
        _selected_install_id = install_id
        set_last_used_install(install_id)  # ✅ record the choice
        _update_window_title()
        messagebox.showinfo("Selected", f"Current install: {install_id}")


def _update_window_title():
    if _root_window:
        title = "Optibach"
        if _selected_install_id:
            title += f" — [{_selected_install_id}]"
        _root_window.title(title)


def set_click_position(install_id: Optional[str]):
    if not install_id:
        messagebox.showwarning("Missing Install", "No MT5 install selected.")
        return

    # Prompt user to click somewhere on screen
    from pynput import mouse

    position = []

    def on_click(x, y, button, pressed):
        if pressed:
            position.append((x, y))
            listener.stop()

    try:
        from pynput.mouse import Listener

        messagebox.showinfo(
            "Click Anywhere", "Please click anywhere on screen to set the position..."
        )
        with Listener(on_click=on_click) as listener:
            listener.join()
    except ImportError:
        messagebox.showerror("Error", "pynput not installed. Run: pip install pynput")
        return

    if position:
        update_click_position(install_id, position[0])
        messagebox.showinfo("Success", f"Click position saved: {position[0]}")
