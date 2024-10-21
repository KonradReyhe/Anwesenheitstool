# attendance.py

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os
from text_utils import get_text
from navigation import return_to_company_selection
from timer import start_timer
from state_management import check_company_team_change

def add_success_message(employee):
    new_message = get_text(
        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
        f'Employee "{employee}" has been added to the attendance list.'
    )
    st.session_state.success_messages.append(new_message)
    st.session_state.last_message_time = time.time()

def add_employee_to_attendance(employee):
    now = datetime.now()
    employee_initials = ''.join([name[0].upper() for name in employee.split()])[:3]
    short_id = f"{employee_initials}{now.strftime('%H%M%S')}"
    new_record = {
        'ID': short_id,
        'Name': employee,
        'Firma': st.session_state.selected_company,
        'Team': st.session_state.selected_team,
        'Zeit': now.strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.attendance_data.append(new_record)
    st.session_state.added_employees.append(employee)
    auto_save_attendance()
    add_success_message(employee)
    
    if st.session_state.require_signature:
        st.session_state.show_signature_modal = True
    
    start_timer()



def auto_save_attendance():
    if st.session_state.attendance_data:
        attendance_df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        file_path = os.path.join(local_data_dir, file_name)
        attendance_df.to_csv(file_path, index=False, encoding='utf-8')
        st.session_state.last_auto_save = datetime.now()

def save_attendance():
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Anwesenheit_{timestamp}.csv"
        df.to_csv(file_name, index=False)
    return False

def undo_last_employee_selection():
    if st.session_state.added_employees:
        last_employee = st.session_state.added_employees.pop()
        
        st.session_state.attendance_data = [
            record for record in st.session_state.attendance_data 
            if record['Name'] != last_employee
        ]
        
        if last_employee in st.session_state.signatures:
            del st.session_state.signatures[last_employee]
        
        undo_message = get_text(
            f'Mitarbeiter "{last_employee}" wurde von der Anwesenheitsliste entfernt.',
            f'Employee "{last_employee}" has been removed from the attendance list.'
        )
        st.session_state.success_messages.append(undo_message)
        st.session_state.last_message_time = time.time()
        
        auto_save_attendance()
        
        st.experimental_rerun()

__all__ = [
    'add_employee_to_attendance',
    'auto_save_attendance',
    'save_attendance',
    'undo_last_employee_selection'
]
