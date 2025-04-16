# streamlit_view/main.py

import streamlit as st
from streamlit_view.layout import configure_page
from streamlit_view.load_data import load_and_prepare_dataframe
from streamlit_view.charts import (
        show_combined_symbol_chart,
        show_grouped_line_chart,
        show_profit_scatter,
        show_monthly_box_plot
    )
from streamlit_view.tables import show_run_table
from streamlit_view.ini_export_controls import show_ini_export_controls
from streamlit_view.summary import show_summary_insights
from streamlit_view.filters import apply_filters


def main() -> None:
    configure_page()

    st.title("📊 OptiBatch Dashboard")

    df = load_and_prepare_dataframe()
    if df.empty:
        st.warning("No jobs or runs found.")
        return
    df = apply_filters(df)

    st.success(f"✅ Loaded {len(df)} runs.")

    # Show insights before charts
    show_summary_insights(df)

    chart_tabs = st.tabs(
        [
            "📈 Raw Monthly Line Chart",
            "📊 Grouped Monthly Line Chart",
            "🟢 Profit Scatter",
            "📦 Monthly Box Plot",
        ]
    )

    with chart_tabs[0]:
        show_combined_symbol_chart(df)
    with chart_tabs[1]:
        show_grouped_line_chart(df)
    with chart_tabs[2]:
        show_profit_scatter(df)
    with chart_tabs[3]:
        show_monthly_box_plot(df)

    show_run_table(df)
    show_ini_export_controls()


if __name__ == "__main__":
    main()
