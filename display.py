# display.py
import streamlit as st
import pandas as pd

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
from database.session import get_engine, get_session
from database.models import Job
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, load_only


def run_dashboard() -> None:
    st.set_page_config(layout="wide")
    st.title("📊 OptiBatch Run Explorer")

    engine = get_engine()
    with get_session(engine, expire_on_commit=False) as session:
        count = session.scalar(select(func.count()).select_from(Job))
        st.write(f"🔍 Job count from raw SQLAlchemy query: {count}")

        stmt = (
            select(Job)
            .options(
                load_only(
                    Job.id,
                    Job.job_name,
                    Job.expert_name,
                    Job.expert_path,
                    Job.strategy_version,
                    Job.modeling_mode,
                    Job.optimization_mode,
                    Job.optimization_criterion,
                    Job.period,
                    Job.deposit,
                    Job.currency,
                    Job.leverage,
                    Job.tester_inputs,
                    Job.created_at,
                ),
                selectinload(Job.runs)
            )
        )

        jobs = session.scalars(stmt).all()

        st.write(f"✅ Loaded {len(jobs)} jobs")
        for job in jobs:
            st.write(f"📦 Job {job.id} with {len(job.runs)} runs")

    if not jobs:
        st.warning("No jobs found in the database.")
        st.stop()

    df: pd.DataFrame = jobs_to_dataframe(jobs)

    # st.write("🧾 First few rows of the full job-run DataFrame:")
    # st.dataframe(df.head())

    df, selected_month = apply_month_filter(df)
    filtered_df = apply_symbol_and_model_filters(df)

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

    show_best_runs_table(best_runs)
    show_monthly_summary_table(summary)
    show_runs_table(filtered_df)
    plot_best_runs_line_chart(best_runs)
    plot_monthly_metrics(summary)
    plot_profit_vs_drawdown(filtered_df)
    plot_custom_score_vs_profit(filtered_df)

    selected_run_id = get_selected_run_id(filtered_df, key="optim_table")
    if not selected_run_id:
        selected_run_id = get_selected_run_id(best_runs, key="best_table")

    show_ini_export_controls(selected_run_id)


if __name__ == "__main__":
    run_dashboard()
