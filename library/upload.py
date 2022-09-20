import streamlit as st
from io import StringIO


def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['json'])
    if uploaded_file is not None:
        return StringIO(uploaded_file.getvalue().decode("utf-8"))
    return None
