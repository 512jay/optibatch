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


def launch_mt5_with_ini(context: JobContext, delay: int = 5) -> None:
    """
    Launches MT5 with the given JobContext's .ini file, and waits for log signal.
    """
    if not context.mt5_path.exists():
        raise FileNotFoundError(f"MT5 executable not found: {context.mt5_path}")
    if not context.ini_file.exists():
        raise FileNotFoundError(f"INI file not found: {context.ini_file}")

    logger.debug(f"Launching MT5: {context.mt5_path} /config:{context.ini_file}")
    subprocess.Popen([str(context.mt5_path), f"/config:{str(context.ini_file)}"])

    logger.debug(f"Waiting {delay} seconds for MT5 to launch...")
    time.sleep(delay)

    success = wait_for_mt5_to_finish(
        log_dir=context.log_dir, timestamp_before=context.timestamp_before
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


def wait_for_mt5_to_finish(log_dir: Path, *, timestamp_before: datetime, timeout: float = 60.0) -> bool:
    """
    Waits for MT5 to finish optimization by watching log files.
    Only considers logs modified after timestamp_before.
    """
    start_time = time.time()
    seen_finish = False
    seen_already_processed = False

    def get_recent_logs():
        return [
            f for f in sorted(log_dir.glob("*.log"), reverse=True)
            if f.stat().st_mtime > timestamp_before.timestamp()
        ]

    logger.debug(f"⏳ Watching MT5 tester logs in: {log_dir}")

    while time.time() - start_time < timeout:
        fresh_logs = get_recent_logs()
        if not fresh_logs:
            time.sleep(1)
            continue

        for log_file in fresh_logs:
            try:
                lines = log_file.read_text(encoding="utf-16", errors="ignore").splitlines()
            except Exception as e:
                logger.warning(f"⚠️ Could not read {log_file.name}: {e}")
                continue

            for line in lines:
                if "optimization finished" in line.lower():
                    seen_finish = True
                    break
                if "optimization already processed" in line.lower():
                    seen_already_processed = True
                    break

            if seen_finish or seen_already_processed:
                break

        if seen_finish or seen_already_processed:
            break

        time.sleep(1)

    if seen_finish:
        logger.success("✅ MT5 log indicates optimization finished.")
        return True
    if seen_already_processed:
        logger.warning("⚠️ MT5 skipped optimization (already processed). Consider clearing .opt file.")
        return False

    logger.error("❌ Timeout waiting for MT5 optimization to finish.")
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
