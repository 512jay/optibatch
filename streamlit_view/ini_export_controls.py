from __future__ import annotations

import streamlit as st
from pathlib import Path
from database.export.ini_writer import write_ini_for_run


def show_ini_export_controls() -> None:
    st.sidebar.header("📤 INI Export")
    # st.sidebar.code(f"DEBUG: run_id = {st.session_state.get('selected_run_id')}")

    run_id = st.session_state.get("selected_run_id")

    if run_id is None:
        st.sidebar.info("Select a run to enable export.")
        return
    else:
        st.sidebar.code(f"Selected Run ID: {run_id}")

    export_dir = st.sidebar.text_input("Export to folder:", value=str(Path.home()))

    if st.sidebar.button("Generate INI file"):
        try:
            ini_path = write_ini_for_run(run_id, output_dir=Path(export_dir))
            st.sidebar.success(f"✅ INI saved to: {ini_path}")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to export INI: {e}")
