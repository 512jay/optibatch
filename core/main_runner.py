"""
main_runner.py

This module coordinates the full optimization run for MetaTrader 5 strategies
by generating .ini files, launching MT5 optimizations, ingesting XML results,
and skipping redundant or failed passes.

Adheres to PEP 8, PEP 257, and uses Google-style docstrings.
"""

import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from core.job_context import build_job_context
from core.job_ini_writer import generate_ini_files
from core.job_runner import run_symbol_optimization
from core.logging.logger import start_run_logger, stop_run_logger
from core.run_utils import (
    copy_core_files_to_run,
    create_run_folder,
    get_mt5_executable_path_from_registry,
)
from core.state import registry
from report_util.reporter import clean_orphaned_reports


def run_optimizations(config_path: Path, run_folder: Path | None = None) -> None:
    """Run back-to-back optimizations based on configuration.

    This function handles the full optimization lifecycle:
    - Reads configuration
    - Prepares INI files and job folders
    - Runs MT5 optimizations
    - Ingests results
    - Skips further runs for symbols that produce no valid passes

    Args:
        config_path (Path): Path to the job configuration JSON file.
        run_folder (Path | None): Optional pre-created folder for run.
                                  If None, a new folder is created.
    """
    logger.info("Run Optimizations triggered.")

    config_json = config_path.read_text(encoding="utf-8")
    config = json.loads(config_json)

    ea_name = config["tester"]["Expert"].split("\\")[-1].split(".")[0]
    if run_folder is None:
        run_folder = create_run_folder(ea_name)

    job_name = run_folder.name
    sink_id = start_run_logger(run_folder)
    logger.info(f"Started new optimization run: {job_name}")

    try:
        # Copy configuration files into run folder
        ini_src = Path(".cache/current_config.ini")
        json_src = Path(".cache/current_config.json")
        copy_core_files_to_run(run_folder, ini_src, json_src)

        dry_run = registry.get("dry_run")
        logger.info(f"Dry run mode: {'ON' if dry_run else 'OFF'}")

        ini_count = generate_ini_files(config, run_folder, dry_run=dry_run)
        logger.success(f"Generated {ini_count} INI files.")

        if not dry_run:
            mt5_path = get_mt5_executable_path_from_registry()
            log_path = registry.get("tester_log_path")

            if not log_path:
                logger.error("Could not locate MT5 tester/logs folder.")
                return

            symbols_to_skip = set()

            for symbol_folder in run_folder.iterdir():
                if not symbol_folder.is_dir():
                    continue

                symbol_name = symbol_folder.name
                if symbol_name in symbols_to_skip:
                    logger.info(
                        f"⏭️ Skipping symbol {symbol_name} due to earlier failed optimization."
                    )
                    continue

                for ini_file in sorted(symbol_folder.glob("*.ini")):
                    context = build_job_context(
                        ini_file=ini_file,
                        run_folder=run_folder,
                        log_dir=Path(log_path),
                        timestamp_before=datetime.now(),
                        mt5_path=mt5_path,
                    )

                    if context.report_exists:
                        logger.info(
                            f"✅ Skipping {context.basename} — XML already exists."
                        )
                        continue

                    success = run_symbol_optimization(context)
                    if not success:
                        logger.warning(
                            f"⚠️ Skipping further runs for {symbol_name} — no passes."
                        )
                        symbols_to_skip.add(symbol_name)
                        break

    except Exception as e:
        logger.exception(f"Unexpected error during run: {e}")
    finally:
        logger.info(f"Optimization run complete: {job_name}")
        stop_run_logger(sink_id)
        clean_orphaned_reports()
