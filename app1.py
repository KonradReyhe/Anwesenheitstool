# app1.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import pytz
import time
import os
import pandas as pd
from state_management import check_company_team_change
from auth import start_get_together
from attendance import (
    add_employee_to_attendance
)
from save_operations import save_attendance
from data_utils import get_companies, get_teams_for_company, get_employees_for_team
from ui_components import (
    select_company, select_team, display_company_team_info, display_employee_buttons,
    handle_signature_modal, display_success_messages, handle_undo_last_selection,
    toggle_language, display_header, signature_modal, guest_info, display_back_button
)
from admin import admin_panel
from utils import (
    get_text, end_get_together, auto_save_attendance, check_event_end,
    create_zip_file, generate_pdf, schedule_event_end, add_success_message,
    display_countdown_timer
)
from session_state import initialize_session_state, initialize_employee_session_state
from config import INACTIVITY_TIMEOUT
from styles import apply_custom_styles, VERSION
from timer import start_timer, check_timer, display_back_button
from navigation import return_to_company_selection, go_back_to_team_from_employee
from PIL import Image
from employee import select_employee

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
    
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    default_file = "Firmen_Teams_Mitarbeiter.csv"
    if default_file not in csv_files:
        csv_files.insert(0, default_file)
    
    selected_file = st.selectbox(
        get_text("Stammdaten-Datei auswählen:", "Select master data file:"),
        options=csv_files,
        index=csv_files.index(default_file) if default_file in csv_files else 0,
        key="selected_file_input"
    )
    st.session_state.selected_file = selected_file

    enable_auto_end = st.checkbox(get_text("Automatisches Ende aktivieren", "Enable automatic end"), key="enable_auto_end_input")
    
    if enable_auto_end:
        col1, col2 = st.columns(2)
        with col1:
            auto_end_hours = st.number_input(get_text("Stunden:", "Hours:"), min_value=0, max_value=23, value=1, step=1, key="auto_end_hours_input")
        with col2:
            auto_end_minutes = st.selectbox(get_text("Minuten:", "Minutes:"), options=[0, 15, 30, 45], index=0, key="auto_end_minutes_input")
        
        now = datetime.now(local_tz)
        end_time = now + timedelta(hours=auto_end_hours, minutes=auto_end_minutes)
        st.write(get_text(f"Geplantes Ende: {end_time.strftime('%d.%m.%Y %H:%M')}", f"Scheduled end: {end_time.strftime('%Y-%m-%d %H:%M')}"))
        
        accounting_email = st.text_input(get_text("E-Mail-Adresse für Buchhaltung:", "Email address for accounting:"), value=st.session_state.get('accounting_email', ''), key="accounting_email_input")
    else:
        auto_end_hours = None
        auto_end_minutes = None
        accounting_email = None

    datenschutz_pin = st.text_input(get_text("Datenschutz PIN setzen (optional):", "Set Data Protection PIN (optional):"), type="password", key="datenschutz_pin_input")
    
    require_signature = st.checkbox(get_text("Unterschrift von Mitarbeitern verlangen", "Require employee signature"), value=st.session_state.get('require_signature', False))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("Stammdaten aktualisieren", "Update Master Data")):
            st.session_state.page = 'update_master_data'
            st.rerun()
    
    with col2:
        if st.button(get_text("GetTogether beginnen", "Start GetTogether")):
            if start_get_together(pin1, pin2, custom_event_name):
                st.session_state.auto_end_hours = auto_end_hours if enable_auto_end else None
                st.session_state.auto_end_minutes = auto_end_minutes if enable_auto_end else None
                st.session_state.accounting_email = accounting_email
                st.session_state.require_signature = require_signature
                if enable_auto_end and auto_end_hours is not None and auto_end_minutes is not None:
                    now = datetime.now(local_tz)
                    end_time = now + timedelta(hours=auto_end_hours, minutes=auto_end_minutes)
                    schedule_event_end(end_time)
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

# Initialize session state at the end of the file
def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = False
    if 'admin_access_granted' not in st.session_state:
        st.session_state.admin_access_granted = False
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = None
    if 'selected_team' not in st.session_state:
        st.session_state.selected_team = None
    if 'selected_employee' not in st.session_state:
        st.session_state.selected_employee = None
    if 'added_employees' not in st.session_state:
        st.session_state.added_employees = []
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'countdown_start_time' not in st.session_state:
        st.session_state.countdown_start_time = None
    if 'success_messages' not in st.session_state:
        st.session_state.success_messages = []
    if 'last_message_time' not in st.session_state:
        st.session_state.last_message_time = None
    if 'all_employees_added_time' not in st.session_state:
        st.session_state.all_employees_added_time = None

initialize_session_state()

def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.experimental_rerun()

def display_header():
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'

    header_container = st.container()

    with header_container:
        title = get_text("GetTogether Anwesenheitstool", "GetTogether Attendance Tool")
        st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
        
        # Updated subtitle
        subtitle = get_text("Präsenz bei Firmenevents erfassen", "Record presence at company events")
        st.markdown(f"<div class='subtitle'>{subtitle}</div>", unsafe_allow_html=True)
        
        # Banner
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_dir = os.path.join(script_dir, "logos")
        banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")
        if os.path.exists(banner_path):
            try:
                # Read the image file as binary data
                with open(banner_path, "rb") as f:
                    banner_image = f.read()
                
                # Encode the image data to base64
                import base64
                encoded_image = base64.b64encode(banner_image).decode()
                
                # Create HTML for the image
                html = f"""
                <style>
                    .banner-container {{
                        width: 100%;
                        margin-bottom: 20px;
                    }}
                    .banner-image {{
                        width: 100%;
                        max-width: 100%;
                        height: auto;
                    }}
                </style>
                <div class="banner-container">
                    <img src="data:image/png;base64,{encoded_image}" class="banner-image" alt="Health Innovators Group Leipzig Banner">
                </div>
                """
                
                # Display the HTML
                st.markdown(html, unsafe_allow_html=True)
            except Exception as e:
                error_message = get_text("Fehler beim Laden des Banners:", "Error loading banner:")
                st.error(f"{error_message} {e}")
        else:
            warning_message = get_text("Banner wurde nicht gefunden:", "Banner not found:")
            st.warning(f"{warning_message} {banner_path}")

        # Admin settings button and language toggle
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.session_state.get_together_started:
                if st.button("⚙️", key="settings_button", help=get_text("Admin-Einstellungen", "Admin Settings")):
                    st.session_state.show_admin_panel = not st.session_state.show_admin_panel
                    st.rerun()
            
            language_toggle = "EN" if st.session_state.language == 'DE' else "DE"
            st.button(language_toggle, key="language_toggle", help=get_text("Sprache ändern", "Change language"), on_click=toggle_language)

    return header_container

def select_company_callback(company):
    if company in ["Externe Partner", "External Partners"]:
        st.session_state.selected_company = "Externe Partner"  # Always use the German version for CSV lookup
    else:
        st.session_state.selected_company = company

    if company in [get_text("Gast", "Guest"), "Gast", "Guest"]:  # Check for both German and English versions
        st.session_state.page = 'guest_info'
    else:
        st.session_state.page = 'select_team'

def update_master_data():
    st.title(get_text("Stammdaten aktualisieren", "Update Master Data"))
    # Add functionality to update master data here
    # For now, we'll just add a placeholder message
    st.info(get_text("Funktion zum Aktualisieren der Stammdaten wird hier implementiert.", 
                     "Functionality to update master data will be implemented here."))
    if st.button(get_text("Zurück", "Back")):
        st.session_state.page = 'home'
        st.rerun()

def select_team_callback(team):
    st.session_state.selected_team = team
    st.session_state.page = 'select_employee'
    st.rerun()
