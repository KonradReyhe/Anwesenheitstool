# app1.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import pytz
import time
import os
from auth import start_get_together
from attendance import (
    get_employees_for_company_team, add_employee_to_attendance, get_companies, 
    get_teams_for_company, check_company_team_change, check_all_employees_added, 
    get_employees_for_team, save_attendance, undo_last_employee_selection,
    submit_guest
)
from ui_components import (
    select_company, select_team, display_company_team_info, display_employee_buttons,
    handle_signature_modal, display_success_messages, handle_undo_last_selection,
    admin_panel, toggle_language, display_header, signature_modal, guest_info
)
from utils import (
    get_text, end_get_together, auto_save_attendance, check_event_end,
    create_zip_file, generate_pdf, send_email, schedule_event_end, add_success_message,
    display_countdown_timer
)
from session_state import initialize_session_state, initialize_employee_session_state
from config import INACTIVITY_TIMEOUT
from styles import apply_custom_styles, VERSION
from timer import start_timer, check_timer, display_back_button
from navigation import return_to_company_selection, go_back_to_team_from_employee
from admin import admin_settings, confirm_end_get_together, update_master_data
from employee import select_employee
from email_utils import send_documents_to_accounting

local_tz = pytz.timezone('Europe/Berlin')

def home():
    st.title(get_text("GetTogether", "GetTogether"))
    pin1 = st.text_input(get_text("PIN eingeben", "Enter PIN"), type="password")
    pin2 = st.text_input(get_text("PIN bestätigen", "Confirm PIN"), type="password")
    custom_event_name = st.text_input(get_text("Benutzerdefinierter Event-Name (optional)", "Custom Event Name (optional)"))
    end_time = st.time_input(get_text("Ende des Events (optional)", "Event End Time (optional)"), value=None)
    datenschutz_pin = st.text_input(get_text("Datenschutz PIN (optional)", "Data Protection PIN (optional)"), type="password")
    require_signature = st.checkbox(get_text("Unterschrift erforderlich", "Signature required"))
    
    # File selection for master data
    st.session_state.selected_file = st.selectbox(
        get_text("Stammdaten-Datei auswählen", "Select Master Data File"),
        options=["Firmen_Teams_Mitarbeiter.csv"] + [f for f in os.listdir() if f.endswith('.csv')],
        index=0
    )

    # Optional automatic end settings
    auto_end = st.checkbox(get_text("Automatisches Ende aktivieren", "Activate Automatic End"))
    if auto_end:
        end_date = st.date_input(get_text("Enddatum", "End Date"))
        end_time = st.time_input(get_text("Endzeit", "End Time"))
        end_datetime = datetime.combine(end_date, end_time)
        st.session_state.end_time = end_datetime
    
    if st.button(get_text("GetTogether starten", "Start GetTogether")):
        if start_get_together(pin1, pin2, custom_event_name):
            if end_time:
                now = datetime.now(local_tz)
                combined_end_time = datetime.combine(now.date(), end_time)
                if combined_end_time < now:
                    combined_end_time += timedelta(days=1)  # Move to the next day if time has passed
                schedule_event_end(combined_end_time.astimezone(local_tz))
            if datenschutz_pin:
                st.session_state.datenschutz_pin = datenschutz_pin
                st.session_state.datenschutz_pin_active = True
            st.session_state.require_signature = require_signature
            st.session_state.page = 'select_company'
            st.experimental_rerun()

def navigate():
    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'select_company':
        select_company()
    elif st.session_state.page == 'guest_info':
        guest_info()
    elif st.session_state.page == 'select_team':
        select_team()
    elif st.session_state.page == 'select_employee':
        select_employee()
    elif st.session_state.page == 'admin_settings':
        admin_settings()
    elif st.session_state.page == 'update_master_data':
        update_master_data()
    else:
        st.error("Invalid page")

def main():
    initialize_session_state()
    apply_custom_styles()
    st_autorefresh(interval=1000, key="autorefresh")
    check_event_end()
    display_countdown_timer()
    navigate()

def update_last_activity():
    st.session_state.last_activity_time = time.time()

# Call this function after every user interaction

if __name__ == "__main__":
    main()

# Initialize session state at the end of the file
initialize_session_state()

def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.experimental_rerun()
