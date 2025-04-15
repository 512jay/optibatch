# streamlit_view/tables.py

from __future__ import annotations

import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame

_selected_run_id_key = "selected_run_id"


def extract_run_id(rows: pd.DataFrame | None) -> int | None:
    if rows is None or rows.empty:
        return None
    return int(rows["Run ID"].iloc[0])


def show_run_table(df: pd.DataFrame) -> None:
    st.markdown("### 🧪 Explore Strategy Runs")

    job_ids = df["Job ID"].unique().tolist()
    selected_job = st.selectbox("Select Job", job_ids)

    filtered_df = df[df["Job ID"] == selected_job]

    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_selection("single", use_checkbox=True)
    gb.configure_pagination()
    gb.configure_default_column(resizable=True, sortable=True, filterable=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        filtered_df,
        gridOptions=grid_options,
        height=400,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="streamlit",
    )

    selected_rows = grid_response["selected_rows"]
    selected_df = pd.DataFrame(selected_rows)

    run_id = extract_run_id(selected_df)
    st.session_state[_selected_run_id_key] = run_id

    with st.expander("🔍 Table selection debug:"):
        st.write(selected_df)
        st.code(f"DEBUG: run_id = {run_id}")
