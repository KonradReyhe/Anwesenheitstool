# auth.py

import streamlit as st
import time
from config import INACTIVITY_TIMEOUT
from text_utils import get_text
from navigation import select_company_callback
from header import display_header


def start_get_together(pin1, pin2, custom_event_name):
    if pin1 and pin2 and pin1 == pin2:
        st.session_state.update({
            'pin': pin1,
            'get_together_started': True,
            'custom_event_name': custom_event_name.strip() if custom_event_name else "",
            'page': 'select_company'
        })
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
    display_header()
    
    st.markdown(f"<div class='sub-header'>{get_text('Datenschutz-PIN eingeben:', 'Enter Data Protection PIN:')}</div>", unsafe_allow_html=True)
    
    entered_pin = st.text_input(get_text("PIN:", "PIN:"), type="password", key="datenschutz_pin_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("Bestätigen", "Confirm"), use_container_width=True):
            if entered_pin == st.session_state.datenschutz_pin:
                select_company_callback(st.session_state.selected_company_temp)
                st.session_state.page = 'select_team'
                st.rerun()
            else:
                st.error(get_text("Falscher PIN. Bitte versuchen Sie es erneut.", "Incorrect PIN. Please try again."))
    
    with col2:
        if st.button(get_text("Abbrechen", "Cancel"), use_container_width=True):
            st.session_state.page = 'select_company'
            st.session_state.selected_company_temp = None
            st.rerun()

def start_get_together_callback():
    if start_get_together(st.session_state.pin1, st.session_state.pin2, st.session_state.custom_event_name_input):
        st.session_state.require_signature = st.session_state.require_signature_checkbox
        if st.session_state.datenschutz_pin_input:
            st.session_state.datenschutz_pin = st.session_state.datenschutz_pin_input
            st.session_state.datenschutz_pin_active = True
        st.session_state.page = 'select_company'
        st.rerun()

