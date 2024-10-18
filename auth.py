# auth.py

import streamlit as st
import time
from config import INACTIVITY_TIMEOUT
from utils import get_text

def start_get_together(pin1, pin2, custom_event_name):
    if pin1 and pin2 and pin1 == pin2:
        st.session_state.pin = pin1
        st.session_state.get_together_started = True
        
        # Set custom event name only if it's not empty
        st.session_state.custom_event_name = custom_event_name if custom_event_name else ""
        
        st.success(get_text("GetTogether gestartet!", "GetTogether started!"))
        return True
    else:
        if not pin1 or not pin2:
            st.error(get_text("Bitte beide PIN-Felder ausfüllen.", "Please fill in both PIN fields."))
        elif pin1 != pin2:
            st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
        return False

def check_datenschutz_pin():
    if not st.session_state.datenschutz_pin_active:
        return True
    
    current_time = time.time()
    if current_time - st.session_state.last_activity_time > INACTIVITY_TIMEOUT:
        st.session_state.locked = True
    
    if st.session_state.locked:
        return datenschutz_pin_page()
    return True

def datenschutz_pin_page():
    st.title(get_text("Datenschutz-PIN erforderlich", "Data Protection PIN Required"))
    entered_pin = st.text_input(get_text("PIN eingeben", "Enter PIN"), type="password")
    
    if st.button(get_text("Entsperren", "Unlock")):
        if entered_pin == st.session_state.datenschutz_pin:
            st.session_state.locked = False
            st.session_state.last_activity_time = time.time()
            st.success(get_text("App entsperrt.", "App unlocked."))
            st.experimental_rerun()
            return True
        else:
            st.error(get_text("Falscher PIN.", "Incorrect PIN."))
    return False
