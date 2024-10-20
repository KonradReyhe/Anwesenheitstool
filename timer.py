#timer.py
import streamlit as st
import time
from utils import get_text
from navigation import return_to_company_selection

def start_timer():
    st.session_state.timer_active = True
    st.session_state.countdown_start_time = time.time()

def check_timer():
    if st.session_state.timer_active and st.session_state.countdown_start_time and not st.session_state.all_employees_added_time:
        elapsed_time = time.time() - st.session_state.countdown_start_time
        remaining_time = max(0, 30 - int(elapsed_time))
        
        if remaining_time > 0:
            st.info(f"{get_text('Zurück zur Firmenauswahl in', 'Back to company selection in')} {remaining_time} {get_text('Sekunden...', 'seconds...')}")
        else:
            return_to_company_selection()

def display_back_button():
    if st.button(get_text("Zurück", "Back"), key="back_button"):
        st.session_state.page = 'home'
        st.experimental_rerun()

def reset_timer_state():
    st.session_state.timer_active = False
    st.session_state.countdown_start_time = None
    st.session_state.current_company_team = None
