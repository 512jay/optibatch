# File: optibatch/core/report_mover.py

import time
import shutil
from pathlib import Path
from loguru import logger


def move_reports_for_ini(
    ini_path: Path,
    report_extensions: list[str] = [".htm", ".csv", ".xml"],
    source_dir: Path = Path("mt5_reports_temp"),
) -> list[Path]:
    """
    Moves reports matching the ini filename (minus .ini) from `source_dir`
    into the same folder as the .ini.

    Returns list of moved report Paths.
    """
    base_name = ini_path.stem
    target_dir = ini_path.parent
    moved = []

    logger.info(f"Looking for reports for: {base_name}")

    for ext in report_extensions:
        report_name = f"{base_name}{ext}"
        src = source_dir / report_name
        if src.exists():
            dst = target_dir / report_name
            shutil.move(src, dst)
            logger.success(f"Moved report: {src.name} → {dst}")
            moved.append(dst)
        else:
            logger.debug(f"Report not found: {src.name}")

    if not moved:
        logger.warning(f"No reports found for {base_name}")

    return moved


def move_all_reports_for_run(
    run_folder: Path,
    source_dir: Path = Path("mt5_reports_temp"),
    extensions: list[str] = [".htm", ".csv", ".xml"],
) -> dict[str, list[Path]]:
    """
    Finds all .ini files in the run folder, and moves matching reports from the MT5 temp folder
    into their respective symbol folders.

    Returns a dict mapping ini filename -> list of report Paths moved.
    """
    logger.info(f"Moving reports for all .ini files in: {run_folder}")
    moved_summary = {}

    ini_files = list(run_folder.rglob("*.ini"))

    for ini_path in ini_files:
        if ini_path.name == f"{run_folder.name}.ini":  # skip master config
            continue

        moved_files = move_reports_for_ini(ini_path, report_extensions=extensions, source_dir=source_dir)

        if moved_files:
            moved_summary[ini_path.name] = moved_files

    logger.info(f"Finished moving reports for {len(moved_summary)} .ini files")
    return moved_summary


def wait_for_report_file(
    base_filename: str,
    source_dir: Path = Path("mt5_reports_temp"),
    extension: str = ".xml",
    timeout: int = 30,
    poll_interval: float = 0.5,
) -> Path:
    """
    Waits for a report file to appear in the source_dir with the given base name + extension.
    Returns the Path if found. Raises TimeoutError if not found in time.
    """
    report_path = source_dir / f"{base_filename}{extension}"
    logger.info(f"Waiting for report: {report_path}")
    elapsed = 0.0

    while not report_path.exists():
        if elapsed >= timeout:
            logger.error(f"Timeout waiting for report: {report_path}")
            raise TimeoutError(f"Report file not found after {timeout}s: {report_path}")
        time.sleep(poll_interval)
        elapsed += poll_interval

    logger.success(f"Report file ready: {report_path}")
    return report_path


def move_report_file(report_path: Path, destination_dir: Path) -> Path:
    """
    Moves the report file into the destination folder.
    Returns the new path.
    """
    destination_path = destination_dir / report_path.name
    shutil.move(report_path, destination_path)
    logger.success(f"Moved report: {report_path.name} → {destination_path}")
    return destination_path
