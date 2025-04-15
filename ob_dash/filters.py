import streamlit as st
import pandas as pd
from typing import Tuple, List


def apply_month_filter(df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
    months = df["Month"].dropna().unique().tolist()
    selected_month = st.sidebar.selectbox(
        "\U0001f4c5 Filter by Month", ["All"] + sorted(months)
    )

    if selected_month != "All":
        return df[df["Month"] == selected_month], selected_month
    return df, "All"


def apply_symbol_and_model_filters(df: pd.DataFrame) -> pd.DataFrame:
    symbols = list(df["Symbol"].dropna().astype(str).unique())
    models = list(df["Model"].dropna().astype(str).unique())

    symbol_options: List[str] = ["All"] + symbols
    model_options: List[str] = ["All"] + models

    selected_symbol: str = st.sidebar.selectbox("Filter by Symbol", symbol_options)
    selected_model: str = st.sidebar.selectbox("Filter by Model", model_options)

    filtered_df = df.copy()
    if selected_symbol != "All":
        filtered_df = filtered_df[filtered_df["Symbol"] == selected_symbol]
    if selected_model != "All":
        filtered_df = filtered_df[filtered_df["Model"] == selected_model]

    return filtered_df
