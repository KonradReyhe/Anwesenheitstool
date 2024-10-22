# app1.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pytz
import sys
from streamlit.runtime.scriptrunner import RerunException, StopException
import asyncio

from auth import start_get_together, start_get_together_callback
from ui_components import (
    select_company, select_team, select_employee, guest_info, 
)
from header import display_header
from session_state import initialize_session_state
from styles import apply_custom_styles
from utils import check_event_end
from text_utils import get_text
from utils import display_countdown_timer
from admin import admin_settings, update_master_data, admin_panel

local_tz = pytz.timezone('Europe/Berlin')

def home():
    display_header()
    st.markdown(f"<div class='sub-header'>{get_text('GetTogether konfigurieren:', 'Configure GetTogether:')}</div>", unsafe_allow_html=True)
    
    with st.form(key='start_gettogether_form'):
        col1, col2 = st.columns(2)
        with col1:
            pin1 = st.text_input(get_text("Setzen Sie einen PIN:", "Set a PIN:"), type="password", key="pin1")
        with col2:
            pin2 = st.text_input(get_text("Bestätigen Sie den PIN:", "Confirm the PIN:"), type="password", key="pin2")
        
        custom_event_name = st.text_input(get_text("Name des Events (optional):", "Event name (optional):"), key="custom_event_name_input")
        
        datenschutz_pin = st.text_input(get_text("Datenschutz PIN setzen (optional):", "Set Data Protection PIN (optional):"), type="password", key="datenschutz_pin_input")
        
        require_signature = st.checkbox(get_text("Unterschrift von Mitarbeitern verlangen", "Require employee signature"), value=st.session_state.get('require_signature', False), key="require_signature_checkbox")
        
        if st.form_submit_button(get_text("GetTogether beginnen", "Start GetTogether")):
            start_get_together_callback()

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
        if st.session_state.get('admin_access_granted', False):
            admin_settings()
        else:
            st.session_state.page = 'select_company'
    else:
        st.error("Invalid page")

async def main():
    try:
        initialize_session_state()
        apply_custom_styles()
        
        if not st.session_state.get('get_together_started', False):
            home()
        else:
            if st.session_state.page == 'select_company':
                select_company()
            elif st.session_state.page == 'select_team':
                select_team()
            elif st.session_state.page == 'select_employee':
                select_employee()
            elif st.session_state.page == 'guest_info':
                guest_info()
            elif st.session_state.page == 'admin_settings':
                admin_settings()
        
        await check_event_end()
        await asyncio.sleep(0)  # Allow other coroutines to run
        st_autorefresh(interval=30000, key="datarefresh")  # 30 seconds instead of 5
    except (RerunException, StopException):
        raise
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.stop()

if __name__ == "__main__":
    asyncio.run(main())

