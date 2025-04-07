# core/jobs_utils/forward_utils.py

import json
from datetime import datetime, timedelta
from pathlib import Path
from core.utils.io import read_utf16_file
from loguru import logger


def get_forward_split_date(job_path: Path) -> datetime:
    data = read_utf16_file(job_path)

    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object from job file.")

    date_start = datetime.strptime(data["Date"]["start"], "%Y.%m.%d")
    date_end = datetime.strptime(data["Date"]["end"], "%Y.%m.%d")
    forward_mode = data.get("Forward", {}).get("mode", 0)

    delta = date_end - date_start

    if forward_mode == 1:  # 1/4
        split_date = date_end - delta / 4
    elif forward_mode == 2:  # 1/2
        split_date = date_end - delta / 2
    elif forward_mode == 3:  # 1/3
        split_date = date_end - delta / 3
    elif forward_mode == 4:  # custom
        custom = data["Forward"].get("custom")
        if not custom:
            raise ValueError("Custom forward mode selected but no date provided.")
        split_date = datetime.strptime(custom, "%Y.%m.%d")
    else:  # mode == 0
        raise ValueError("No forward test defined.")

    return split_date


def parse_forward_mode(job_json_path: Path) -> int:
    """
    Reads the job.json and returns the forward mode as an int.
    0 means no forward test.
    """
    with open(job_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("forward", {}).get("mode", 0)


from core.utils.io import read_utf16_file


def is_forward_enabled(job_json_path: Path) -> bool:
    try:
        job_data = read_utf16_file(job_json_path)
        return job_data.get("forward", {}).get("mode", 0) != 0
    except Exception as e:
        logger.warning(f"Failed to determine forward mode: {e}")
        return False
