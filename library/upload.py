import streamlit as st
from io import StringIO


def upload_pgn():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        return StringIO(uploaded_file.getvalue().decode("utf-8"))
    return None
