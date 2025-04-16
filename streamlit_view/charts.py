# streamlit_view/charts.py

import streamlit as st
import pandas as pd
import plotly.express as px


def show_combined_symbol_chart(df: pd.DataFrame) -> None:
    """Displays a line chart showing raw monthly profit per symbol."""
    if df.empty:
        st.info("No data available.")
        return

    if not {"Run Month", "Symbol", "Profit"}.issubset(df.columns):
        st.warning("Missing required columns for chart.")
        return

    fig = px.line(
        df,
        x="Run Month",
        y="Profit",
        color="Symbol",
        title="📈 Monthly Profit by Symbol (Raw Data)",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)


def show_grouped_line_chart(df: pd.DataFrame) -> None:
    """Displays a grouped line chart aggregating profit per month per symbol."""
    if df.empty:
        st.info("No data available.")
        return

    grouped = df.groupby(['Run Month', 'Symbol'], as_index=False).agg({'Profit': 'sum'})
    fig = px.line(
        grouped,
        x='Run Month',
        y='Profit',
        color='Symbol',
        title='📈 Total Monthly Profit by Symbol (Grouped)',
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)


def show_profit_scatter(df: pd.DataFrame) -> None:
    """Displays a scatter plot of profit per run."""
    if df.empty:
        st.info("No data available.")
        return

    fig = px.scatter(
        df,
        x='Run Month',
        y='Profit',
        color='Symbol',
        title='🔍 Profit per Run by Symbol',
        hover_data=['Run ID', 'Trades', 'Drawdown']
    )
    st.plotly_chart(fig, use_container_width=True)


def show_monthly_box_plot(df: pd.DataFrame) -> None:
    """Displays a box plot of monthly profit distributions per symbol."""
    if df.empty:
        st.info("No data available.")
        return

    fig = px.box(
        df,
        x='Run Month',
        y='Profit',
        color='Symbol',
        title='📦 Monthly Profit Distribution by Symbol'
    )
    st.plotly_chart(fig, use_container_width=True)