import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- Generate Fake Data ---
np.random.seed(42)
months = pd.date_range("2025-01-01", "2025-06-01", freq="MS").strftime("%Y-%m").tolist()
symbols = ["EURUSD", "GBPUSD", "USDJPY"]
strategies = ["IndyTSL", "MomentumX", "ReversalPro"]

data = []
for strategy in strategies:
    for symbol in symbols:
        for month in months:
            data.append(
                {
                    "run_month": month,
                    "expert_name": strategy,
                    "symbol": symbol,
                    "profit": round(np.random.normal(500, 100), 2),
                    "drawdown": round(np.random.normal(100, 20), 2),
                    "sharpe_ratio": round(np.random.uniform(0.5, 2.0), 2),
                    "job_name": f"{strategy}_{symbol}_{month}",
                }
            )

df = pd.DataFrame(data)

# --- Sidebar Filters ---
st.sidebar.title("📊 Filter Options")
selected_strategies = st.sidebar.multiselect(
    "Strategy", df["expert_name"].unique(), default=strategies
)
selected_symbols = st.sidebar.multiselect(
    "Symbol", df["symbol"].unique(), default=symbols
)
selected_metrics = st.sidebar.multiselect(
    "Metrics to Visualize", ["profit", "drawdown", "sharpe_ratio"], default=["profit"]
)

filtered = df[
    df["expert_name"].isin(selected_strategies) & df["symbol"].isin(selected_symbols)
]

# --- Line Charts ---
st.title("📈 Month-to-Month Strategy Performance")
for metric in selected_metrics:
    st.subheader(f"{metric.replace('_', ' ').title()} Over Time")
    chart = (
        alt.Chart(filtered)
        .mark_line(point=True)
        .encode(
            x="run_month:T",
            y=alt.Y(metric, title=metric.replace("_", " ").title()),
            color="symbol:N",
            tooltip=["job_name", "symbol", metric],
        )
        .properties(width=700)
    )
    st.altair_chart(chart, use_container_width=True)

# --- Table View ---
st.subheader("🧾 Raw Data Table")
st.dataframe(filtered.sort_values(["run_month", "expert_name", "symbol"]))
