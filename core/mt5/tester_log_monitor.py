# core/mt5/tester_log_monitor.py

from datetime import datetime, time as dt_time
from pathlib import Path
from typing import List, Tuple, Optional
import time as systime
from core.logging.logger import logger
from core.jobs_utils.settings import load_settings


def get_latest_log(log_dir: Path) -> Optional[Path]:
    files = list(log_dir.glob("*.log"))
    return max(files, key=lambda f: f.stat().st_mtime) if files else None


def read_log_utf16(path: Path) -> List[Tuple[dt_time, str]]:
    parsed_lines = []
    with open(path, encoding="utf-16-le", errors="ignore") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                try:
                    log_time = datetime.strptime(parts[2][:8], "%H:%M:%S").time()
                    parsed_lines.append((log_time, line.strip()))
                except ValueError:
                    continue
    return parsed_lines


def get_last_log_timestamp(path: Path) -> Optional[dt_time]:
    lines = read_log_utf16(path)
    return lines[-1][0] if lines else None


def log_contains(path: Path, keyword: str) -> bool:
    with open(path, encoding="utf-16-le", errors="ignore") as f:
        return any(keyword in line for line in f)


def filter_log_by_keyword(path: Path, keyword: str) -> List[Tuple[dt_time, str]]:
    return [(t, line) for t, line in read_log_utf16(path) if keyword in line]


def wait_for_optimization_to_finish(inactivity_timeout_seconds=900) -> bool:
    """
    Waits until the MT5 tester log contains 'optimization finished' or 'already processed'.
    Timeout only occurs if NO NEW log entries appear for `inactivity_timeout_seconds`.

    Returns:
        bool: True if optimization finished, False if log went silent too long.
    """
    settings = load_settings()
    data_path = Path(settings.get("data_path", ""))
    log_dir = data_path / "tester" / "logs"

    if not log_dir.exists():
        logger.error(f"Tester log path does not exist: {log_dir}")
        return False

    log_path = get_latest_log(log_dir)
    if not log_path:
        logger.error("No tester log file found.")
        return False

    logger.info(f"Monitoring tester log: {log_path.name}")
    last_seen_time = get_last_log_timestamp(log_path)
    logger.debug(f"Last known timestamp before run: {last_seen_time}")

    seen_lines = set()
    last_activity_time = systime.time()

    while True:
        new_lines = read_log_utf16(log_path)
        new_content_found = False

        for log_time, line in new_lines:
            if last_seen_time and log_time <= last_seen_time:
                continue
            if line not in seen_lines:
                seen_lines.add(line)
                new_content_found = True
                if (
                    "optimization finished" in line.lower()
                    or "optimization already processed" in line.lower()
                ):
                    logger.success("Optimization finished successfully.")
                    return True

        if new_content_found:
            last_activity_time = systime.time()

        if systime.time() - last_activity_time > inactivity_timeout_seconds:
            logger.warning("Timeout: No new log entries detected.")
            return False

        systime.sleep(2)
