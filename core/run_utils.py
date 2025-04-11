# File: core/run_utils.py

import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

from loguru import logger

from core.state import registry


# ==========================
# MT5 Launching Utilities
# ==========================


def get_mt5_executable_path_from_registry() -> Path:
    """
    Reads 'install_path' from registry and appends 'terminal64.exe'.
    """
    base_path = Path(registry.get("install_path", "C:/MT5"))
    return base_path / "terminal64.exe"



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


def get_latest_log_timestamp(log_folder: Path) -> datetime | None:
    latest_log = get_latest_log_path(log_folder)
    if not latest_log:
        return None

    timestamp_pattern = re.compile(r"^(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})")
    last_timestamp = None

    with latest_log.open(encoding="utf-16") as f:
        for line in f:
            match = timestamp_pattern.match(line)
            if match:
                try:
                    last_timestamp = datetime.strptime(
                        match.group(1), "%Y.%m.%d %H:%M:%S"
                    )
                except ValueError:
                    continue

    return last_timestamp


def wait_for_mt5_to_finish(after: datetime, timeout: int = 300) -> bool:
    """
    Watches MT5 tester logs for 'optimization finished' or 'already processed'
    lines that appear *after* the given timestamp.
    Returns True if successful, False if timeout.
    """
    log_dir = Path(registry.get("tester_log_path"))
    deadline = time.time() + timeout
    seen_lines = set()
    pattern = re.compile(
        r"^(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*?(optimization finished|optimization already processed)"
    )

    logger.debug(f"Waiting for MT5 log activity after: {after}")
    logger.debug(f"Monitoring log folder: {log_dir}")

    while time.time() < deadline:
        logs = sorted(
            log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True
        )
        if not logs:
            logger.debug("No log files found.")
            time.sleep(1)
            continue

        latest_log = logs[0]
        #  logger.debug(f"Scanning log file: {latest_log.name}")

        try:
            with latest_log.open(encoding="utf-16") as f:
                for line in f:
                    if line in seen_lines:
                        continue
                    seen_lines.add(line)

                    match = pattern.match(line)
                    if match:
                        log_time = datetime.strptime(
                            match.group(1), "%Y.%m.%d %H:%M:%S"
                        )
                        logger.debug(f"Found log entry: {match.group(2)} at {log_time}")
                        if log_time > after:
                            logger.debug(
                                "Log line is newer than launch time — assuming MT5 ran successfully."
                            )
                            return True
        except Exception as e:
            logger.warning(f"Error reading log: {e}")

        time.sleep(2)

    logger.error("MT5 optimization log not found or did not complete in time.")
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
    shutil.copy2(json_src, run_folder / "current_config.json")
