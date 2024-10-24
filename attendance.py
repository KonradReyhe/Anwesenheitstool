# attendance.py

# Import necessary libraries and modules
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os
from text_utils import get_text
from timer import start_timer
import zipfile

def add_success_message(employee):
    """
    Add a success message for the newly added employee.
    This function creates and stores a success message in the session state, which will be displayed to the user.

    Args:
        employee (str): The name of the employee that was added to the attendance list.
    """
    # Clear existing success messages
    st.session_state.success_messages = []
    
    # Create a new success message for the added employee
    new_message = get_text(
        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
        f'Employee "{employee}" has been added to the attendance list.'
    )
    st.session_state.success_messages.append(new_message)
    st.session_state.last_message_time = time.time()

def add_employee_to_attendance(employee, from_signature_modal=False):
    """
    Add an employee to the attendance list and perform related actions.
    
    Args:
        employee (str): The name of the employee to add.
        from_signature_modal (bool): Indicates if the function is called from the signature modal.
    """
    # Get current time
    now = datetime.now()
    # Generate employee initials
    employee_initials = ''.join([name[0].upper() for name in employee.split()])[:3]
    # Create a short ID for the employee
    short_id = f"{employee_initials}{now.strftime('%H%M%S')}"
    # Create a new attendance record
    new_record = {
        'ID': short_id,
        'Name': employee,
        'Firma': st.session_state.selected_company,
        'Team': st.session_state.selected_team,
        'Zeit': now.strftime("%Y-%m-%d %H:%M:%S")
    }
    # Add the new record to the attendance data
    st.session_state.attendance_data.append(new_record)
    st.session_state.added_employees.append(employee)
    # Auto-save the attendance data
    auto_save_attendance()
    # Add a success message
    add_success_message(employee)
    # Start the timer
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
    if not st.session_state.attendance_data:
        return None

    attendance_df = pd.DataFrame(st.session_state.attendance_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if st.session_state.custom_event_name:
        sanitized_event_name = st.session_state.custom_event_name.replace(" ", "_")
        attendance_csv = f"GetTogether_{sanitized_event_name}_{timestamp}.csv"
    else:
        attendance_csv = f"GetTogether_{timestamp}.csv"

    attendance_csv_path = os.path.join("data", attendance_csv)
    attendance_df.to_csv(attendance_csv_path, index=False)

    zip_file_name = f"GetTogether_{timestamp}.zip"
    zip_file_path = os.path.join("data", zip_file_name)

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(attendance_csv_path, arcname=attendance_csv)

        if 'signature_pdf_path' in st.session_state and st.session_state.signature_pdf_path and os.path.exists(st.session_state.signature_pdf_path):
            pdf_filename = os.path.basename(st.session_state.signature_pdf_path)
            zipf.write(st.session_state.signature_pdf_path, arcname=pdf_filename)
            os.remove(st.session_state.signature_pdf_path)

    os.remove(attendance_csv_path)
    st.session_state.signature_pdf_path = None

    return zip_file_path

def undo_last_employee_selection():
    """
    Remove the last added employee from the attendance list and related data structures.
    This function is used to undo the most recent employee addition.
    """
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

# Define public interface for this module
__all__ = [
    'add_employee_to_attendance',
    'auto_save_attendance',
    'save_attendance',
    'undo_last_employee_selection'
]
