#ui_components.py
from config import VERSION
import streamlit as st
from utils import get_text, display_countdown_timer, end_get_together, add_success_message, auto_save_attendance
from language_utils import toggle_language
from data_utils import get_companies, get_teams_for_company
from message_utils import show_custom_employee_message
from attendance_functions import add_employee_to_attendance
from timer import start_timer
import time
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import math
from math import ceil
from datetime import datetime
import os
import base64
from auth import check_datenschutz_pin
from admin import admin_panel
from navigation import return_to_company_selection, go_back_to_team_from_employee, select_company_callback, go_back_to_company
import pytz
from io import BytesIO
from header_utils import display_header
from attendance import undo_last_employee_selection, add_employee_to_attendance

local_tz = pytz.timezone('Europe/Berlin')  # Replace with your actual timezone

def display_employee_buttons(employees):
    num_cols = min(3, len(employees))
    num_rows = ceil(len(employees) / num_cols)
    
    container = st.container()
    with container:
        for row in range(num_rows):
            cols = st.columns(num_cols)
            for col in range(num_cols):
                idx = row * num_cols + col
                if idx < len(employees):
                    with cols[col]:
                        employee = employees[idx]
                        is_added = employee in st.session_state.added_employees
                        button_key = f"employee_{employee}_{idx}"
                        
                        if st.button(employee, key=button_key, use_container_width=True, 
                                     disabled=is_added):
                            handle_employee_selection(employee)
                        
                        if is_added:
                            apply_selected_button_style(button_key)

def handle_employee_selection(employee):
    if employee not in st.session_state.added_employees:
        add_employee_to_attendance(employee)
        st.session_state.current_employee = employee
        
        if st.session_state.require_signature:
            st.session_state.show_signature_modal = True
        
        if employee in st.session_state.custom_employee_messages:
            show_custom_employee_message(employee)
        
        start_timer()
        st.rerun()

def display_success_messages():
    with st.container():
        for message in st.session_state.success_messages:
            st.success(message)
    
    current_time = time.time()
    if st.session_state.last_message_time and current_time - st.session_state.last_message_time > 5:
        st.session_state.success_messages = []
        st.session_state.last_message_time = None

def handle_undo_last_selection():
    if st.session_state.added_employees:
        if st.button(get_text("Letzte Auswahl rückgängig machen", "Undo last selection"), 
                     key="undo_last_selection",
                     use_container_width=True):
            undo_last_employee_selection()

def select_team():
    display_header()
    display_company_team_info()
    
    teams = get_teams_for_company(st.session_state.selected_company)
    st.markdown(f"<div class='sub-header'>{get_text('Team auswählen:', 'Select team:')}</div>", unsafe_allow_html=True)
    
    num_columns = 3
    columns = st.columns(num_columns)
    
    for i, team in enumerate(teams):
        with columns[i % num_columns]:
            if st.button(team, key=f"team_{team}", use_container_width=True):
                select_team_callback(team)
    
    display_back_button()

def select_team_callback(team):
    st.session_state.selected_team = team
    st.session_state.page = 'select_employee'
    st.rerun()

def apply_selected_button_style(button_key):
    st.markdown(f"""
        <style>
        #{button_key} {{
            background-color: #f9c61e !important;
            color: #ffffff !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def signature_modal():
    if st.session_state.show_signature_modal:
        with st.form(key='signature_form'):
            st.write(get_text("Bitte unterschreiben Sie hier:", "Please sign here:"))
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="#000000",
                background_color="#ffffff",
                height=150,
                width=400,
                drawing_mode="freedraw",
                key="canvas",
            )
            submitted = st.form_submit_button(get_text("Unterschrift bestätigen", "Confirm Signature"))
            
        if submitted and canvas_result.image_data is not None:
            # Save the signature
            signature_path = f"signatures/{st.session_state.current_employee}_{int(time.time())}.png"
            Image.fromarray(canvas_result.image_data.astype('uint8')).save(signature_path)
            st.session_state.signatures[st.session_state.current_employee] = signature_path
            
            # Add employee to attendance
            add_employee_to_attendance(st.session_state.current_employee)
            
            st.session_state.show_signature_modal = False
            st.rerun()


def handle_signature_modal():
    if st.session_state.get('show_signature_modal', False):
        signature_modal()

def select_company():
    display_header()
    
    st.markdown(f"<div class='important-text'>{get_text('Bitte wählen Sie eine Firma aus, um Ihre Anwesenheit zu bestätigen:', 'Please select a company to confirm your attendance:')}</div>", unsafe_allow_html=True)
    
    companies = get_companies()
    num_cols = 3
    regular_companies = [c for c in companies if c not in ["iLOC", "Externe Partner", get_text("Gast", "Guest")]]
    special_companies = ["iLOC", "Externe Partner", get_text("Gast", "Guest")]
    
    # Display regular companies
    company_rows = [regular_companies[i:i + num_cols] for i in range(0, len(regular_companies), num_cols)]
    for row in company_rows:
        cols = st.columns(num_cols)
        for col, company in zip(cols, row):
            with col:
                display_company_button(company)
    
    # Display special companies at the bottom
    st.markdown("<div class='company-divider'></div>", unsafe_allow_html=True)
    special_cols = st.columns(3)
    for i, company in enumerate(special_companies):
        with special_cols[i]:
            display_company_button(company)
    
    display_back_button()

def display_company_button(company):
    logo_path = f"logos/{company.lower().replace(' ', '_')}.png"
    if os.path.exists(logo_path):
        logo_base64 = base64.b64encode(open(logo_path, 'rb').read()).decode()
        st.markdown(
            f"""
            <div class="company-container">
                <img class="company-logo" src="data:image/png;base64,{logo_base64}" alt="{company}" />
            </div>
            """, 
            unsafe_allow_html=True
        )
    st.button(company, key=company, on_click=select_company_callback, args=(company,), use_container_width=True)

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def select_company_callback(company):
    st.session_state.selected_company = company
    if company == get_text("Gast", "Guest"):
        st.session_state.page = 'guest_info'
    else:
        st.session_state.page = 'select_team'
    st.rerun()

def display_company_team_info():
    if st.session_state.selected_company:
        st.markdown(f"<div class='company-info'>{get_text('Ausgewählte Firma:', 'Selected Company:')} {st.session_state.selected_company}</div>", unsafe_allow_html=True)
    if st.session_state.selected_team:
        st.markdown(f"<div class='team-info'>{get_text('Ausgewähltes Team:', 'Selected Team:')} {st.session_state.selected_team}</div>", unsafe_allow_html=True)

def guest_info():
    st.title(get_text("Gast-Information", "Guest Information"))
    st.session_state.guest_name = st.text_input(get_text("Name des Gastes", "Guest Name"))
    st.session_state.guest_company = st.text_input(get_text("Firma des Gastes", "Guest Company"))
    if st.button(get_text("Bestätigen", "Confirm")):
        submit_guest()

def submit_guest():
    if st.session_state.guest_name and st.session_state.guest_company:
        now = datetime.now()
        new_record = {
            'ID': f"Guest_{now.strftime('%Y%m%d%H%M%S')}",
            'Name': st.session_state.guest_name,
            'Firma': st.session_state.guest_company,
            'Team': 'Guest',
            'Zeit': now.strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.attendance_data.append(new_record)
        auto_save_attendance()
        st.success(get_text(f"Gast {st.session_state.guest_name} wurde hinzugefügt.", 
                            f"Guest {st.session_state.guest_name} has been added."))
        st.session_state.page = 'select_company'
        st.experimental_rerun()
    else:
        st.error(get_text("Bitte füllen Sie alle Felder aus.", "Please fill in all fields."))

def display_countdown_timer():
    if st.session_state.end_time and st.session_state.get_together_started:
        now = datetime.now(local_tz)
        time_remaining = st.session_state.end_time - now
        if time_remaining.total_seconds() > 0:
            days, remainder = divmod(time_remaining.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            countdown_text = get_text(
                f"Verbleibende Zeit: {int(days)} T, {int(hours)} Std, {int(minutes)} Min",
                f"Time remaining: {int(days)}d, {int(hours)}h, {int(minutes)}m"
            )
            
            st.markdown(
                f"""
                <div style="
                    position: fixed;
                    top: 10px;
                    right: 10px;
                    background-color: rgba(249, 198, 30, 0.1);
                    color: #888888;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    z-index: 1000;
                ">
                    {countdown_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning(get_text("Das Event ist beendet!", "The event has ended!"))
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()

def display_back_button():
    if st.button(get_text("Zurück zur Firmenauswahl", "Back to company selection"), key="back_button"):
        go_back_to_company()
    
    # Check if timer is active (only if not all employees have been added)
    if st.session_state.timer_active and st.session_state.countdown_start_time and not st.session_state.all_employees_added_time:
        # Calculate remaining time
        elapsed_time = time.time() - st.session_state.countdown_start_time
        remaining_time = max(0, 30 - int(elapsed_time))  # 30 seconds timer
        
        # Display countdown
        st.info(f"{get_text('Zurück zur Firmenauswahl in', 'Back to company selection in')} {remaining_time} {get_text('Sekunden...', 'seconds...')}")
        
        # If the countdown is finished, reset and go back to company selection
        if remaining_time == 0:
            go_back_to_company()

__all__ = ['select_company', 'select_team', 'display_company_team_info', 'display_employee_buttons',
           'handle_signature_modal', 'display_success_messages', 'handle_undo_last_selection',
           'toggle_language', 'display_header', 'signature_modal', 'guest_info', 'display_back_button']

def display_language_toggle():
    # Implement language toggle functionality here
    pass

def display_version():
    # Implement version display functionality here
    st.text(f"Version: {VERSION}")  # Make sure to import VERSION from the appropriate module











