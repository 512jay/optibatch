# File: dev/tools/query.py
# Purpose: Confirm that job + run data was ingested correctly

from sqlalchemy import select, func
from database.session import get_engine, get_session
from database.models import Job, Run


def show_ingestion_summary():
    engine = get_engine()
    with get_session(engine) as session:
        total_jobs = session.scalar(select(func.count(Job.id)))
        total_runs = session.scalar(select(func.count(Run.id)))

        print(f"🧾 Total Jobs: {total_jobs}")
        print(f"📊 Total Runs: {total_runs}")

        latest_job = session.execute(
            select(Job).order_by(Job.created_at.desc()).limit(1)
        ).scalar_one_or_none()

        if latest_job:
            print("\n📌 Latest Job:")
            print(f"  ID:         {latest_job.id}")
            print(f"  Name:       {latest_job.job_name}")
            print(f"  Strategy:   {latest_job.expert_name}")
            print(f"  Deposit:    {latest_job.deposit} {latest_job.currency}")
            print(f"  Created At: {latest_job.created_at}")

            run_count = session.scalar(
                select(func.count(Run.id)).where(Run.job_id == latest_job.id)
            )
            print(f"  # of Runs:  {run_count}")
        else:
            print("❌ No jobs found.")


if __name__ == "__main__":
    show_ingestion_summary()
