# File: core/job_runner.py

from __future__ import annotations
from pathlib import Path
from core.automation import optimize_with_mt5
from report_util.reporter import export_and_confirm_xml
from loguru import logger
from core.job_context import JobContext



def xml_exists(context: JobContext) -> bool:
    path = context.xml_path
    return path.exists() and path.stat().st_size > 0


def run_symbol_optimization(
    context: JobContext, mt5_path: Path, log_path: Path, timeout: int = 300
) -> bool:
    logger.info(f"Running optimization for {context.basename}")

    success = optimize_with_mt5(
        ini_file=context.ini_file, mt5_path=mt5_path, log_path=log_path, timeout=timeout
    )

    if not success:
        logger.warning(f"⚠️ MT5 optimization failed or timed out for {context.basename}")
        return False

    if not export_and_confirm_xml(context):
        logger.warning(f"⚠️ Failed to export XML for {context.basename}")
        return False

    return True
