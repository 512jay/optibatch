# file: optibatch/windows/controller.py
# Controls the MT5 window geometry and focus based on process path
# Ensures correct automation setup (e.g., right-click coordinates are valid)

import time
import json
import psutil
import fnmatch
import win32gui  # type: ignore
import win32con  # type: ignore
import win32process  # type: ignore
from pathlib import Path
from typing import Optional, Tuple
from loguru import logger
from core.state import registry
from typing import Optional


MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 2

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
    Locate the MT5 window handle by matching the process path with the registry's terminal_path.
    Retries for a few seconds if the window is not immediately visible.
    Returns the window handle (HWND) or None if not found.
    """
    terminal_path = registry.get("install_path")
    if not terminal_path:
        logger.warning("❌ No MT5 path found in registry.")
        return None

    # Normalize path for comparison
    normalized_target_path = str(Path(terminal_path).resolve()).lower()

    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            if proc.info["name"] == "terminal64.exe":
                exe_path = str(Path(proc.info["exe"]).resolve()).lower()
                if normalized_target_path in exe_path:
                    pid = proc.info["pid"]

                    for attempt in range(1, MAX_RETRIES + 1):
                        hwnds: list[int] = []

                        def callback(hwnd, hwnds_list):
                            tid, current_pid = win32process.GetWindowThreadProcessId(
                                hwnd
                            )
                            if current_pid == pid and win32gui.IsWindowVisible(hwnd):
                                hwnds_list.append(hwnd)

                        win32gui.EnumWindows(callback, hwnds)

                        if hwnds:
                            return hwnds[0]  # Return the first visible window handle

                        logger.debug(
                            f"⏳ Retry {attempt}: No visible window found yet. Sleeping {RETRY_DELAY_SECONDS}s"
                        )
                        time.sleep(RETRY_DELAY_SECONDS)

                    logger.warning("⚠️ Could not locate MT5 window after retries.")
                    return None
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    logger.warning("⚠️ No MT5 process found matching terminal_path.")
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
    except Exception as e:
        logger.warning(f"⚠️ Could not focus window: {e}")


def apply_mt5_window_geometry(delay_seconds: int = 0) -> None:
    """
    Waits for MT5 to fully launch, then applies window position and size.
    """
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


def close_mt5_report_window() -> None:
    """
    Attempts to close the XML report viewer window opened by MT5,
    without affecting other applications.
    Looks for windows with *.xml or 'report' in the title.
    """

    def enum_handler(hwnd: int, windows_to_close: list[int]) -> None:
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if fnmatch.fnmatch(title.lower(), "*.xml") or "report" in title.lower():
                windows_to_close.append(hwnd)

    windows_to_close: list[int] = []
    win32gui.EnumWindows(enum_handler, windows_to_close)

    for hwnd in windows_to_close:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        logger.info(f"🔐 Closed report window: {win32gui.GetWindowText(hwnd)}")
