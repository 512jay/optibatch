# File: core/run_utils.py

import re
import subprocess
import time
from typing import Optional
from datetime import datetime
from pathlib import Path
from loguru import logger
from core.state import registry
from windows.controller import apply_mt5_window_geometry
from core.job_context import JobContext
import shutil

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
    log_dir = context.log_dir
    log_path = get_latest_log_path(log_dir)

    timeout = 3000

    logger.info(f"🔧 Launching MT5 with INI: {ini_path}")
    logger.info(f"MT5 executable: {mt5_path}")
    logger.info(f"Expected log path: {log_path}")
    logger.info(f"Waiting timeout: {timeout} seconds")

    if not ini_path.exists():
        raise FileNotFoundError(f"❌ INI file not found: {ini_path}")
    if not mt5_path.exists():
        raise FileNotFoundError(f"❌ MT5 path not found: {mt5_path}")

    timestamp_before = datetime.now()

    # Launch MT5 subprocess
    subprocess.Popen(
        [str(mt5_path), f"/config:{ini_path}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Small delay to let MT5 open
    time.sleep(3)

    # Now monitor the logs
    success = wait_for_mt5_to_finish(context, timeout=timeout)

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
    context: JobContext,
    timeout: int = 3000,
) -> bool:
    """
    Monitors MT5 log file for success markers, using the context's log_dir.
    """
    log_path = get_latest_log_path(context.log_dir)
    if not log_path:
        raise FileNotFoundError("❌ Could not locate latest .log file in log_dir.")

    timestamp_before = context.timestamp_before
    start_time = time.time()
    seen_lines = set()

    logger.info(f"🕵️ Monitoring MT5 log: {log_path}")

    while time.time() - start_time < timeout:
        time.sleep(2)

        if not log_path.exists():
            continue

        mtime = datetime.fromtimestamp(log_path.stat().st_mtime)
        if mtime <= timestamp_before:
            continue

        with open(log_path, "r", encoding="utf-16") as f:
            lines = f.readlines()

        for line in lines:
            if line in seen_lines:
                continue
            seen_lines.add(line)

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
