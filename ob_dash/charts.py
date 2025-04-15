import plotly.express as px
import pandas as pd
import streamlit as st


def plot_best_runs_line_chart(best_runs: pd.DataFrame) -> None:
    st.subheader("\U0001f4c8 Month-over-Month Performance (Best Runs)")
    fig = px.line(
        best_runs,
        x="Month",
        y="Profit",
        color="Symbol",
        line_group="Expert",
        hover_data=["Expert", "Run ID", "Drawdown", "Custom Score"],
        title="Month-over-Month Best Profit by Strategy and Symbol",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_monthly_metrics(summary: pd.DataFrame) -> None:
    st.subheader("\U0001f4c8 Month-over-Month Performance")
    fig = px.line(
        summary,
        x="Month",
        y=["Profit", "Drawdown", "Custom Score"],
        markers=True,
        title="Month-over-Month Metrics",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_profit_vs_drawdown(df: pd.DataFrame) -> None:
    st.subheader("\U0001f4c8 Profit vs Drawdown")
    fig = px.scatter(
        df,
        x="Drawdown",
        y="Profit",
        color="Symbol",
        hover_data=["Run ID", "Job ID", "Timeframe", "Model"],
        labels={"Profit": "Profit ($)", "Drawdown": "Drawdown ($)"},
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_custom_score_vs_profit(df: pd.DataFrame) -> None:
    st.subheader("\U0001f4c9 Profit vs Custom Score")
    fig = px.scatter(
        df,
        x="Custom Score",
        y="Profit",
        color="Model",
        hover_data=["Run ID", "Symbol", "Timeframe"],
        labels={"Custom Score": "Score", "Profit": "Profit ($)"},
    )
    st.plotly_chart(fig, use_container_width=True)
