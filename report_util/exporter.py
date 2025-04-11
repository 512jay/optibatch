# file: optibatch/report_util/exporter.py
# Handles exporting MT5 optimization results via UI automation
# Supports cleanup and file relocation after export

import shutil
import time
from pathlib import Path
from typing import Optional
from loguru import logger
import pyautogui

from core.state import registry
from windows.controller import ensure_mt5_ready_for_automation
from report_util.cleaner import close_auto_opened_report_window

REPORTS_DIR = Path("generated") / "reports"
MT5_EXPORT_DIR = Path.home() / "Documents" / "MetaTrader 5" / "Tester"


def export_report(filename: str, click_position: tuple[int, int], delay: float = 0.5) -> Optional[Path]:
    """
    Triggers a right-click export of an optimization report from MT5 and moves it to the reports folder.

    Args:
        filename: Name of the report file to save.
        click_position: Tuple (x, y) where the right-click should occur in MT5.
        delay: Time to wait between actions (in seconds).

    Returns:
        Path to the moved report, or None if export failed.
    """
    logger.info(f"📤 Exporting MT5 report to {filename}")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_mt5_ready_for_automation()
    time.sleep(delay)

    x, y = click_position
    try:
        pyautogui.rightClick(x, y)
        time.sleep(delay)
        pyautogui.press(["down"] * 9)  # Navigate to "Export to XML"
        pyautogui.press("enter")
        time.sleep(delay)
        pyautogui.typewrite(filename)
        pyautogui.press("enter")
        time.sleep(2.0)  # Give MT5 time to write the file
    except pyautogui.FailSafeException:
        logger.error("🛑 Mouse in fail-safe position. Export aborted.")
        return None

    temp_file = MT5_EXPORT_DIR / filename
    final_file = REPORTS_DIR / filename

    if temp_file.exists():
        shutil.move(str(temp_file), str(final_file))
        logger.success(f"✅ Report saved: {final_file}")
        return final_file
    else:
        logger.warning("⚠️ Report file not found after export.")
        return None


