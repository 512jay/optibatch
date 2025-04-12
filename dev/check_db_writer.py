from pathlib import Path
from sqlalchemy import select
from database.export.ini_writer import write_ini_for_run
from database.session import get_engine, get_session
from database.models import Run

# Get the latest run ID
engine = get_engine()
with get_session(engine) as session:
    latest_id = session.scalars(select(Run.id).order_by(Run.id.desc())).first()

if latest_id:
    write_ini_for_run(latest_id, Path("~/Desktop/optibatch_exports").expanduser())
else:
    print("❌ No runs found.")
