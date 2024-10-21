#employee.py
import streamlit as st
import time
from data_utils import get_employees_for_team
from utils import get_text, add_success_message, auto_save_attendance, update_last_activity
from attendance import (
    add_employee_to_attendance
)
from state_management import check_company_team_change
from ui_components import (
    display_header, 
    display_company_team_info, 
    show_custom_employee_message,
    handle_signature_modal,
    display_success_messages,
    handle_undo_last_selection,
    apply_selected_button_style,
    display_employee_buttons
)
from auth import check_datenschutz_pin
from timer import display_back_button, check_timer, start_timer
from session_state import initialize_employee_session_state
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from navigation import return_to_company_selection
from message_utils import show_custom_employee_message
from admin import admin_panel
from math import ceil

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
            if st.button(employee, key=f"employee_{employee}", use_container_width=True):
                add_employee(employee)
                st.success(get_text(f"Sie haben sich erfolgreich als {employee} angemeldet.", f"You have successfully logged in as {employee}."))
                st.session_state.page = 'select_company'
                st.rerun()

    display_back_button()

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

def handle_employee_selection(employee):
    if st.session_state.require_signature:
        st.session_state.current_employee = employee
        st.session_state.show_signature_modal = True
    else:
        add_employee_to_attendance(employee)

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

def add_employee(employee):
    add_employee_to_attendance(employee)
    st.session_state.current_employee = employee
    
    if st.session_state.require_signature:
        st.session_state.show_signature_modal = True
    else:
        add_success_message(employee)
    
    if employee in st.session_state.custom_employee_messages:
        show_custom_employee_message(employee)
    
    start_timer()

__all__ = ['select_employee']
