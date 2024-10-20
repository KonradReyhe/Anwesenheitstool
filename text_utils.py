#text_utils.py
import streamlit as st

def get_text(de_text, en_text):
    return de_text if st.session_state.language == 'DE' else en_text