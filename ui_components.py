#ui_components.py
import streamlit as st
from utils import get_text, auto_save_attendance, display_countdown_timer, end_get_together
from language_utils import toggle_language
from data_utils import get_companies, get_teams_for_company
from message_utils import show_custom_employee_message
from attendance import undo_last_employee_selection, add_employee_to_attendance
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

VERSION = "1.0.0"

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
        else:
            add_success_message(employee)
        
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

def add_success_message(employee):
    new_message = get_text(
        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
        f'Employee "{employee}" has been added to the attendance list.'
    )
    st.session_state.success_messages.append(new_message)
    st.session_state.last_message_time = time.time()

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

def display_header():
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'

    header_container = st.container()

    with header_container:
        title = get_text("GetTogether Anwesenheitstool", "GetTogether Attendance Tool")
        st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
        
        subtitle = get_text("Präsenz bei Firmenevents erfassen", "Record presence at company events")
        st.markdown(f"<div class='subtitle'>{subtitle}</div>", unsafe_allow_html=True)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_dir = os.path.join(script_dir, "logos")
        banner_path = os.path.join(logo_dir, "HealthInnovatorsGroupLeipzig-Banner.png")
        if os.path.exists(banner_path):
            try:
                with open(banner_path, "rb") as f:
                    banner_image = f.read()
                
                encoded_image = base64.b64encode(banner_image).decode()
                
                html = f"""
                <div class="banner-container">
                    <img src="data:image/png;base64,{encoded_image}" class="banner-image" alt="Health Innovators Group Leipzig Banner">
                </div>
                """
                
                st.markdown(html, unsafe_allow_html=True)
            except Exception as e:
                error_message = get_text("Fehler beim Laden des Banners:", "Error loading banner:")
                st.error(f"{error_message} {e}")
        else:
            warning_message = get_text("Banner wurde nicht gefunden:", "Banner not found:")
            st.warning(f"{warning_message} {banner_path}")

        col1, col2 = st.columns([9, 1])
        with col2:
            if st.session_state.get('get_together_started', False):
                if st.button("⚙️", key="settings_button", help=get_text("Admin-Einstellungen", "Admin Settings")):
                    st.session_state.show_admin_panel = not st.session_state.get('show_admin_panel', False)
                    st.rerun()
            
            language_toggle = "EN" if st.session_state.language == 'DE' else "DE"
            st.button(language_toggle, key="language_toggle", help=get_text("Sprache ändern", "Change language"), on_click=toggle_language)

    st.markdown(f"<div class='version-number'>v{VERSION}</div>", unsafe_allow_html=True)

    return header_container

def handle_signature_modal():
    if st.session_state.get('show_signature_modal', False):
        signature_modal()

def select_company():
    if not check_datenschutz_pin():
        return

    display_header()
    
    display_countdown_timer()
    
    if st.session_state.get('custom_message'):
        st.markdown(
            f"""
            <div class='custom-message'>
                {st.session_state.custom_message}
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown(f"<div class='event-name'>{st.session_state.custom_event_name}</div>", unsafe_allow_html=True)
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_dir = os.path.join(script_dir, "logos")
        company_logos = {
            "4K Analytics": os.path.join(logo_dir, "4K_ANALYTICS.png"),
            "CLINIBOTS": os.path.join(logo_dir, "CLINIBOTS.png"),
            "GREENBAY research": os.path.join(logo_dir, "GREENBAY_research.png"),
            "InfAI Management": os.path.join(logo_dir, "InfAI_Management.png"),
            "iNNO3": os.path.join(logo_dir, "iNNO3.png"),
            "Lieblingsimmobilien": os.path.join(logo_dir, "Lieblingsimmobilien.png"),
            "Termingo": os.path.join(logo_dir, "TERMINGO.png"),
            "Visgato": os.path.join(logo_dir, "visgato.png"),
            "WIG2": os.path.join(logo_dir, "WIG2.png"),
        }
        st.markdown(f"<div class='important-text'>{get_text('Bitte wählen Sie eine Firma aus, um Ihre Anwesenheit zu bestätigen:', 'Please select a company to confirm your attendance:')}</div>", unsafe_allow_html=True)
        
        num_cols = 3
        company_list_with_logos = list(company_logos.keys())
        companies_per_row = [company_list_with_logos[i:i + num_cols] for i in range(0, len(company_list_with_logos), num_cols)]
        
        for row in companies_per_row:
            cols = st.columns(num_cols)
            for col, company in zip(cols, row):
                with col:
                    if company in company_logos:
                        logo_path = company_logos.get(company)
                        if logo_path and os.path.exists(logo_path):
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

        st.markdown("<hr style='border-top: 2px solid #f9c61e; margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='important-text'>{get_text('Weitere Auswahl:', 'Additional options:')}</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            st.button("iLOC", key="iLOC", on_click=select_company_callback, args=("iLOC",), use_container_width=True)
        with cols[1]:
            external_partners = get_text("Externe Partner", "External Partners")
            st.button(external_partners, key="Externe Partner", on_click=select_company_callback, args=(external_partners,), use_container_width=True)
        with cols[2]:
            guest = get_text("Gast", "Guest")
            st.button(guest, key="Guest", on_click=select_company_callback, args=(guest,), use_container_width=True)
    st.session_state.last_activity_time = time.time()

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





