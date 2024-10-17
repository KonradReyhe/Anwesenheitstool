import streamlit as st
from datetime import datetime, timedelta
import os
import base64
import pandas as pd

def get_text(de_text, en_text):
    return de_text if st.session_state.language == 'DE' else en_text

def trigger_rerun():
    st.session_state.trigger_rerun = not st.session_state.trigger_rerun

def toggle_language():
    st.session_state.language = 'EN' if st.session_state.language == 'DE' else 'DE'

def display_header():
    # Implementation of display_header function
    pass

# Add other utility functions here
