# File: core/logging/logger.py

from loguru import logger
from pathlib import Path
from typing import Optional

# === Global Logger Setup ===

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.add(
    LOG_DIR / "optibach.log",
    rotation="1 MB",       # Rotate after 1MB
    retention="7 days",    # Keep logs for 1 week
    compression="zip",     # Archive old logs
    level="INFO",          # Default logging level
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
)

# Logs are written to both the global log file and any active job-specific log sinks.
# Use `start_run_logger()` and `stop_run_logger()` to enable job-specific logging.

# === Job-Specific Logger Sink ===

def start_run_logger(run_folder: Path) -> int:
    '''
    Adds a dedicated log sink that writes logs live to this run folder.
    Returns the sink ID so it can be removed later.
    '''
    log_file = run_folder / f"{run_folder.name}.log"
    sink_id = logger.add(
        log_file,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
    )
    logger.debug(f"Started job logger: {log_file}")
    return sink_id


def stop_run_logger(sink_id: Optional[int]) -> None:
    '''
    Removes a previously added job-specific sink.
    '''
    if sink_id is not None:
        logger.remove(sink_id)
        logger.debug(f"Stopped job logger: sink {sink_id}")
