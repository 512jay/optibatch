# streamlit_view/load_data.py

from typing import Sequence
from database.models import Job
from database.session import get_engine, get_session
import pandas as pd
from database.models import Run
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def load_and_prepare_dataframe() -> pd.DataFrame:
    engine = get_engine()
    rows: list[dict] = []

    with get_session(engine) as session:
        stmt = (
            select(Job).options(selectinload(Job.runs)).order_by(Job.created_at.desc())
        )
        jobs = session.scalars(stmt).all()

        for job in jobs:
            for run in job.runs:
                rows.append(
                    {
                        "Run ID": run.id,
                        "Job ID": job.id,
                        "Created": job.created_at,
                        "Symbol": run.symbol,
                        "Profit": run.profit,
                        "Drawdown": run.drawdown,
                        "Custom Score": run.custom_score,
                        "Sharpe Ratio": run.sharpe_ratio,
                        "Trades": run.trades,
                        "Expected Payoff": run.expected_payoff,
                        "Recovery Factor": run.recovery_factor,
                        "Profit Factor": run.profit_factor,
                        "Run Month": run.run_month,
                        "params_json": run.params_json,
                    }
                )

    return pd.DataFrame(rows)


def load_jobs() -> Sequence[Job]:
    engine = get_engine()
    with get_session(engine) as session:
        return session.query(Job).order_by(Job.created_at.desc()).all()
