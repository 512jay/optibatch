# streamlit_view/charts.py

import streamlit as st
import pandas as pd
import plotly.express as px


def show_combined_symbol_chart(df: pd.DataFrame) -> None:
    """Displays a line chart showing monthly profit per symbol."""
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
        title="📈 Monthly Profit by Symbol",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)
