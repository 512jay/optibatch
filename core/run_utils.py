# File: core/run_utils.py

import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from loguru import logger
from core.state import registry
from windows.controller import apply_mt5_window_geometry
from core.job_context import JobContext


# ==========================
# MT5 Launching Utilities
# ==========================


def get_mt5_executable_path_from_registry() -> Path:
    """
    Reads 'install_path' from registry and appends 'terminal64.exe'.
    """
    base_path = Path(registry.get("install_path", "C:/MT5"))
    return base_path / "terminal64.exe"


def launch_mt5_with_ini(context: JobContext) -> None:
    """
    Launches MT5 with a specific INI config file and waits for it to finish.
    Raises RuntimeError if MT5 fails to start or finish properly.
    """
    ini_path = context.ini_file
    mt5_path = context.mt5_path
    log_path = context.log_path
    timeout = context.timeout or 300

    logger.info(f"🔧 Launching MT5 with INI: {ini_path}")
    logger.info(f"MT5 executable: {mt5_path}")
    logger.info(f"Expected log path: {log_path}")
    logger.info(f"Waiting timeout: {timeout} seconds")

    if not ini_path.exists():
        raise FileNotFoundError(f"❌ INI file not found: {ini_path}")
    if not mt5_path.exists():
        raise FileNotFoundError(f"❌ MT5 path not found: {mt5_path}")

    timestamp_before = datetime.datetime.now()

    # Launch MT5 subprocess
    subprocess.Popen(
        [str(mt5_path), f"/config:{ini_path}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Small delay to let MT5 open
    time.sleep(3)

    # Now monitor the logs
    success = wait_for_mt5_to_finish(
        timestamp_before=timestamp_before, timeout=timeout, log_path=log_path
    )

    if not success:
        raise RuntimeError("❌ MT5 optimization failed or skipped.")


def get_mt5_data_path(terminal_path: Path) -> Path | None:
    """
    Given the path to terminal64.exe, tries to locate the hashed MT5 data directory.
    Returns the path to the `tester/logs` directory, or None if not found.
    """
    install_dir = terminal_path.resolve()

    metaquotes_root = Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal"
    if not metaquotes_root.exists():
        return None

    for hash_dir in metaquotes_root.iterdir():
        if not hash_dir.is_dir():
            continue

        terminal_cfg = hash_dir / "origin.txt"
        if terminal_cfg.exists():
            try:
                content = terminal_cfg.read_text(encoding="utf-16").strip()
                if Path(content).resolve() == install_dir:
                    return hash_dir / "tester" / "logs"
            except Exception:
                continue

    return None


# ==========================
# Log Monitoring
# ==========================

def get_latest_log_path(log_folder: str | Path) -> Path | None:
    """
    Returns the most recently modified .log file in the given folder.
    Accepts a string or Path.
    """
    log_folder = Path(log_folder)  # ← Convert str to Path if needed

    log_files = sorted(
        log_folder.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True
    )

    return log_files[0] if log_files else None


def wait_for_mt5_to_finish(
    timestamp_before: datetime.datetime,
    timeout: int = 300,
    log_path: Optional[Path] = None,
) -> bool:
    """
    Monitor the MT5 tester logs for a completion marker after the given timestamp.
    Returns True if optimization finishes, False on timeout.
    """
    start_time = time.time()
    log_file = log_path or DEFAULT_MT5_LOG_PATH

    logger.info(f"🕵️ Monitoring MT5 log: {log_file}")

    while time.time() - start_time < timeout:
        time.sleep(2)
        if not log_file.exists():
            continue

        with open(log_file, "r", encoding="utf-16") as f:
            lines = f.readlines()

        recent_lines = [
            line for line in lines if is_after_timestamp(line, timestamp_before)
        ]

        for line in recent_lines:
            if "optimization finished" in line.lower():
                logger.info("✅ Optimization finished detected in logs.")
                return True
            if "optimization already processed" in line.lower():
                logger.info("⚠️ Optimization already processed detected.")
                return True

    logger.warning("⏳ Timeout reached without success marker in logs.")
    return False


# ==========================
# Run Management Utilities
# ==========================

from datetime import datetime
import shutil


def create_run_folder(ea_name: str) -> Path:
    """
    Creates a timestamped folder for a new run under 'generated/'.
    Returns the Path to the new run folder.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = Path("generated") / f"{timestamp}_{ea_name}"
    run_folder.mkdir(parents=True, exist_ok=True)
    return run_folder


def copy_core_files_to_run(run_folder: Path, ini_src: Path, json_src: Path) -> None:
    """
    Copies the core .ini and .json config files into the root of the run folder
    for reference or recordkeeping.
    """
    shutil.copy2(ini_src, run_folder / "current_config.ini")
    shutil.copy2(json_src, run_folder / "job_config.json")
