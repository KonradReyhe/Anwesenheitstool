# text_utils.py

import streamlit as st

def toggle_language():
    current_language = st.session_state.get('language', 'de')
    new_language = 'en' if current_language == 'de' else 'de'
    st.session_state.language = new_language
    if current_language != new_language:
        st.rerun()

def get_text(de_text, en_text):
    return en_text if st.session_state.get('language') == 'EN' else de_text
