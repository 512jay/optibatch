# streamlit_view/layout.py

import streamlit as st


def configure_page() -> None:
    st.set_page_config(
        page_title="OptiBatch Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )
