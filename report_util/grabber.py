# File: report_util/grabber.py

from __future__ import annotations

import time
import logging
import pyautogui
from pathlib import Path
from report_util.cleaner import REPORTS_DIR
from core.state import registry
from windows.controller import apply_mt5_window_geometry, find_mt5_window

logger = logging.getLogger(__name__)


def export_xml_via_context_menu() -> bool:
    """
    Brings MT5 to the foreground, applies window geometry,
    moves to the saved click_offset (or absolute click_position),
    right-clicks, and navigates the context menu to trigger 'Export XML'.
    """
    if not find_mt5_window():
        logger.error("Failed to bring MT5 to front.")
        return False

    apply_mt5_window_geometry()

    geometry = registry.get("window_geometry")
    offset = registry.get("click_offset")
    if geometry and offset and isinstance(offset, list) and len(offset) == 2:
        x = geometry["x"] + offset[0]
        y = geometry["y"] + offset[1]
        logger.info(f"Using relative click offset: ({offset[0]}, {offset[1]})")
    else:
        pos = registry.get("click_position")
        if not pos or not isinstance(pos, list) or len(pos) != 2:
            logger.error("No valid click_offset or click_position found in app state.")
            return False
        x, y = pos
        logger.warning("Using legacy absolute click_position fallback.")

    logger.info(f"Exporting XML from position ({x}, {y})...")
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.rightClick()
    time.sleep(0.5)

    for _ in range(9):
        pyautogui.press("down")
    time.sleep(0.2)
    pyautogui.press("enter")

    logger.info("Triggered XML export via context menu.")
    return True


def get_current_xml_path() -> Path:
    """
    Returns the expected XML file path for the currently running optimization,
    based on 'last_job_name' and 'current_basename' in app_state.
    """
    job_name = registry.get("last_job_name")
    basename = registry.get("current_basename")

    if not job_name or not basename:
        raise ValueError("Missing 'last_job_name' or 'current_basename' in app state.")

    symbol = basename.split(".", 1)[0]
    return Path("generated") / job_name / symbol / f"{basename}.xml"


def handle_save_dialog(destination: Path) -> None:
    """
    Handles the Windows Save dialog: types only the base filename (no path or extension) and confirms save.
    """
    filename = destination.stem
    logger.info(f"Typing XML save filename: {filename}")

    time.sleep(1.2)  # ⏱️ Wait for the Save dialog to be ready (tweak if still flaky)
    pyautogui.write(filename, interval=0.02)
    pyautogui.press("enter")
    time.sleep(1)


def confirm_export_success(timeout: int = 10) -> bool:
    """
    Confirms that the expected XML file was saved successfully.
    Waits up to `timeout` seconds for the file to appear.
    """
    expected_path = get_current_xml_path()
    logger.debug(f"Waiting for XML report to be saved: {expected_path}")

    for _ in range(timeout * 2):
        if expected_path.exists() and expected_path.stat().st_size > 0:
            logger.info(f"\u2705 XML report saved: {expected_path}")
            return True
        time.sleep(0.5)

    logger.warning(f"\u274c XML report not found after {timeout}s: {expected_path}")
    return False


def export_and_confirm_xml() -> bool:
    """
    Full export flow:
    1. Brings MT5 to front and applies window geometry
    2. Right-clicks to trigger 'Export XML'
    3. Handles the Save dialog with the expected path
    4. Waits for the XML file to be written and confirms success

    Returns True if export was successful, False otherwise.
    """
    export_xml_via_context_menu()
    handle_save_dialog(get_current_xml_path())
    return confirm_export_success()
