# dev/test_ingest.py
from database.ingest.ingest_job import ingest_job_folder
from pathlib import Path

ingest_job_folder(Path("generated/20250412_002932_IndyTSL"))
