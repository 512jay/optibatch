# File: core/job_runner.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from core.state import registry
from core.automation import optimize_with_mt5
from report_util.grabber import export_and_confirm_xml, get_current_xml_path
from loguru import logger
from core.job_context import build_job_context, JobContext



def xml_exists(context: JobContext) -> bool:
    path = context.xml_path
    return path.exists() and path.stat().st_size > 0


def run_symbol_optimization(
    context: JobContext, mt5_path: Path, log_path: Path, timeout: int = 300
) -> bool:
    logger.info(f"Running optimization for {context.basename}")

    registry.set("current_basename", context.basename)
    registry.save()

    success = optimize_with_mt5(
        ini_file=context.ini_file, mt5_path=mt5_path, log_path=log_path, timeout=timeout
    )

    if not success:
        logger.warning(f"⚠️ MT5 optimization failed or timed out for {context.basename}")
        return False

    if not export_and_confirm_xml():
        logger.warning(f"⚠️ Failed to export XML for {context.basename}")
        return False

    return True
