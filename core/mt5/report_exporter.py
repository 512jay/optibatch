import time
import shutil
import pyautogui
from pathlib import Path
from loguru import logger
from core.utils.io import read_utf16_file
from trash.config import config


def safe_right_click(x, y, retries=1):
    """Attempt to right-click safely, moving the mouse out of fail-safe zones if needed."""
    try:
        pyautogui.rightClick(x, y)
    except pyautogui.FailSafeException:
        logger.warning(
            "🛑 PyAutoGUI fail-safe triggered (mouse at corner). Attempting recovery..."
        )
        pyautogui.moveTo(x + 50, y + 50)  # Nudge the mouse out of danger zone
        time.sleep(0.5)
        if retries > 0:
            return safe_right_click(x, y, retries=retries - 1)
        else:
            logger.error("❌ Right-click failed after retry.")


# Default MT5 export directory
DEFAULT_MT5_EXPORT_DIR = Path.home() / "Documents" / "MetaTrader 5" / "Tester"


def export_mt5_results_to_xml(run_id: str, job_path: Path) -> list[Path]:
    logger.info("🔄 Exporting MT5 results to XML...")

    # Load job metadata from JSON file
    job_json = job_path / f"{job_path.name}.json"
    forward_mode = 0
    job_data = {}

    if job_json.exists():
        job_data = read_utf16_file(job_json)
        try:
            forward_mode = int(job_data.get("forward", {}).get("mode", 0))
        except Exception as e:
            logger.warning(f"⚠️ Could not determine forward mode: {e}")

    is_forward_enabled = forward_mode > 0

    # Extract details from job
    expert_path = job_data.get("expert", {}).get("path", "Unknown.ex5")
    ea_name = job_data.get("expert", {}).get("name", "UNKNOWN")
    symbol = job_data.get("symbols", ["UNKNOWN"])[0]
    start = job_data.get("date", {}).get("start", "0000.00.00").replace(".", "")
    end = job_data.get("date", {}).get("end", "0000.00.00").replace(".", "")

    output_dir = job_path
    output_dir.mkdir(parents=True, exist_ok=True)

    report_paths = []

    # Click coordinates for right-clicking in MT5
    x, y = config.get("report_click").values()

    # Export Optimization Report
    opt_filename = f"{ea_name}.{symbol}.H1.{start}_{end}.{run_id}.opt.xml"
    opt_report_temp = DEFAULT_MT5_EXPORT_DIR / opt_filename
    opt_report_final = output_dir / opt_filename

    logger.info(f"📤 Saving Optimization Report: {opt_filename}")

    safe_right_click(x, y)
    time.sleep(0.5)
    pyautogui.press(["down"] * (10 if is_forward_enabled else 9))
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite(opt_filename)
    pyautogui.press("enter")
    time.sleep(2)

    if opt_report_temp.exists():
        shutil.move(str(opt_report_temp), str(opt_report_final))
        close_auto_opened_report_window()
        report_paths.append(opt_report_final)
        logger.success(f"✅ Saved: {opt_report_final.name}")
    else:
        logger.warning("⚠️ Optimization report not found after export.")

    # Export Forward Report (if applicable)
    if is_forward_enabled:
        logger.info("🔁 Forward test detected, switching to forward tab...")
        safe_right_click(x, y)
        time.sleep(0.5)
        pyautogui.press(["down"] * 2)
        pyautogui.press("enter")
        time.sleep(1)

        fwd_filename = f"{ea_name}.{symbol}.H1.{start}_{end}.{run_id}.fwd.xml"
        fwd_report_temp = DEFAULT_MT5_EXPORT_DIR / fwd_filename
        fwd_report_final = output_dir / fwd_filename

        logger.info(f"📤 Saving Forward Report: {fwd_filename}")

        safe_right_click(x, y)
        time.sleep(0.5)
        pyautogui.press(["down"] * 10)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.typewrite(fwd_filename)
        pyautogui.press("enter")
        time.sleep(2)

        if fwd_report_temp.exists():
            shutil.move(str(fwd_report_temp), str(fwd_report_final))
            close_auto_opened_report_window()
            report_paths.append(fwd_report_final)
            logger.success(f"✅ Saved: {fwd_report_final.name}")
        else:
            logger.warning("⚠️ Forward report not found after export.")

    logger.info("✅ All reports exported successfully.")
    return report_paths


def close_auto_opened_report_window():
    """Close any report viewer that may have opened after export."""
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "w")
    time.sleep(0.5)
