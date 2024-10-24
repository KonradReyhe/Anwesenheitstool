# text_utils.py
"""
This module provides utility functions for text handling and localization
in the GetTogether application.
"""
import streamlit as st

def toggle_language():
    current_language = st.session_state.get('language', 'de')
    new_language = 'en' if current_language == 'de' else 'de'
    st.session_state.language = new_language
    if current_language != new_language:
        st.rerun()

def get_text(de_text, en_text):
    """Get the appropriate text based on the current language setting.

    Args:
        german_text (str): The text in German.
        english_text (str): The text in English.

    Returns:
        str: The text in the current language.
    """
    return en_text if st.session_state.get('language') == 'EN' else de_text
