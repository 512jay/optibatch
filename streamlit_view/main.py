# streamlit_view/main.py

import streamlit as st
from streamlit_view.layout import configure_page
from streamlit_view.load_data import load_and_prepare_dataframe
from streamlit_view.charts import show_combined_symbol_chart
from streamlit_view.tables import show_run_table
from streamlit_view.ini_export_controls import show_ini_export_controls


def main() -> None:
    configure_page()

    st.title("📊 OptiBatch Dashboard")

    df = load_and_prepare_dataframe()
    if df.empty:
        st.warning("No jobs or runs found.")
        return

    st.success(f"✅ Loaded {len(df)} runs.")

    show_combined_symbol_chart(df)
    show_run_table(df)
    show_ini_export_controls()


if __name__ == "__main__":
    main()
