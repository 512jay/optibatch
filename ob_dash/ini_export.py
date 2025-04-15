import streamlit as st
import tempfile
from pathlib import Path
from database.export.ini_writer import write_ini_for_run


def show_ini_export_controls(selected_run_id: str | None) -> None:
    st.subheader("\U0001f6e0 Export INI for Clicked Row")

    if selected_run_id:
        if st.button("Generate INI from Selected Row"):
            with tempfile.TemporaryDirectory() as tmpdir:
                path = write_ini_for_run(
                    run_id=int(selected_run_id), output_dir=Path(tmpdir)
                )

                with open(path, "rb") as f:
                    st.download_button(
                        "\U0001f4c5 Download INI File",
                        f,
                        file_name=path.name,
                        mime="text/plain",
                    )
    else:
        st.info("Click a row above to enable export.")
