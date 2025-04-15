from typing import Any
from database.models import Job
import pandas as pd
from collections.abc import Sequence
from typing import Union
OPTIMIZATION_MODES = {"0": "Disabled", "1": "Slow", "2": "Fast", "3": "MarketWatch"}


def flatten_jobs_to_records(jobs: Sequence[Job]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for job in jobs:
        base = {
            "Job ID": job.id,
            "Created": job.created_at,
            "Expert": job.expert_path,
            "Deposit": job.deposit,
            "Currency": job.currency,
            "Leverage": job.leverage,
            "Model": job.modeling_mode,
            "Timeframe": job.period,
        }
        for run in job.runs:
            rec = base.copy()
            rec.update(
                {
                    "Run ID": run.id,
                    "Symbol": run.symbol,
                    "Pass #": run.pass_number,
                    "Profit": run.profit,
                    "Drawdown": run.drawdown,
                    "Win Rate": run.win_rate,
                    "Custom Score": run.custom_score,
                    "Optimization": OPTIMIZATION_MODES.get(
                        str(job.optimization_mode), str(job.optimization_mode)
                    ),
                    "Sharpe": run.sharpe_ratio,
                    "Payoff": run.expected_payoff,
                    "Recovery": run.recovery_factor,
                    "Profit Factor": run.profit_factor,
                    "Trades": run.trades,
                    "Month": f"{run.start_date.strftime('%Y-%m')} to {run.end_date.strftime('%Y-%m')}",
                }
            )
            records.append(rec)
    return records


def jobs_to_dataframe(jobs: Union[Sequence[Job], list[Job]]) -> pd.DataFrame:
    return pd.DataFrame(flatten_jobs_to_records(jobs))
