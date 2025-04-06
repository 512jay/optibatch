# File: core/mt5/report_exporter.py

import time
import pyautogui
import pygetwindow as gw
from loguru import logger
from core.config import config


def close_auto_opened_report_window():
    time.sleep(2)  # Give it a moment to open

    candidates = [
        w
        for w in gw.getAllWindows()
        if w.visible
        and any(
            phrase in w.title.lower()
            for phrase in ("file://", "chrome", "edge", "notepad", ".xml")
        )
    ]

    if not candidates:
        logger.info("✅ No auto-opened report window to close.")
        return

    for w in candidates:
        try:
            logger.warning(f"🧹 Auto-closing window: {w.title}")
            w.activate()
            time.sleep(0.3)
            pyautogui.hotkey("alt", "f4")
            break
        except Exception as e:
            logger.error(f"⚠️ Failed to close window: {e}")


def focus_mt5_window() -> bool:
    logger.info("🔍 Looking for MT5 window...")

    windows = gw.getAllWindows()
    candidates = [
        w
        for w in windows
        if w.visible
        and "Deriv" in w.title
        and ("Strategy Tester" in w.title or "IndyTSL" in w.title)
    ]

    if not candidates:
        logger.warning("⚠️ MetaTrader 5 window not found!")
        return False

    mt5_window = candidates[0]
    mt5_window.activate()
    logger.success(f"🪟 Focused MT5 window: '{mt5_window.title}'")
    return True


def export_mt5_results_to_xml(run_id: str = None):
    """Triggers MT5 right-click and Export to XML using saved coordinates."""
    # 🔍 Get coordinates from config
    click = config.get("report_click", {})
    x = click.get("x")
    y = click.get("y")

    if x is None or y is None:
        logger.error("❌ Report click coordinates not set in settings.json.")
        return

    logger.info(f"📤 Exporting MT5 results to XML using point ({x}, {y})")

    if not focus_mt5_window():
        return

    # 🖱️ Right-click report area
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.rightClick()
    time.sleep(0.6)

    # ⬇ Navigate to "Export to XML"
    for _ in range(9):
        pyautogui.press("down")
        time.sleep(0.1)
    pyautogui.press("enter")

    time.sleep(2)

    # 📝 Type custom filename if provided
    if run_id:
        pyautogui.write(run_id)
        pyautogui.press("enter")
        logger.success(f"✅ Report saved as: {run_id}.xml")
    else:
        logger.info("🗂️ Saved with default filename.")
    time.sleep(1)
    # 🧹 Close any auto-opened report window
    close_auto_opened_report_window()
