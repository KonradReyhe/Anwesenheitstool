#language_utils.py
import streamlit as st
from utils import get_text

def toggle_language():
    st.session_state.language = 'EN' if st.session_state.language == 'DE' else 'DE'
    st.success(get_text("Sprache wurde geändert.", "Language has been changed."))
    st.rerun()
