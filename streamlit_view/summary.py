import streamlit as st
import pandas as pd


def show_summary_insights(df: pd.DataFrame) -> None:
    st.markdown("### 🧠 Run Summary Insights")

    if df.empty:
        st.info("No data available to summarize.")
        return

    symbol_perf = df.groupby("Symbol")["Profit"].sum().sort_values(ascending=False)
    month_perf = df.groupby("Run Month")["Profit"].sum().sort_values(ascending=False)
    avg_profit = df["Profit"].mean()
    top_run = df.loc[df["Custom Score"].idxmax()] if "Custom Score" in df else None

    st.write(
        f"📌 **Top-performing Symbol**: `{symbol_perf.idxmax()}` with total profit of `{symbol_perf.max():,.2f}`"
    )
    st.write(
        f"📉 **Worst Month**: `{month_perf.idxmin()}` with total loss of `{month_perf.min():,.2f}`"
    )
    st.write(
        f"📈 **Best Month**: `{month_perf.idxmax()}` with total profit of `{month_perf.max():,.2f}`"
    )
    st.write(f"📊 **Average Profit per Run**: `{avg_profit:,.2f}`")

    if top_run is not None:
        st.markdown("🥇 **Top Run by Custom Score**")
        st.json(
            {
                "Run ID": int(top_run["Run ID"]),
                "Symbol": top_run["Symbol"],
                "Profit": round(top_run["Profit"], 2),
                "Custom Score": round(top_run["Custom Score"], 2),
                "Trades": int(top_run["Trades"]),
                "Drawdown": round(top_run["Drawdown"], 2),
            }
        )
