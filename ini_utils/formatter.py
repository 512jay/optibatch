# File: core/utils/ini_utils.py

from pathlib import Path
from datetime import datetime
import json

from helpers.path_utils import get_ini_output_dir  # Determines where .ini files go
from trash.writer import format_ini  # Builds the content of each .ini file


def generate_ini_files_from_job(job_path: Path) -> list[Path]:
    """
    Generates .ini files from a job config file.

    Each .ini file corresponds to a single symbol and will be saved in a folder
    named after the job file (same stem as job_path). Returns a list of generated ini file paths.

    Args:
        job_path (Path): Path to the job JSON file (UTF-16 encoded).

    Returns:
        list[Path]: A list of paths to the generated .ini files.
    """

    # Read the job config (UTF-16 encoded JSON)
    with job_path.open("r", encoding="utf-16") as f:
        config = json.load(f)

    # Format dates from "YYYY.MM.DD" to "YYYYMMDD" for filenames
    start_fmt = datetime.strptime(config["date"]["start"], "%Y.%m.%d").strftime(
        "%Y%m%d"
    )
    end_fmt = datetime.strptime(config["date"]["end"], "%Y.%m.%d").strftime("%Y%m%d")

    # Extract EA name and target symbols list
    expert_name = config["expert"]["name"]
    symbols = config["symbols"]

    # Determine output directory: e.g., jobs/job_20250407_001/
    output_dir = get_ini_output_dir(job_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    ini_paths = []

    # For each symbol, create an .ini file with a unique run ID (e.g., 001, 002, ...)
    for idx, symbol in enumerate(symbols, start=1):
        run_id = f"{idx:03}"  # Pad index: 1 -> '001'
        ini_name = f"{expert_name}.{symbol}.H1.{start_fmt}_{end_fmt}.{run_id}.ini"
        ini_path = output_dir / ini_name

        # Get the content using the formatter and save as UTF-16
        ini_content = format_ini(config, symbol)
        ini_path.write_text(ini_content, encoding="utf-16")
        ini_paths.append(ini_path)

    return ini_paths
