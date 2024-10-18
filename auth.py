import streamlit as st
import time
from config import INACTIVITY_TIMEOUT
from streamlit import rerun
from text_utils import get_text

def start_get_together(pin1, pin2, custom_event_name):
    if pin1 and pin2 and pin1 == pin2:
        st.session_state.pin = pin1
        st.session_state.get_together_started = True
        st.session_state.custom_event_name = custom_event_name
        st.session_state.last_activity_time = time.time()
        st.success(get_text("GetTogether wurde gestartet.", "GetTogether has been started."))
        return True
    else:
        st.error(get_text("PINs stimmen nicht überein oder sind leer.", "PINs do not match or are empty."))
        return False

def check_datenschutz_pin(entered_pin):
    if entered_pin == st.session_state.datenschutz_pin:
        st.session_state.datenschutz_pin_active = False
        st.success(get_text("Datenschutz-PIN korrekt. Zugriff gewährt.", "Data protection PIN correct. Access granted."))
        rerun()
    else:
        st.error(get_text("Falscher Datenschutz-PIN.", "Incorrect data protection PIN."))

def datenschutz_pin_page():
    st.title(get_text("Datenschutz-PIN erforderlich", "Data Protection PIN Required"))
    entered_pin = st.text_input(get_text("Bitte geben Sie den Datenschutz-PIN ein:", "Please enter the data protection PIN:"), type="password")
    if st.button(get_text("Bestätigen", "Confirm")):
        check_datenschutz_pin(entered_pin)

__all__ = ['start_get_together', 'check_datenschutz_pin', 'datenschutz_pin_page']
