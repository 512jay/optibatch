# streamlit_view/filters.py

import streamlit as st
import pandas as pd


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("🔎 Filter Runs")

    # Symbol filter
    symbols = df["Symbol"].dropna().unique().tolist()
    selected_symbols = st.sidebar.multiselect("Symbols", symbols, default=symbols)

    # Run Month range filter
    run_months = sorted(df["Run Month"].dropna().unique())
    selected_months = st.sidebar.multiselect("Run Months", run_months, default=run_months)

    # Profit filter
    min_profit, max_profit = float(df["Profit"].min()), float(df["Profit"].max())
    profit_range = st.sidebar.slider("Profit Range", min_profit, max_profit, (min_profit, max_profit))

    # Trades filter
    if "Trades" in df.columns:
        min_trades, max_trades = int(df["Trades"].min()), int(df["Trades"].max())
        trade_range = st.sidebar.slider("Trades Range", min_trades, max_trades, (min_trades, max_trades))
    else:
        trade_range = (None, None)

    # Apply filters
    filtered_df = df[
        df["Symbol"].isin(selected_symbols)
        & df["Run Month"].isin(selected_months)
        & df["Profit"].between(*profit_range)
    ]

    if trade_range[0] is not None:
        filtered_df = filtered_df[filtered_df["Trades"].between(*trade_range)]

    return filtered_df