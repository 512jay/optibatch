# File: core/run_utils.py

import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

from loguru import logger

from core.state import registry
from windows.controller import apply_mt5_window_geometry

# ==========================
# MT5 Launching Utilities
# ==========================


def get_mt5_executable_path_from_registry() -> Path:
    """
    Reads 'install_path' from registry and appends 'terminal64.exe'.
    """
    base_path = Path(registry.get("install_path", "C:/MT5"))
    return base_path / "terminal64.exe"


def launch_mt5_with_ini(ini_file: Path, mt5_path: Path, delay: int = 5) -> None:
    """
    Launches MetaTrader 5 with the given INI file using subprocess.
    Expects mt5_path to point to terminal64.exe.
    """

    if not mt5_path.exists():
        raise FileNotFoundError(f"MT5 executable not found: {mt5_path}")
    if not ini_file.exists():
        raise FileNotFoundError(f"INI file not found: {ini_file}")

    logger.debug(f"Launching MT5: {mt5_path} /config:{ini_file}")
    subprocess.Popen([str(mt5_path), f"/config:{str(ini_file)}"])
    wait_for_mt5_to_finish()
    

    logger.debug(f"Waiting {delay} seconds for MT5 to launch...")
    time.sleep(delay)


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


def wait_for_mt5_to_finish(timeout: int = 300) -> bool:
    """
    Watches MT5 tester logs for 'optimization finished' or 'optimization already processed'.
    Returns True if either phrase is detected within the timeout.
    """
    apply_mt5_window_geometry()
    log_dir = Path(registry.get("tester_log_path"))
    deadline = time.time() + timeout
    seen_lines = set()
    keywords = ("optimization finished", "optimization already processed")

    logger.debug(f"⏳ Watching MT5 tester logs in: {log_dir}")

    while time.time() < deadline:
        logs = sorted(
            log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True
        )
        if not logs:
            logger.debug("📭 No log files found yet.")
            time.sleep(1)
            continue

        latest_log = logs[0]
        logger.debug(f"📄 Scanning latest log file: {latest_log.name}")

        try:
            with latest_log.open(encoding="utf-16") as f:
                for line in f:
                    if line in seen_lines:
                        continue
                    seen_lines.add(line)

                    if any(k in line.lower() for k in keywords):
                        logger.success(f"🟢 MT5 log line detected: {line.strip()}")
                        return True
        except Exception as e:
            logger.warning(f"⚠️ Error reading log file {latest_log.name}: {e}")

        time.sleep(2)

    logger.error("❌ MT5 optimization not detected within timeout.")
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
