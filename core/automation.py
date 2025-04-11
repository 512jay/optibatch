# File: optibatch/core/automation.py

from pathlib import Path
from datetime import datetime
from loguru import logger
from core.process import kill_mt5
from core.run_utils import (
    launch_mt5_with_ini,
    wait_for_mt5_to_finish
)

def optimize_with_mt5(
    ini_file: Path,
    mt5_path: Path,
    log_path: Path,
    timeout: int = 7200
) -> bool:
    """
    Runs a single MT5 optimization job using the provided INI file.
    Ensures MT5 is not running before starting.
    Waits for 'optimization finished' or 'already processed' in the log.
    Returns True if successful, False on timeout or failure.
    """
    kill_mt5(str(mt5_path))

    launch_mt5_with_ini(ini_file, mt5_path)

    logger.info(f"Waiting for MT5 to finish: {ini_file.name}")
    success = wait_for_mt5_to_finish(timeout=timeout)

    # kill_mt5(str(mt5_path))

    if success:
        logger.success(f"MT5 optimization completed: {ini_file.name}")
    else:
        logger.error(f"MT5 optimization timeout/failure: {ini_file.name}")

    return success
