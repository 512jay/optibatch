# File: core/job_runner.py

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from core.automation import optimize_with_mt5
from report_util.reporter import export_and_confirm_xml
from loguru import logger
from core.job_context import JobContext
from database.ingest.ingest_job import ingest_single_xml, extract_job_metadata
from database.session import get_engine, get_session
from database.models import Job
from sqlalchemy.exc import SQLAlchemyError
from xml.etree.ElementTree import ParseError


def xml_exists(context: JobContext) -> bool:
    return context.final_xml_path.is_file()


def run_symbol_optimization(context: JobContext, timeout: int = 300) -> bool:
    logger.info(f"🧪 Running optimization for {context.basename}")

    if not optimize_with_mt5(context, timeout=timeout):
        logger.warning(f"⚠️ MT5 optimization failed or timed out for {context.basename}")
        return False

    if not export_and_confirm_xml(context):
        logger.warning(f"⚠️ Failed to export XML for {context.basename}")
        return False

    # ✅ Ingest the XML result into the database
    job_folder = context.run_folder
    config_path = job_folder / "job_config.json"
    xml_path = context.final_xml_path
    job_id = context.job_id

    engine = get_engine()
    with get_session(engine) as session, session.begin():
        # Ensure job record exists
        if not session.get(Job, job_id):
            job_meta = extract_job_metadata(config_path)
            job = Job(
                id=job_id, job_name=job_id, created_at=datetime.utcnow(), **job_meta
            )
            session.add(job)

        try:
            added = ingest_single_xml(xml_path, config_path, session, job_id)
            if added == 0:
                logger.warning(
                    f"⚠️ No passes found in {xml_path.name}, skipping ingest."
                )
                return False
            logger.success(f"📊 Ingested {added} runs from {xml_path.name}")
        except (ValueError, ParseError, SQLAlchemyError) as e:
            logger.exception(f"❌ Failed to ingest XML {xml_path.name}: {e}")
            return False

    return True
