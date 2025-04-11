# file: optibatch/report_util/cleaner.py
# Handles cleanup tasks related to report files (e.g., deleting XML exports)

import shutil
from pathlib import Path
from loguru import logger

REPORTS_DIR = Path("generated") / "reports"


def empty_reports_folder() -> None:
    """
    Deletes only .xml files in the reports directory.
    Preserves other files and folders.
    """
    if REPORTS_DIR.exists():
        deleted = 0
        for item in REPORTS_DIR.iterdir():
            try:
                if item.is_file() and item.suffix.lower() == ".xml":
                    item.unlink()
                    deleted += 1
            except Exception as e:
                logger.warning(f"⚠️ Failed to delete {item}: {e}")
        logger.info(f"🧹 Deleted {deleted} .xml file(s) from {REPORTS_DIR}")
    else:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Created missing reports folder at {REPORTS_DIR}")

import pyautogui
import time
from loguru import logger


def close_auto_opened_report_window() -> None:
    """
    Attempts to close the report viewer window that may open after export.
    Uses Ctrl+W, which is a common 'close window' shortcut.
    """
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "w")
    logger.info("🔐 Sent Ctrl+W to close any auto-opened report window.")
    time.sleep(0.3)
