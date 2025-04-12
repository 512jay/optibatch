# file: optibatch/core/job_context.py

from dataclasses import dataclass
from pathlib import Path


@dataclass
class JobContext:
    symbol: str
    ini_file: Path
    basename: str
    run_folder: Path

    @property
    def final_xml_path(self) -> Path:
        return self.run_folder / self.symbol / f"{self.basename}.xml"

    @property
    def report_exists(self) -> bool:
        """
        Returns True if the final .xml report exists and is not empty.
        """
        return self.final_xml_path.exists() and self.final_xml_path.stat().st_size > 0


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
