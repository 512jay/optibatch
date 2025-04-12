# File: report_util/grabber.py

from __future__ import annotations

import time
import pyautogui
import shutil
from pathlib import Path
from core.state import registry
from windows.controller import apply_mt5_window_geometry, find_mt5_window, close_mt5_report_window
from core.job_context import JobContext
from loguru import logger


REPORTS_DIR = Path.cwd() / "reports"


def move_xml_to_job_folder(context: JobContext) -> Path:
    """
    Moves the XML report from the shared reports folder (REPORTS_DIR)
    to the final job-specific folder alongside the .ini file.
    Returns the new destination path.
    """
    src = REPORTS_DIR / f"{context.basename}.xml"
    dst = context.final_xml_path
    dst.parent.mkdir(parents=True, exist_ok=True)

    if src.exists():
        shutil.move(src, dst)
        logger.success(f"📂 Moved report: {src.name} → {dst}")
    else:
        logger.warning(f"⚠️ Expected XML not found in {REPORTS_DIR}: {src.name}")

    return dst


def clean_orphaned_reports() -> int:
    """
    Deletes any leftover .xml files in the shared reports folder
    that were not moved after export.
    Returns the number of files deleted.
    """
    deleted = 0
    for file in REPORTS_DIR.glob("*.xml"):
        try:
            file.unlink()
            deleted += 1
        except Exception as e:
            logger.warning(f"⚠️ Failed to delete {file.name}: {e}")
    logger.info(f"🧽 Cleaned up {deleted} orphaned report(s) in {REPORTS_DIR}")
    return deleted


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


def handle_save_dialog(context: JobContext) -> None:
    """
    Handles the Windows Save dialog: types only the base filename (no path or extension) and confirms save.
    """
    filename = context.basename
    logger.info(f"Typing XML save filename: {filename}")

    time.sleep(1.2)  # ⏱️ Wait for the Save dialog to be ready (tweak if still flaky)
    pyautogui.write(filename, interval=0.02)
    pyautogui.press("enter")
    time.sleep(1)


def confirm_export_success(context: JobContext, timeout: int = 10) -> bool:
    expected_path = REPORTS_DIR / f"{context.basename}.xml"
    logger.debug(f"Waiting for XML report to be saved: {expected_path}")

    for _ in range(timeout * 2):
        if expected_path.exists() and expected_path.stat().st_size > 0:
            logger.info(f"✅ XML report saved: {expected_path}")
            return True
        time.sleep(0.5)

    # 👇 Add fallback sanity log
    logger.warning(f"❌ XML report not found after {timeout}s: {expected_path}")
    if REPORTS_DIR.exists():
        existing = list(REPORTS_DIR.glob("*.xml"))
        if existing:
            logger.warning(
                "⚠️ XML files found in reports dir (but didn't match expected):"
            )
            for f in existing:
                logger.warning(f" - {f.name}")

    return False


def export_and_confirm_xml(context: JobContext) -> bool:
    export_xml_via_context_menu()
    handle_save_dialog(context)

    if confirm_export_success(context):
        move_xml_to_job_folder(context)
        time.sleep(1.5)  # ⏱ give the viewer time to open
        close_mt5_report_window()
        return True

    return False
