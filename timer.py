#timer.py
import streamlit as st
import time
from text_utils import get_text

def start_timer():
    st.session_state.timer_active = True
    st.session_state.countdown_start_time = time.time()



def display_back_button():
    if st.button(get_text("Zurück", "Back"), key="back_button"):
        st.session_state.page = 'home'
        st.rerun()

def reset_timer_state():
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.current_company_team = None
