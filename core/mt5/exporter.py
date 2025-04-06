import os
import time
from datetime import datetime
import pyautogui
from core.logging.logger import logger


def export_mt5_results_to_xml(x, y, output_folder="exports") -> str:
    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{timestamp}.xml"
    full_path = os.path.abspath(os.path.join(output_folder, filename))

    logger.info(f"🚀 Exporting MT5 results to: {full_path}")
    logger.info("🧭 Switching to MT5 window...")

    pyautogui.hotkey("alt", "tab")
    time.sleep(2)

    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.rightClick()
    time.sleep(0.5)

    for _ in range(9):  # Adjust if menu structure changes
        pyautogui.press("down")
    time.sleep(0.2)
    pyautogui.press("enter")

    time.sleep(2)
    pyautogui.write(full_path)
    pyautogui.press("enter")

    logger.success("📄 Export complete.")
    return full_path
