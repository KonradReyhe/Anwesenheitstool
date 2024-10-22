# ui_components.py

import streamlit as st
from text_utils import get_text
from data_utils import get_companies, get_teams_for_company, get_employees_for_team
from attendance import add_employee_to_attendance, undo_last_employee_selection, auto_save_attendance
from timer import start_timer
import time
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import math
from math import ceil
from datetime import datetime
import os
import base64
from navigation import (
    return_to_company_selection, go_back_to_team_from_employee,
    select_company_callback, select_team_callback, go_back_to_company
)
import pytz
from io import BytesIO
from header import display_header
from admin import admin_panel
import threading


local_tz = pytz.timezone('Europe/Berlin')  


def handle_employee_selection(employee):
    if employee not in st.session_state.added_employees:
        add_employee_to_attendance(employee)
        st.session_state.current_employee = employee
        
        if st.session_state.require_signature:
            st.session_state.show_signature_modal = True
        
        
        
        start_timer()

def display_success_messages():
    if st.session_state.success_messages:
        with st.container():
            for message in st.session_state.success_messages:
                st.success(message)
        
        current_time = time.time()
        if st.session_state.last_message_time is None:
            st.session_state.last_message_time = current_time
        
        # If 5 seconds have passed since the message was set, clear the messages
        if current_time - st.session_state.last_message_time > 5:
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
                st.session_state.selected_team = team
                st.session_state.page = 'select_employee'
                st.rerun()

    if st.button(get_text("Zurück", "Back"), key="back_to_company", use_container_width=True):
        st.session_state.selected_company = None
        st.session_state.page = 'select_company'
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
                stroke_width=2,
                stroke_color="#000000",
                background_color="#ffffff",
                height=100,  # Reduced height
                width=300,   # Reduced width
                drawing_mode="freedraw",
                key="canvas",
            )
            submitted = st.form_submit_button(get_text("Unterschrift bestätigen", "Confirm Signature"))
        
        if submitted and canvas_result.image_data is not None:
            # Process signature asynchronously
            threading.Thread(target=process_signature, args=(canvas_result.image_data, st.session_state.current_employee)).start()
            st.session_state.show_signature_modal = False
            # Removed st.experimental_rerun()

def process_signature(image_data, employee):
    signature_path = f"signatures/{employee}_{int(time.time())}.png"
    Image.fromarray(image_data.astype('uint8')).save(signature_path)
    st.session_state.signatures[employee] = signature_path
    add_employee_to_attendance(employee)

def handle_signature_modal():
    if st.session_state.get('show_signature_modal', False):
        signature_modal()

def select_company():
    display_header()
    
    if st.session_state.show_admin_panel:
        entered_pin = st.text_input(get_text("Admin PIN eingeben", "Enter Admin PIN"), type="password", key="admin_pin_input")
        if st.button("Enter", key="admin_pin_enter"):
            if entered_pin == st.session_state.pin:
                st.session_state.admin_access_granted = True
                st.session_state.page = 'admin_settings'
            else:
                st.error(get_text("Falscher Admin PIN.", "Incorrect Admin PIN."))
        if st.button(get_text("Abbrechen", "Cancel"), key="cancel_admin_panel"):
            st.session_state.show_admin_panel = False
    
    
    display_success_messages()
    
    if st.session_state.custom_event_name:
        st.markdown(f"<div class='event-name'>{st.session_state.custom_event_name}</div>", unsafe_allow_html=True)
    
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
    
    # Add yellow dividing line with increased margin
    st.markdown("<hr style='border: 2px solid #f9c61e; margin-top: 40px; margin-bottom: 40px;'>", unsafe_allow_html=True)
    
    # Display special companies with increased spacing
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    special_cols = st.columns(3)
    for i, company in enumerate(special_companies):
        with special_cols[i]:
            display_company_button(company)
    
    # Add extra space at the bottom
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

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
    if st.button(company, key=f"company_button_{company}", use_container_width=True):
        select_company_callback(company)
        # Removed st.rerun()

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()



def display_company_team_info():
    if st.session_state.selected_company:
        st.markdown(
            f"<div class='company-info'>{get_text('Ausgewählte Firma:', 'Selected Company:')} {st.session_state.selected_company}</div>", 
            unsafe_allow_html=True
        )
    if st.session_state.selected_team:
        st.markdown(
            f"<div class='team-info'>{get_text('Ausgewähltes Team:', 'Selected Team:')} {st.session_state.selected_team}</div>", 
            unsafe_allow_html=True
        )

def guest_info():
    display_header()
    
    st.markdown(f"<div class='sub-header'>{get_text('Gast-Information', 'Guest Information')}</div>", unsafe_allow_html=True)
    
    st.session_state.guest_name = st.text_input(get_text("Name des Gastes", "Guest Name"))
    st.session_state.guest_company = st.text_input(get_text("Firma des Gastes (optional)", "Guest Company (optional)"))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("Bestätigen", "Confirm"), use_container_width=True):
            submit_guest()
    with col2:
        if st.button(get_text("Zurück", "Back"), use_container_width=True):
            st.session_state.page = 'select_company'
            st.rerun()

def submit_guest():
    if st.session_state.guest_name:
        now = datetime.now()
        new_record = {
            'ID': f"Guest_{now.strftime('%Y%m%d%H%M%S')}",
            'Name': st.session_state.guest_name,
            'Firma': st.session_state.guest_company if st.session_state.guest_company else get_text("Nicht angegeben", "Not specified"),
            'Team': 'Guest',
            'Zeit': now.strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.attendance_data.append(new_record)
        auto_save_attendance()
        
        success_message = get_text(
            f'Gast "{st.session_state.guest_name}" wurde zur Anwesenheitsliste hinzugefügt.',
            f'Guest "{st.session_state.guest_name}" has been added to the attendance list.'
        )
        st.session_state.success_messages.append(success_message)
        st.session_state.last_message_time = time.time()
        
        st.session_state.page = 'select_company'
        st.rerun()
    else:
        st.error(get_text("Bitte geben Sie mindestens den Namen des Gastes ein.", "Please enter at least the guest's name."))

__all__ = [
    'select_company',
    'select_team',
    'select_employee',
    'guest_info',
    'display_back_button',
    'display_company_team_info',
    'display_employee_buttons',
    'handle_signature_modal',
    'display_success_messages',
    'handle_undo_last_selection',
    'signature_modal',
]


def select_employee():
    if not check_employee_pin():
        return

    display_header()
    display_company_team_info()
    
    employees = get_employees_for_team(st.session_state.selected_company, st.session_state.selected_team)
    if not employees:
        st.warning(get_text("Keine Mitarbeiter für dieses Team gefunden.", "No employees found for this team."))
        return

    st.markdown(f"<div class='sub-header'>{get_text('Mitarbeiter auswählen:', 'Select employee:')}</div>", unsafe_allow_html=True)
    
    num_columns = 3
    columns = st.columns(num_columns)
    
    for i, employee in enumerate(employees):
        with columns[i % num_columns]:
            if st.button(employee, key=f"employee_{employee}_{i}", use_container_width=True):
                add_employee_to_attendance(employee)
                st.session_state.page = 'select_company'
                st.rerun()

    # Add back button
    if st.button(get_text("Zurück", "Back"), key="back_to_team", use_container_width=True):
        st.session_state.selected_team = None
        st.session_state.page = 'select_team'
        st.rerun()

    handle_undo_last_selection()

def check_employee_pin():
    if 'employee_pin_required' in st.session_state and st.session_state.employee_pin_required:
        pin = st.text_input(get_text("PIN eingeben:", "Enter PIN:"), type="password")
        if st.button(get_text("Bestätigen", "Confirm")):
            if pin == st.session_state.employee_pin:
                return True
            else:
                st.error(get_text("Falsche PIN. Bitte versuchen Sie es erneut.", "Incorrect PIN. Please try again."))
                return False
    else:
        return True

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

def select_employee_callback(employee):
    now = datetime.now()
    new_record = {
        'ID': f"{employee}_{now.strftime('%Y%m%d%H%M%S')}",
        'Name': employee,
        'Firma': st.session_state.selected_company,
        'Team': st.session_state.selected_team,
        'Zeit': now.strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.attendance_data.append(new_record)
    auto_save_attendance()
    

def check_all_employees_added(employees):
    if st.session_state.all_employees_added_time:
        time_since_all_added = time.time() - st.session_state.all_employees_added_time
        if time_since_all_added <= 5:
            st.info(get_text(f"Alle Teammitglieder wurden hinzugefügt. Kehre in {5 - int(time_since_all_added)} Sekunden zur Firmenauswahl zurück...",
                             f"All team members have been added. Returning to company selection in {5 - int(time_since_all_added)} seconds..."))
        else:
            return_to_company_selection()
    elif set(st.session_state.added_employees) == set(employees):
        st.session_state.all_employees_added_time = time.time()





































st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .special-companies {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

























