# file: optibatch/core/job_context.py

from dataclasses import dataclass
from pathlib import Path
from report_util.grabber import get_current_xml_path


@dataclass
class JobContext:
    symbol: str
    ini_file: Path
    basename: str
    run_folder: Path

    @property
    def xml_path(self) -> Path:
        return get_current_xml_path()


def build_job_context(ini_file: Path, run_folder: Path) -> JobContext:
    symbol = ini_file.parent.name
    stem = ini_file.stem

    if "." in stem:
        _, rest = stem.split(".", 1)
    else:
        rest = stem

    basename = f"{symbol}.{rest}"

    return JobContext(
        symbol=symbol, ini_file=ini_file, basename=basename, run_folder=run_folder
    )
