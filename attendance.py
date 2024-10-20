# attendance.py

print("Loading attendance.py")
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import time
import os
import zipfile
import io
from utils import get_text, add_success_message, auto_save_attendance
from pdf_utils import generate_pdf
from navigation import return_to_company_selection
from message_utils import show_custom_employee_message
from timer import start_timer
from data_utils import get_companies, get_teams_for_company, get_employees_for_team
from save_operations import save_attendance


print("Defining get_companies function")
def delete_attendance_record():
    st.session_state.attendance_data = []
    st.success(get_text("Anwesenheitsdaten wurden gelöscht.", "Attendance data has been deleted."))

def save_current_attendance():
    if save_attendance():
        st.success(get_text("Aktuelle Anwesenheit wurde gespeichert.", "Current attendance has been saved."))
    else:
        st.warning(get_text("Keine Anwesenheitsdaten zum Speichern vorhanden.", "No attendance data available to save."))

def check_company_team_change():
    current_company_team = (st.session_state.selected_company, st.session_state.selected_team)
    if st.session_state.current_company_team != current_company_team:
        st.session_state.added_employees = []
        st.session_state.current_company_team = current_company_team
        st.session_state.timer_active = False
        st.session_state.countdown_start_time = None
        st.session_state.success_messages = []
        st.session_state.last_message_time = None
        st.session_state.all_employees_added_time = None

def add_employee_to_attendance(employee):
    now = datetime.now()
    new_record = {
        'ID': f"{employee}_{now.strftime('%Y%m%d%H%M%S')}",
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
    
    if employee in st.session_state.custom_employee_messages:
        show_custom_employee_message(employee)
    
    start_timer()

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

def get_teams_for_company(company, file_path="Firmen_Teams_Mitarbeiter.csv"):
    df = pd.read_csv(file_path)
    teams = df[df['Firma'] == company]['Team'].unique().tolist()
    return teams

def guest_info():
    st.title(get_text("Gast-Information", "Guest Information"))
    st.session_state.guest_name = st.text_input(get_text("Name des Gastes", "Guest Name"))
    st.session_state.guest_company = st.text_input(get_text("Firma des Gastes", "Guest Company"))
    if st.button(get_text("Bestätigen", "Confirm")):
        submit_guest()


