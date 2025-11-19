import streamlit as st

def next_page(page_path: str):
    """Navigate to another Streamlit page."""
    st.switch_page(page_path)
