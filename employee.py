#employee.py
import streamlit as st
import time
from utils import get_text, add_success_message, auto_save_attendance, update_last_activity
from attendance import (
    add_employee_to_attendance, 
    get_employees_for_team, 
    check_company_team_change,
    check_all_employees_added
)
from ui_components import (
    display_header, 
    display_company_team_info, 
    admin_panel,
    show_custom_employee_message,
    handle_signature_modal,
    display_success_messages,
    handle_undo_last_selection,
    apply_selected_button_style
)
from auth import check_datenschutz_pin
from timer import display_back_button, check_timer, start_timer
from session_state import initialize_employee_session_state
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

def select_employee():
    if not check_datenschutz_pin():
        return

    display_header()
    display_company_team_info()
    
    if st.session_state.show_admin_panel:
        admin_panel()
    
    if not st.session_state.admin_access_granted:
        employees = get_employees_for_team()
        if not employees:
            return

        st.markdown(f"<div class='sub-header'>{get_text('Mitarbeiter*innen auswählen:', 'Select employees:')}</div>", unsafe_allow_html=True)
        
        initialize_employee_session_state()
        check_company_team_change()

        display_employee_buttons(employees)
        
        handle_signature_modal()
        display_success_messages()
        handle_undo_last_selection()
        check_all_employees_added(employees)
        
        st_autorefresh(interval=1000, key="autorefresh")
        
        display_back_button()
        check_timer()

    update_last_activity()

def display_employee_buttons(employees):
    num_columns = 3
    columns = st.columns(num_columns)
    for i, employee in enumerate(employees):
        with columns[i % num_columns]:
            button_key = f"employee_button_{employee}"
            if st.button(employee, key=button_key, use_container_width=True):
                handle_employee_selection(employee)
            if employee in st.session_state.added_employees:
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
        st.experimental_rerun()

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
