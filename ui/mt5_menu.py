# ui/mt5_menu.py

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from pathlib import Path
from mt5.controller import get_mt5_window_geometry
from core.state import registry
from core.types import WindowGeometry  # adjust if needed
from typing import Optional
from typing_extensions import Tuple
import pynput
from  core.state import registry


def add_install(root) -> None:
    """
    Prompt the user to select an MT5 folder and save it as the active install path.
    """
    selected_folder = filedialog.askdirectory(title="Select MT5 Folder")
    if not selected_folder:
        return

    resolved_path = str(Path(selected_folder).resolve())

    confirm = messagebox.askyesno(
        "Use This Install?", f"Set this MT5 path as the default?\n\n{resolved_path}"
    )
    if not confirm:
        return

    registry.set("install_path", resolved_path)

    install_label = simpledialog.askstring(
        "Label This Install", "Enter a short name (e.g. 'forex_demo'):"
    )
    if install_label:
        registry.set("install_label", install_label.strip())

    registry.save()
    messagebox.showinfo("Install Saved", f"MT5 path saved to app settings.")
    update_window_title(root)


def add_log_folder(root):
    """
    Prompt the user to select an MT5 folder and save it as the active install path.
    """
    selected_folder = filedialog.askdirectory(title="Select MT5 Tester/Log Folder")
    if not selected_folder:
        return

    resolved_path = str(Path(selected_folder).resolve())

    confirm = messagebox.askyesno(
        "Tester Log Folder", f"Set this path as the default log folder to get Tester info?\n\n{resolved_path}"
    )
    if not confirm:
        return

    registry.set("tester_log_path", resolved_path)
    registry.save()
    messagebox.showinfo("Tester Log Path", f"Tester log path saved to app settings.")
    update_window_title(root)


def build_mt5_menu(
    menubar: tk.Menu, root: tk.Tk, selected_mt5_id: Optional[str] = None
):
    """
    Construct the MT5 menu and return it for use in the menubar.
    """

    mt5_menu = tk.Menu(menubar, tearoff=0)

    mt5_menu.add_command(
        label="📐 Save Window Geometry",
        command=lambda: save_geometry(),
    )
    mt5_menu.add_separator()
    mt5_menu.add_command(label="📁 Select MT5 Install", command=lambda: add_install(root))
    mt5_menu.add_command(label="Select MT5 Tester/Logs Folder", command=lambda: add_log_folder(root))
    mt5_menu.add_command(
        label="🖱 Set Click Position",
        command=lambda: set_click_position(),
    )

    menubar.add_cascade(label="MT5", menu=mt5_menu)
    update_window_title(root)


def save_geometry() -> None:
    mt5_path_str = registry.get("install_path")
    if not mt5_path_str:
        messagebox.showwarning("Missing Install", "No MT5 install path saved.")
        return

    mt5_path = Path(mt5_path_str)
    geometry: WindowGeometry | None = get_mt5_window_geometry(mt5_path)

    if geometry:
        registry.set("window_geometry", geometry)
        registry.save()
        messagebox.showinfo("Success", "Window geometry saved.")
    else:
        messagebox.showerror("Error", "Could not capture MT5 window position.")

# Update the window title with the install label
def update_window_title(root: tk.Tk) -> None:
    title = "Optibach"
    label = registry.get("install_label")
    if label:
        title += f" — [{label}]"
    root.title(title)


def set_click_position() -> None:
    """
    Record a user click position on the screen and save it for reuse.
    """
    try:
        from pynput.mouse import Listener
    except ImportError:
        messagebox.showerror("Error", "pynput not installed. Run: pip install pynput")
        return

    position = []

    def on_click(x, y, button, pressed):
        if pressed:
            position.append((x, y))
            listener.stop()

    messagebox.showinfo(
        "Click Anywhere", "Please click anywhere on the screen, after clicking OK, to set the position..."
    )

    with Listener(on_click=on_click) as listener:
        listener.join()

    if position:
        registry.set("click_position", position[0])
        registry.save()
        messagebox.showinfo("Success", f"Click position saved: {position[0]}")
    else:
        messagebox.showwarning("No Position", "No click was recorded.")
