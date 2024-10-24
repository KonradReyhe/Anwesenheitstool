# auth.py

"""
This module handles authentication and authorization processes for the GetTogether application.
It includes functions for starting a GetTogether event, managing PINs, and handling data protection.
"""

# Import required libraries and modules
import streamlit as st
import time
import hmac
from config import INACTIVITY_TIMEOUT
from text_utils import get_text
from navigation import select_company_callback
from header import display_header

def compare_digest(a, b):
    """
    Securely compare two strings for equality.

    This function uses hmac.compare_digest to prevent timing attacks
    when comparing strings (e.g., passwords or PINs).

    Args:
        a (str): First string to compare.
        b (str): Second string to compare.

    Returns:
        bool: True if the strings are equal, False otherwise.
    """
    return hmac.compare_digest(a.encode(), b.encode())

def start_get_together(pin1, pin2, custom_event_name):
    """
    Start a new GetTogether event if the provided PINs match.

    This function validates the PINs, sets up the session state for a new event,
    and handles error messages if the PINs don't match or are missing.

    Args:
        pin1 (str): First PIN entered by the user.
        pin2 (str): Second PIN entered by the user for confirmation.
        custom_event_name (str): Optional custom name for the event.

    Returns:
        bool: True if the event was successfully started, False otherwise.
    """
    if pin1 and pin2 and compare_digest(pin1, pin2):
        # Set up session state for the new event
        st.session_state.update({
            'pin': pin1,
            'get_together_started': True,
            'custom_event_name': custom_event_name.strip() if custom_event_name else "",
            'page': 'select_company'
        })
        return True
    else:
        # Handle error cases
        if not pin1 or not pin2:
            st.error(get_text("Bitte beide PIN-Felder ausfüllen.", "Please fill in both PIN fields."))
        elif not compare_digest(pin1, pin2):
            st.error(get_text("Die eingegebenen PINs stimmen nicht überein.", "The entered PINs do not match."))
        return False

def check_datenschutz_pin():
    """
    Check if the data protection PIN is active and if the session is locked due to inactivity.

    This function manages the data protection PIN state and handles session locking
    based on user inactivity.

    Returns:
        bool: True if the PIN check passes or is not required, False otherwise.
    """
    # Check if data protection PIN is active
    if not st.session_state.datenschutz_pin_active:
        return True
    
    # Check for inactivity timeout
    current_time = time.time()
    if current_time - st.session_state.last_activity_time > INACTIVITY_TIMEOUT:
        st.session_state.locked = True
    
    # Handle locked state
    if st.session_state.locked:
        return datenschutz_pin_page()
    return True

def datenschutz_pin_page():
    """
    Display the data protection PIN entry page.
    This function handles the UI and logic for entering the data protection PIN.
    """
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
    """
    Callback function to start a new GetTogether event.
    This function is called when the user submits the start GetTogether form.
    """
    if start_get_together(st.session_state.pin1, st.session_state.pin2, st.session_state.custom_event_name_input):
        st.session_state.require_signature = st.session_state.require_signature_checkbox
        if st.session_state.datenschutz_pin_input:
            st.session_state.datenschutz_pin = st.session_state.datenschutz_pin_input
            st.session_state.datenschutz_pin_active = True
        st.session_state.page = 'select_company'
        st.rerun()
