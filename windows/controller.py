# file: optibatch/windows/controller.py
# Controls the MT5 window geometry and focus based on process path
# Ensures correct automation setup (e.g., right-click coordinates are valid)

import time
import json
import psutil
import win32gui  # type: ignore
import win32con  # type: ignore
import win32process  # type: ignore
from pathlib import Path
from typing import Optional, Tuple
from loguru import logger
from core.state import registry


def load_window_geometry() -> Optional[Tuple[int, int, int, int]]:
    """
    Load saved window geometry from app_state.json via registry.
    Returns (x, y, width, height) or None if missing/incomplete.
    """
    data = registry.get("window_geometry")
    if not data:
        logger.warning("⚠️ No saved geometry found in registry.")
        return None

    x = data.get("x")
    y = data.get("y")
    width = data.get("width")
    height = data.get("height")
    if None in (x, y, width, height):
        logger.warning("⚠️ Incomplete geometry config.")
        return None
    return x, y, width, height


def find_mt5_window() -> Optional[int]:
    """
    Locate the MT5 window handle by matching process path with registry's terminal_path.
    Returns the window handle (HWND) or None if not found.
    """
    terminal_path = registry.get("terminal_path")
    if not terminal_path:
        logger.error("❌ terminal_path not set in registry.")
        return None
    target_path = str(Path(terminal_path).resolve()).lower()

    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            if (
                proc.info["name"]
                and "terminal64.exe" in proc.info["name"].lower()
                and proc.info["exe"]
                and str(Path(proc.info["exe"]).resolve()).lower() == target_path
            ):
                pid = proc.pid
                hwnds: list[int] = []

                def _enum(hwnd, hwnds_out):
                    tid, _ = win32process.GetWindowThreadProcessId(hwnd)
                    if tid == pid and win32gui.IsWindowVisible(hwnd):
                        hwnds_out.append(hwnd)
                    return True

                win32gui.EnumWindows(_enum, hwnds)
                return hwnds[0] if hwnds else None
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    logger.warning("⚠️ Could not locate MT5 window.")
    return None


def move_and_resize_window(hwnd: int, x: int, y: int, width: int, height: int) -> None:
    """
    Move and resize a window using its handle.
    """
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.MoveWindow(hwnd, x, y, width, height, True)
    logger.success(f"📐 Window moved to ({x}, {y}, {width}, {height})")


def focus_window(hwnd: int) -> None:
    """
    Bring the MT5 window to the foreground using its handle.
    """
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        logger.info("🔎 MT5 window focused.")
    except Exception as e:
        logger.warning(f"⚠️ Could not focus window: {e}")


def apply_mt5_window_geometry(delay_seconds: int = 20) -> None:
    """
    Waits for MT5 to fully launch, then applies window position and size.
    """
    logger.info(f"🕓 Waiting {delay_seconds}s to reposition MT5...")
    time.sleep(delay_seconds)

    hwnd = find_mt5_window()
    geom = load_window_geometry()
    if hwnd and geom:
        x, y, w, h = geom
        move_and_resize_window(hwnd, x, y, w, h)
    else:
        logger.warning("❌ Could not apply geometry – missing window or config.")


def ensure_mt5_ready_for_automation() -> None:
    """
    Focuses MT5 and pauses briefly to ensure it's ready for UI actions.
    """
    hwnd = find_mt5_window()
    if hwnd:
        focus_window(hwnd)
        time.sleep(1.0)
