# File: core/jobs_utils/runner.py

from tkinter import filedialog, messagebox
from pathlib import Path
import json
import subprocess
import psutil
import pyautogui
from core.mt5.report_exporter import export_mt5_results_to_xml
import time

from state.app_state import AppState
from core.jobs_utils.settings import load_settings
from ini_utils.formatter import generate_ini_files_from_job
from core.mt5.tester_log_monitor import wait_for_optimization_to_finish
from core.logging.logger import logger
from core.mt5.process import kill_mt5


def run_and_monitor_optimization(ini_file: Path, terminal_path: Path, job_path: Path):
    logger.info(f"Launching optimization for: {ini_file.name}")
    process = subprocess.Popen([str(terminal_path), f"/config:{ini_file}"])

    if wait_for_optimization_to_finish():
        logger.info(f"Optimization complete: {ini_file.name}")

        logger.info("📤 Exporting optimization results...")
        job_json = job_path / f"{job_path.name}.json"
        filename = export_mt5_results_to_xml(run_id=ini_file.stem, job_json_path=job_json)

        logger.info("Attempting to close MT5...")
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and "terminal64.exe" in proc.info["name"].lower():
                try:
                    proc.terminate()
                    proc.wait(timeout=10)
                    logger.info("MT5 closed successfully.")
                except psutil.TimeoutExpired:
                    logger.warning("MT5 did not close in time — forcing kill.")
                    proc.kill()

        time.sleep(2)
    else:
        logger.warning(f"Timeout while waiting on: {ini_file.name}")


def auto_resume_job(job_path: Path, terminal_path: Path):
    ini_files = generate_ini_files_from_job(job_path)
    logger.info(f"Preparing to run {len(ini_files)} optimization(s)")

    # ✅ Ensure MT5 is closed before any run
    kill_mt5()
    time.sleep(2) # Optional short delay for clean shutdown

    for ini in ini_files:
        run_and_monitor_optimization(ini, terminal_path, job_path)

    logger.info("All optimizations completed.")


def pick_and_resume_job():
    file_path = filedialog.askopenfilename(
        filetypes=[("Job Config", "*.json")],
        initialdir="jobs",
        title="Select a Job File",
    )
    if not file_path:
        return

    settings = load_settings()
    terminal_path = Path(settings.get("terminal_path", ""))

    if terminal_path.exists():
        auto_resume_job(Path(file_path), terminal_path)
    else:
        messagebox.showerror("Error", "Terminal path not found.")
