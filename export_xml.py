# File: export_xml.py

from core.mt5.report_exporter import export_mt5_results_to_xml
from loguru import logger
from uuid import uuid4

if __name__ == "__main__":
    logger.info("🔍 Running standalone MT5 XML export test...")

    # Generate a unique filename using UUID
    run_id = f"test_export_{uuid4().hex[:8]}"
    logger.info(f"📝 Generated run_id: {run_id}")

    export_mt5_results_to_xml(run_id=run_id)
