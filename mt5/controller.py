import json
import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple

import psutil
import win32con  # type: ignore
import win32gui  # type: ignore
import win32process  # type: ignore
from loguru import logger
from core.state import registry
from core.types import WindowGeometry


def launch_mt5(mt5_path: Path, ini_file: Path):
    """
    Launch MT5 from a specific installed path with a given .ini config file.
    This function assumes installed (non-portable) mode.
    """
    terminal = mt5_path / "terminal64.exe"
    if not terminal.exists():
        raise FileNotFoundError(f"MT5 terminal not found at: {terminal}")

    ini_path = ini_file.resolve()
    cmd = [str(terminal), f"/config:{ini_path}"]

    logger.debug("Command parts:")
    for i, part in enumerate(cmd):
        logger.debug(f"[{i}] {repr(part)}")

    subprocess.Popen(cmd, cwd=str(mt5_path))
    logger.info(f"Launched MT5 from: {terminal} with config {ini_file}")


def save_window_geometry(path: Path, geometry: WindowGeometry) -> None:
    if not geometry:
        return

    registry.set("window_geometry", geometry)
    registry.save()
    logger.info(f"Saved window geometry for {path}")


def load_window_geometry() -> Optional[WindowGeometry]:
    geometry = registry.get("window_geometry")
    if geometry:
        return geometry
    logger.warning("No saved window geometry found in app_state.json.")
    return None


def wait_for_mt5_window(mt5_path: Path, timeout: float = 20.0) -> Optional[int]:
    """Wait up to `timeout` seconds for the MT5 window to appear."""
    interval = 0.5
    elapsed = 0.0
    while elapsed < timeout:
        hwnd = _find_mt5_hwnd(mt5_path)
        if hwnd:
            return hwnd
        time.sleep(interval)
        elapsed += interval
    return None


def kill_mt5(mt5_path: Path):
    """Kill any MT5 process running from the specified install folder."""
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            if proc.info["name"].lower() == "terminal64.exe":
                exe_path = Path(proc.info["exe"]).resolve()
                if mt5_path in exe_path.parents:
                    logger.info(f"Killing MT5 process at: {exe_path}")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def is_mt5_running(mt5_path: Path) -> bool:
    """Check if MT5 is currently running from the specified install folder."""
    for proc in psutil.process_iter(["name", "exe"]):
        try:
            if proc.info["name"].lower() == "terminal64.exe":
                exe_path = Path(proc.info["exe"]).resolve()
                if mt5_path in exe_path.parents:
                    return True
        except Exception:
            continue
    return False


def focus_mt5(mt5_path: Path):
    """Bring the MT5 window to the front if launched from a specific install path."""
    hwnd = _find_mt5_hwnd(mt5_path)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        logger.info("MT5 window brought to front.")
    else:
        logger.warning("Could not find MT5 window to focus.")


def get_mt5_window_geometry(mt5_path: Path) -> Optional[WindowGeometry]:
    """Get the position and size of the MT5 window."""
    hwnd = _find_mt5_hwnd(mt5_path)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return WindowGeometry(
            x=rect[0],
            y=rect[1],
            width=rect[2] - rect[0],
            height=rect[3] - rect[1],
        )
    return None


def restore_mt5_window_position(mt5_path: Path) -> None:
    geometry = registry.get("window_geometry")
    if geometry:
        hwnd = _find_mt5_hwnd(mt5_path)
        if hwnd:
            win32gui.SetWindowPos(
                hwnd,
                0,
                geometry["x"],
                geometry["y"],
                geometry["width"],
                geometry["height"],
                0,
            )
            logger.info(f"Window restored to ({geometry['x']}, {geometry['y']})")
        else:
            logger.warning("Failed to find MT5 window.")
    else:
        logger.warning("No window geometry found in app_state.json.")


def get_click_position() -> Optional[Tuple[int, int]]:
    pos = registry.get("click_position")
    if pos and isinstance(pos, (list, tuple)) and len(pos) == 2:
        return int(pos[0]), int(pos[1])
    return None


def _find_mt5_hwnd(mt5_path: Path) -> Optional[int]:
    """Find the window handle for MT5 launched from the specified folder."""
    hwnd_target = None

    def enum_window_callback(hwnd, _):
        nonlocal hwnd_target
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                proc = psutil.Process(pid)
                exe_path = Path(proc.exe()).resolve()
                if (
                    mt5_path in exe_path.parents
                    and "terminal64.exe" in exe_path.name.lower()
                ):
                    hwnd_target = hwnd
            except Exception:
                pass

    win32gui.EnumWindows(enum_window_callback, None)
    return hwnd_target
