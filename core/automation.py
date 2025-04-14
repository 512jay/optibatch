# File: optibatch/core/automation.py

from loguru import logger
from core.process import kill_mt5
from core.run_utils import (
    launch_mt5_with_ini,
    wait_for_mt5_to_finish
)
from core.job_context import JobContext


def optimize_with_mt5(job: JobContext, timeout: int = 7200) -> bool:
    """
    Runs a single MT5 optimization job using the provided JobContext.
    Ensures MT5 is not running before starting.
    Waits for 'optimization finished' or 'already processed' in the log.
    Returns True if successful, False on timeout or failure.
    """
    kill_mt5(str(job.mt5_path))

    launch_mt5_with_ini(job)

    logger.info(f"Waiting for MT5 to finish: {job.ini_file.name}")
    success = wait_for_mt5_to_finish(
        log_dir=job.log_dir, timestamp_before=job.timestamp_before, timeout=timeout
    )

    if success:
        logger.success(f"MT5 optimization completed: {job.ini_file.name}")
    else:
        logger.error(f"MT5 optimization timeout/failure: {job.ini_file.name}")

    return success
