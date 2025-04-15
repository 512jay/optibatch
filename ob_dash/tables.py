import streamlit as st
import pandas as pd


def show_best_runs_table(best_runs: pd.DataFrame) -> None:
    st.subheader("\U0001f3c6 Best Runs Per Month")
    st.dataframe(
        best_runs[
            [
                "Month",
                "Expert",
                "Symbol",
                "Timeframe",
                "Profit",
                "Drawdown",
                "Custom Score",
                "Run ID",
            ]
        ]
    )


def show_monthly_summary_table(summary: pd.DataFrame) -> None:
    st.subheader("\U0001f4c6 Monthly Summary")
    st.dataframe(summary)


def show_runs_table(df: pd.DataFrame) -> None:
    st.subheader("\U0001f4cb Optimization Runs")
    st.dataframe(
        df.sort_values(by="Created", ascending=False), use_container_width=True
    )


def get_selected_run_id(df: pd.DataFrame, key: str) -> str | None:
    selected = st.data_editor(
        df.sort_values(by="Created", ascending=False),
        num_rows="dynamic",
        use_container_width=True,
        key=key,
        disabled=True,
    )
    if not selected.empty:
        return selected.iloc[0]["Run ID"]
    return None
