# app1.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pytz

from auth import start_get_together
from ui_components import (
    select_company, select_team, select_employee, guest_info, display_back_button
)
from header import display_header
from session_state import initialize_session_state
from styles import apply_custom_styles
from utils import check_event_end
from text_utils import get_text
from utils import display_countdown_timer
from admin import admin_settings, update_master_data


local_tz = pytz.timezone('Europe/Berlin')

def home():
    display_header()
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether konfigurieren:', 'Configure GetTogether:')}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pin1 = st.text_input(get_text("Setzen Sie einen PIN:", "Set a PIN:"), type="password", key="pin1")
    with col2:
        pin2 = st.text_input(get_text("Bestätigen Sie den PIN:", "Confirm the PIN:"), type="password", key="pin2")
    
    custom_event_name = st.text_input(get_text("Name des Events (optional):", "Event name (optional):"), key="custom_event_name_input")
    
    datenschutz_pin = st.text_input(get_text("Datenschutz PIN setzen (optional):", "Set Data Protection PIN (optional):"), type="password", key="datenschutz_pin_input")
    
    require_signature = st.checkbox(get_text("Unterschrift von Mitarbeitern verlangen", "Require employee signature"), value=st.session_state.get('require_signature', False))
    
    if st.button(get_text("GetTogether beginnen", "Start GetTogether")):
        if start_get_together(pin1, pin2, custom_event_name):
            st.session_state.require_signature = require_signature
            if datenschutz_pin:
                st.session_state.datenschutz_pin = datenschutz_pin
                st.session_state.datenschutz_pin_active = True
            st.session_state.page = 'select_company'
            st.rerun()

def navigate():
    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'select_company':
        select_company()
    elif st.session_state.page == 'select_team':
        select_team()
    elif st.session_state.page == 'select_employee':
        select_employee()
    elif st.session_state.page == 'guest_info':
        guest_info()
    elif st.session_state.page == 'update_master_data':
        update_master_data()
    elif st.session_state.page == 'admin_settings':
        admin_settings()
    else:
        st.error("Invalid page")

def main():
    initialize_session_state()
    apply_custom_styles()
    st_autorefresh(interval=1000, key="autorefresh_main")
    check_event_end()
    display_countdown_timer()
    navigate()

if __name__ == "__main__":
    main()