# core/mt5/report_exporter.py

import time
import pyautogui
import pygetwindow as gw
from loguru import logger
from pathlib import Path
from core.config import config
from core.jobs_utils.forward_utils import get_forward_split_date, is_forward_enabled
from core.utils.io import read_utf16_file


def focus_mt5_window():
    logger.info("🔍 Looking for MT5 window using EA name...")

    expert_path = config.get("terminal_path")  # Or wherever the EA path is stored
    ea_name = (
        Path(config.get("expert_path")).stem if config.get("expert_path") else "IndyTSL"
    )

    logger.debug(f"🔎 Searching for window containing EA name: {ea_name}")

    candidates = [
        w
        for w in gw.getAllWindows()
        if w.visible
        and ea_name.lower() in w.title.lower()
        and not w.title.lower().endswith(".xml")
    ]

    if not candidates:
        logger.warning("⚠️ MT5 window with EA name not found!")
        return False

    win = candidates[0]
    win.activate()
    logger.success(f"🟢 Focused MT5 window: '{win.title}'")
    time.sleep(1)
    return True


def export_one_report(
    run_id: str, x: int, y: int, suffix: str = "", press_count: int = 9
):
    full_id = f"{run_id}.{suffix}" if suffix else run_id
    logger.info(f"🧾 Saving report: {full_id}.xml")

    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.rightClick()
    time.sleep(0.5)

    logger.info(f"Press count: {press_count}")
    for _ in range(press_count):
        pyautogui.press("down")
    pyautogui.press("enter")

    time.sleep(1.5)
    pyautogui.write(full_id)
    pyautogui.press("enter")
    time.sleep(1)

    close_auto_opened_report_window()
    logger.success(f"✅ Report saved: {full_id}.xml")


def close_auto_opened_report_window():
    for win in gw.getWindowsWithTitle(".xml"):
        if win.visible:
            win.close()
            time.sleep(0.5)


def export_mt5_results_to_xml(run_id: str, job_json_path: Path):
    logger.info("🔄 Exporting MT5 results to XML...")

    forward_enabled = is_forward_enabled(job_json_path)

    presses_to_report = 10 if is_forward else 9

    report_click = config.get("report_click")
    x, y = report_click["x"], report_click["y"]
    logger.info(f"📤 Exporting MT5 results to XML using point ({x}, {y})")

    focus_mt5_window()
    export_one_report(run_id, x, y, suffix="opt", press_count=presses_to_report)
    time.sleep(0.5)
    close_auto_opened_report_window()
    time.sleep(0.5)

    if forward_enabled:
        logger.info("🔄 Exporting forward test results...")
        focus_mt5_window()
        pyautogui.press("down")  # switch to forward test result
        # pyautogui.press("down")
        pyautogui.press("enter")
        time.sleep(0.2)
        export_one_report(run_id, x, y, suffix="fwd", press_count=presses_to_report)
        time.sleep(0.5)
        close_auto_opened_report_window()
        time.sleep(0.5)

    logger.info("✅ All reports exported successfully.")
