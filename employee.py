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
    if not check_datenschutz_pin():
        return
    if not check_datenschutz_pin():
        display_header()
        display_company_team_info()
        
        if st.session_state.show_admin_panel:
            admin_panel()
        
        if not st.session_state.admin_access_granted:
            employees = get_employees_for_team(st.session_state.selected_company, st.session_state.selected_team)
            if not employees:
                return
            if not employees:
                st.markdown(f"<div class='sub-header'>{get_text('Mitarbeiter*innen auswählen:', 'Select employees:')}</div>", unsafe_allow_html=True)
                
                initialize_employee_session_state()
                check_company_team_change()
                initialize_employee_session_state()
                display_employee_buttons(employees)
                
                handle_signature_modal()
                display_success_messages()
                handle_undo_last_selection()
                check_all_employees_added(employees)
                
                # Automatically refresh the app every second to update the countdown and messages
                st_autorefresh(interval=1000, key="autorefresh")
                
                display_back_button()
                display_back_button()
    st.session_state.last_activity_time = time.time()

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

__all__ = ['select_employee']
