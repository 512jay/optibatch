# File: helpers/path_utils.py

from datetime import datetime
from pathlib import Path


def get_next_job_path() -> Path:
    today = datetime.now().strftime("%Y%m%d")
    job_dir = Path("jobs")
    job_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(job_dir.glob(f"job_{today}_*.json"))
    next_index = len(existing) + 1
    return job_dir / f"job_{today}_{next_index:03d}.json"


def get_ini_output_dir(job_path: Path) -> Path:
    return job_path.with_suffix("")  # folder with same stem
