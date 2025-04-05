# core/log/log_utils.py
# # core/log/log_utils.py
#
# Purpose: Utility functions for handling log files, including reading, filtering, and checking contents.   

from datetime import datetime, time
from pathlib import Path
from typing import List, Tuple, Optional


def get_latest_log(log_dir: Path) -> Optional[Path]:
    """
    Finds and returns the most recently modified .log file in a directory.

    Args:
        log_dir (Path): Directory to search for log files.

    Returns:
        Optional[Path]: Path to the latest .log file, or None if no .log files are found.
    """
    files = list(log_dir.glob("*.log"))
    return max(files, key=lambda f: f.stat().st_mtime) if files else None


def read_log_utf16(path: Path) -> List[Tuple[time, str]]:
    """
    Reads a UTF-16 encoded log file and extracts time-stamped lines.

    Each line is expected to be tab-separated, with the 3rd field containing
    a timestamp like 'HH:MM:SS.fff'.

    Args:
        path (Path): Path to the log file.

    Returns:
        List[Tuple[time, str]]: List of (log time, full line) tuples.
    """
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


def get_last_log_timestamp(path: Path) -> Optional[time]:
    """
    Gets the last timestamp recorded in a UTF-16 log file.

    Args:
        path (Path): Path to the log file.

    Returns:
        Optional[time]: The last time found in the log, or None if no valid time is found.
    """
    lines = read_log_utf16(path)
    return lines[-1][0] if lines else None


def log_contains(path: Path, keyword: str) -> bool:
    """
    Checks whether the log contains a given keyword.

    Args:
        path (Path): Path to the log file.
        keyword (str): Substring to search for.

    Returns:
        bool: True if any line contains the keyword, else False.
    """
    with open(path, encoding="utf-16-le", errors="ignore") as f:
        return any(keyword in line for line in f)


def filter_log_by_keyword(path: Path, keyword: str) -> List[Tuple[time, str]]:
    """
    Filters the log file and returns lines that contain a specific keyword.

    Args:
        path (Path): Path to the log file.
        keyword (str): Substring to filter lines by.

    Returns:
        List[Tuple[time, str]]: Matching lines with timestamps.
    """
    return [(t, line) for t, line in read_log_utf16(path) if keyword in line]
