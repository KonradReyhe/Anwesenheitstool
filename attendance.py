# attendance.py

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os
from text_utils import get_text
from timer import start_timer
import zipfile

def add_success_message(employee):
    st.session_state.success_messages = []
    
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
        
        if 'ID' in attendance_df.columns:
            attendance_df = attendance_df.drop(columns=['ID'])
        
        local_data_dir = "data"
        os.makedirs(local_data_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        if st.session_state.custom_event_name:
            sanitized_event_name = st.session_state.custom_event_name.replace(" ", "_")
            file_name = f"GetTogether_{sanitized_event_name}_{timestamp}.csv"
        else:
            file_name = f"GetTogether_{timestamp}.csv"
        
        file_path = os.path.join(local_data_dir, file_name)
        attendance_df.to_csv(file_path, index=False, encoding='utf-8')
        st.session_state.last_auto_save = datetime.now()

def save_attendance():
    if st.session_state.attendance_data:
        df = pd.DataFrame(st.session_state.attendance_data)
        
        if 'ID' in df.columns:
            df = df.drop(columns=['ID'])
        
        timestamp = datetime.now().strftime("%Y%m%d")
        if st.session_state.custom_event_name:
            sanitized_event_name = st.session_state.custom_event_name.replace(" ", "_")
            csv_file_name = f"GetTogether_{sanitized_event_name}_{timestamp}.csv"
            zip_file_name = f"GetTogether_{sanitized_event_name}_{timestamp}.zip"
        else:
            csv_file_name = f"GetTogether_{timestamp}.csv"
            zip_file_name = f"GetTogether_{timestamp}.zip"
        
        df.to_csv(csv_file_name, index=False, encoding='utf-8')
        with zipfile.ZipFile(zip_file_name, 'w') as zipf:
            zipf.write(csv_file_name, arcname=csv_file_name)
        os.remove(csv_file_name)  
        return zip_file_name
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
        
        st.rerun()

__all__ = [
    'add_employee_to_attendance',
    'auto_save_attendance',
    'save_attendance',
    'undo_last_employee_selection'
]

