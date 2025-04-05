# File: core/utils/ini_utils.py
from pathlib import Path
from datetime import datetime
import json

from helpers.path_utils import get_ini_output_dir
from ini_utils.writer import format_ini

def generate_ini_files_from_job(job_path: Path) -> list[Path]:
    """
    Generates .ini files from a job config file. Each .ini file is saved in a folder
    named after the job file (same stem). Returns a list of generated ini file paths.
    """
    with job_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    start_fmt = datetime.strptime(config["date"]["start"], "%Y-%m-%d").strftime(
        "%Y%m%d"
    )
    end_fmt = datetime.strptime(config["date"]["end"], "%Y-%m-%d").strftime("%Y%m%d")
    expert_name = config["expert"]["name"]
    symbols = config["symbols"]

    output_dir = get_ini_output_dir(job_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    ini_paths = []
    for idx, symbol in enumerate(symbols, start=1):
        run_id = f"{idx:03}"
        ini_name = f"{expert_name}.{symbol}.H1.{start_fmt}_{end_fmt}.{run_id}.ini"
        ini_path = output_dir / ini_name
        ini_content = format_ini(config, symbol)
        ini_path.write_text(ini_content, encoding="utf-16")
        ini_paths.append(ini_path)

    return ini_paths
