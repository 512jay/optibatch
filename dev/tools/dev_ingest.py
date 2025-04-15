# dev/tools/dev_ingest.py

from pathlib import Path
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from database.ingest.ingest_job import ingest_job_folder

folder = Path("generated/20250415_005024_IndyTSL")
ingest_job_folder(folder)
