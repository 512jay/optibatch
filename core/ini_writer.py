# File: optibatch/core/ini_writer.py

from pathlib import Path
from datetime import datetime
from core.state import registry
from core.ini_generator import generate_monthly_ini_files, CasePreservingConfig
from loguru import logger
import json


def parse_symbols(symbols_field) -> list[str]:
    if isinstance(symbols_field, str):
        return [s.strip() for s in symbols_field.split(",")]
    if isinstance(symbols_field, list):
        return symbols_field
    raise ValueError(f"Unexpected symbol format: {symbols_field}")


def generate_single_ini(
    base_ini_path: Path,
    symbol: str,
    from_str: str,
    to_str: str,
    symbol_folder: Path,
    dry_run: bool,  # Still passed for logging, but doesn't block write
) -> Path:
    ini = CasePreservingConfig(strict=False)
    ini.read(base_ini_path, encoding="utf-16")
    ini["Tester"]["Symbol"] = symbol
    ini["Tester"]["FromDate"] = from_str
    ini["Tester"]["ToDate"] = to_str
    ini["Tester"][
        "Report"
    ] = f"{symbol}.{from_str.replace('.', '')}_{to_str.replace('.', '')}"

    name = f"{symbol}.{from_str.replace('.', '')}_{to_str.replace('.', '')}.ini"
    path = symbol_folder / name

    with path.open("w", encoding="utf-16") as f:
        for section in ini.sections():
            f.write(f"[{section}]\n")
            for key, value in ini[section].items():
                f.write(f"{key}={value}\n")

    logger.debug(f"{'Dry run:' if dry_run else 'Wrote'} INI file: {path}")
    return path


def generate_ini_files(config: dict, run_folder: Path, dry_run: bool = False) -> int:
    """
    Generates .ini files based on config dict.
    Returns the number of files actually written.
    """
    from_str = config["tester"]["FromDate"]
    to_str = config["tester"]["ToDate"]
    from_date = datetime.strptime(from_str, "%Y.%m.%d").date()
    to_date = datetime.strptime(to_str, "%Y.%m.%d").date()

    use_months = registry.get("use_discrete_months")
    symbols = parse_symbols(config["tester"]["Symbol"])
    base_ini_path = Path(".cache/current_config.ini")
    total_written = 0

    for symbol in symbols:
        symbol_folder = run_folder / symbol
        symbol_folder.mkdir(parents=True, exist_ok=True)

        if use_months:
            files = generate_monthly_ini_files(
                base_ini_path=base_ini_path,
                output_folder=symbol_folder,
                symbols=[symbol],
                from_date=from_date,
                to_date=to_date,
            )
            written = len(files)
        else:
            result = generate_single_ini(
                base_ini_path=base_ini_path,
                symbol=symbol,
                from_str=from_str,
                to_str=to_str,
                symbol_folder=symbol_folder,
                dry_run=dry_run,
            )
            written = 1 if result else 0

        total_written += written
        logger.info(
            f"{'Dry run:' if dry_run else 'Created'} {written} INI files for {symbol}"
        )

    return total_written
