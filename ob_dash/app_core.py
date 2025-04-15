import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import ob_dash as st
import pandas as pd

from database.session import get_engine, get_session
from database.models import Job
from ob_dash.data_loader import jobs_to_dataframe
from ob_dash.filters import apply_month_filter, apply_symbol_and_model_filters
from ob_dash.charts import (
    plot_best_runs_line_chart,
    plot_monthly_metrics,
    plot_profit_vs_drawdown,
    plot_custom_score_vs_profit,
)
from ob_dash.tables import (
    show_best_runs_table,
    show_monthly_summary_table,
    show_runs_table,
    get_selected_run_id,
)
from ob_dash.ini_export import show_ini_export_controls

def main():
    st.set_page_config(layout="wide")
    st.title("📊 OptiBatch Run Explorer")

    # Load jobs and flatten to dataframe
    engine = get_engine()
    with get_session(engine) as session:
        jobs: list[Job] = session.query(Job).all()

    if not jobs:
        st.warning("No jobs found in the database.")
        st.stop()

    df: pd.DataFrame = jobs_to_dataframe(jobs)

    # Filters
    df, selected_month = apply_month_filter(df)
    filtered_df = apply_symbol_and_model_filters(df)

    # Best runs and summaries
    best_runs = (
        df.sort_values("Profit", ascending=False)
        .groupby(["Month", "Expert", "Symbol"])
        .first()
        .reset_index()
    )

    summary = (
        df.groupby("Month")
        .agg(
            {
                "Profit": "mean",
                "Drawdown": "mean",
                "Custom Score": "mean",
                "Run ID": "count",
            }
        )
        .rename(columns={"Run ID": "Run Count"})
        .reset_index()
    )

    # Tables
    show_best_runs_table(best_runs)
    show_monthly_summary_table(summary)
    show_runs_table(filtered_df)

    # Charts
    plot_best_runs_line_chart(best_runs)
    plot_monthly_metrics(summary)
    plot_profit_vs_drawdown(filtered_df)
    plot_custom_score_vs_profit(filtered_df)

    # INI export logic
    selected_run_id = get_selected_run_id(filtered_df, key="optim_table")
    if not selected_run_id:
        selected_run_id = get_selected_run_id(best_runs, key="best_table")

    show_ini_export_controls(selected_run_id)
