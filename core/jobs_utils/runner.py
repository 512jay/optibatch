# File: core/jobs_utils/runner.py

from tkinter import filedialog, messagebox
from pathlib import Path
import subprocess
import time
import psutil

from core.mt5.report_exporter import export_mt5_results_to_xml
from core.mt5.tester_log_monitor import wait_for_optimization_to_finish
from core.process import kill_mt5
from core.jobs_utils.settings import load_settings
from ini_utils.formatter import generate_ini_files_from_job
from core.logging.logger import logger


def run_and_monitor_optimization(ini_file: Path, terminal_path: Path, job_folder: Path):
    """
    Launches a single MT5 optimization, monitors it, exports results, then shuts down MT5.

    Args:
        ini_file (Path): The .ini config file to launch in MT5.
        terminal_path (Path): Path to terminal64.exe for launching MT5.
        job_folder (Path): Path to the folder where the job.json and XML reports should go.
    """
    logger.info(f"Launching optimization for: {ini_file.name}")

    # 🟢 Start MT5 with the provided config
    process = subprocess.Popen([str(terminal_path), f"/config:{ini_file}"])

    # ⏳ Wait for the MT5 optimization to complete
    if wait_for_optimization_to_finish():
        logger.info(f"Optimization complete: {ini_file.name}")

        logger.info("📤 Exporting optimization results...")

        # ✅ Export XML report(s) to the same folder as the job
        export_mt5_results_to_xml(run_id=ini_file.stem, job_path=job_folder)

        # 🔻 Attempt to close MT5 cleanly after export
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


def auto_resume_job(job_json_path: Path, terminal_path: Path):
    """
    Given a job JSON file, resume all optimization runs by:
    - Generating all INI files from the job
    - Running MT5 on each
    - Exporting results to the job folder

    Args:
        job_json_path (Path): Path to a job JSON (e.g., jobs/job_20250407_004.json)
        terminal_path (Path): Path to terminal64.exe
    """
    # 📂 Get the job folder: e.g., jobs/job_20250407_004/
    job_folder = job_json_path.parent

    # 🧠 Generate all the .ini files from the JSON spec
    ini_files = generate_ini_files_from_job(job_json_path)
    logger.info(f"Preparing to run {len(ini_files)} optimization(s)")

    # 🛑 Make sure MT5 isn't already running
    kill_mt5()
    time.sleep(2)  # Optional delay for full shutdown

    # ▶️ Run each optimization and export results
    for ini in ini_files:
        run_and_monitor_optimization(ini, terminal_path, job_folder)

    logger.info("All optimizations completed.")


def pick_and_resume_job():
    """
    GUI helper to allow user to select a job JSON file from file picker,
    and auto-resume it using MT5 and saved terminal path.
    """
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
