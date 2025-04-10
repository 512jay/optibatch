# File: optibatch/core/run_utils.py

from datetime import datetime
from pathlib import Path
import shutil
from pathlib import Path
import zipfile
import subprocess
import time
from datetime import datetime
import re
from pathlib import Path
# ==========================
# Log Monitoring
# ==========================

import re
from datetime import datetime


def get_latest_log_path(log_folder: Path) -> Path | None:
    """
    Returns the most recently modified .log file in the tester/logs folder.
    Returns None if no logs exist.
    """
    log_files = sorted(
        log_folder.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return log_files[0] if log_files else None


def get_latest_log_timestamp(log_folder: Path) -> datetime | None:
    """
    Scans the latest MT5 tester log for the most recent timestamp entry.
    Assumes logs are encoded in UTF-16 and timestamps look like: '2025.04.10 08:00:02'
    Returns a datetime object or None if not found.
    """
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


def wait_for_mt5_to_finish(
    log_dir: Path, start_time: float, timeout: int = 300
) -> bool:
    """
    Watches MT5 tester logs for 'optimization finished' or 'already processed'.
    Returns True if successful, False if timeout.
    """
    deadline = time.time() + timeout
    last_seen = None

    while time.time() < deadline:
        logs = sorted(
            log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True
        )
        if not logs:
            time.sleep(1)
            continue

        latest_log = logs[0]
        with latest_log.open(encoding="utf-16") as f:
            for line in f:
                if (
                    "optimization finished" in line
                    or "optimization already processed" in line
                ):
                    return True
        time.sleep(2)

    return False


def launch_mt5_with_ini(ini_file: Path, mt5_path: Path) -> None:
    """
    Launches MetaTrader 5 with the given .ini config file.
    """
    if not mt5_path.exists():
        raise FileNotFoundError(f"MT5 executable not found: {mt5_path}")

    if not ini_file.exists():
        raise FileNotFoundError(f"INI file not found: {ini_file}")

    subprocess.Popen([str(mt5_path), f"/config:{ini_file}"])


def create_run_folder(ea_name: str, base_dir: str = "generated_ini") -> Path:
    """
    Creates a run folder like: generated_ini/{timestamp}_{ea_name}/
    Returns the Path object to that folder.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{timestamp}_{ea_name}"
    run_folder = Path(base_dir) / folder_name
    run_folder.mkdir(parents=True, exist_ok=False)
    return run_folder


def get_symbol_folder(run_folder: Path, symbol: str) -> Path:
    """
    Creates and returns a folder inside `run_folder` for the given symbol.
    """
    symbol_folder = run_folder / symbol
    symbol_folder.mkdir(parents=True, exist_ok=True)
    return symbol_folder


def copy_core_files_to_run(
    run_folder: Path, ini_src: Path, json_src: Path | None = None
) -> tuple[Path, Path | None]:
    """
    Copies the core INI and optional JSON config into the run folder.
    Filenames will match the run folder name (e.g., 20250410_1120_IndyTSL.ini).
    Returns a tuple of (ini_path, json_path or None).
    """
    base_name = run_folder.name
    ini_dest = run_folder / f"{base_name}.ini"
    shutil.copy2(ini_src, ini_dest)

    json_dest = None
    if json_src and json_src.exists():
        json_dest = run_folder / f"{base_name}.json"
        shutil.copy2(json_src, json_dest)

    return ini_dest, json_dest


def archive_run_folder(run_folder: Path, delete_original: bool = False) -> Path:
    """
    Zips the entire run folder (e.g., 20250410_1120_IndyTSL).
    If delete_original=True, deletes the folder after zipping.
    Returns the path to the zip file.
    """
    zip_path = run_folder.with_suffix(".zip")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for file_path in run_folder.rglob("*"):
            arcname = file_path.relative_to(run_folder.parent)
            zipf.write(file_path, arcname)

    if delete_original:
        shutil.rmtree(run_folder)

    return zip_path


def write_readme(
    run_folder: Path,
    ea_name: str,
    date_range: tuple[str, str],
    symbols: list[str],
    optimization: str,
    forward: str,
    month_split: bool,
    ini_count: int,
) -> Path:
    """
    Writes a README.txt file in the run folder summarizing the run.
    Returns the path to the README.
    """
    readme_path = run_folder / "README.txt"
    with readme_path.open("w", encoding="utf-8") as f:
        f.write(f"Run ID: {run_folder.name}\n")
        f.write(f"Expert Advisor: {ea_name}\n")
        f.write(f"Date Range: {date_range[0]} to {date_range[1]}\n")
        f.write(f"Symbols: {', '.join(symbols)}\n")
        f.write(f"Optimization Mode: {optimization}\n")
        f.write(f"Forward Mode: {forward}\n")
        f.write(
            f"Month-to-Month Splitting: {'Enabled' if month_split else 'Disabled'}\n"
        )
        f.write(f"Files Generated: {ini_count} .ini files\n")
        f.write(f"Original Configs: {run_folder.name}.ini, .json\n")
    return readme_path


def delete_run_folder(run_folder: Path) -> None:
    """
    Deletes the entire run folder and all its contents.

    Example:
    run_folder = Path("generated_ini/20250410_1120_IndyTSL")
    delete_run_folder(run_folder)
    """
    if not run_folder.exists() or not run_folder.is_dir():
        raise FileNotFoundError(f"Run folder not found: {run_folder}")

    # Safety: only allow deleting inside generated_ini/
    if "generated_ini" not in str(run_folder.resolve()):
        raise ValueError("Deletion is only allowed for folders inside 'generated_ini'")

    shutil.rmtree(run_folder)
