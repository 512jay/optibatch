# core/ini_generator.py

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
from typing import List, Tuple
from configparser import ConfigParser
from loguru import logger


class CasePreservingConfig(ConfigParser):
    def optionxform(self, optionstr: str) -> str:
        return optionstr


def get_full_month_ranges(start: date, end: date) -> List[Tuple[date, date]]:
    """Returns (FromDate, ToDate) pairs for each full calendar month in the range."""
    current = start.replace(day=1)
    if start.day != 1:
        current += relativedelta(months=1)

    months = []
    while current + relativedelta(days=1) < end:
        month_end = (current + relativedelta(months=1)) - timedelta(days=1)
        if month_end < end:
            months.append((current, month_end))
        current += relativedelta(months=1)

    return months


def generate_monthly_ini_files(
    base_ini_path: Path,
    output_folder: Path,
    symbols: List[str],
    from_date: date,
    to_date: date,
) -> List[Path]:
    """
    Generate .ini files for each symbol and month slice within the date range.
    Returns list of all generated ini paths.
    """
    base_ini = CasePreservingConfig(strict=False)
    base_ini.read(base_ini_path, encoding="utf-16")

    output_folder.mkdir(parents=True, exist_ok=True)

    full_months = get_full_month_ranges(from_date, to_date)
    if not full_months:
        logger.warning("No full months found in selected date range.")
        return []

    skipped_start = from_date.day != 1
    skipped_end = to_date != (
        to_date.replace(day=1) + relativedelta(months=1) - timedelta(days=1)
    )

    if skipped_start or skipped_end:
        logger.warning("Partial months trimmed. Using full months only.")

    generated_files = []

    for symbol in symbols:
        for start, end in full_months:
            ini_copy = CasePreservingConfig(strict=False)
            ini_copy.read_dict(base_ini)

            ini_copy["Tester"]["Symbol"] = symbol
            ini_copy["Tester"]["FromDate"] = start.strftime("%Y.%m.%d")
            ini_copy["Tester"]["ToDate"] = end.strftime("%Y.%m.%d")

            # Inject Report key just in case
            ini_copy["Tester"][
                "Report"
            ] = f"{symbol}.{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}"

            name = f"{symbol}.{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.ini"
            out_path = output_folder / name
            with out_path.open("w", encoding="utf-16") as f:
                for section in ini_copy.sections():
                    f.write(f"[{section}]\n")
                    for key, value in ini_copy[section].items():
                        f.write(f"{key}={value}\n")

            generated_files.append(out_path)

    return generated_files
