# state_management.py

import streamlit as st
from text_utils import get_text

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

def delete_attendance_record():
    st.session_state.attendance_data = []
    st.success(get_text("Anwesenheitsdaten wurden gelöscht.", "Attendance data has been deleted."))

def save_current_attendance():
    from attendance import save_attendance  
    if save_attendance():
        st.success(get_text("Aktuelle Anwesenheit wurde gespeichert.", "Current attendance has been saved."))
    else:
        st.warning(get_text("Keine Anwesenheitsdaten zum Speichern vorhanden.", "No attendance data available to save."))

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = False
    if 'admin_access_granted' not in st.session_state:
        st.session_state.admin_access_granted = False
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = None
    if 'selected_team' not in st.session_state:
        st.session_state.selected_team = None
    if 'selected_employee' not in st.session_state:
        st.session_state.selected_employee = None
    if 'added_employees' not in st.session_state:
        st.session_state.added_employees = []
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'countdown_start_time' not in st.session_state:
        st.session_state.countdown_start_time = None
    if 'success_messages' not in st.session_state:
        st.session_state.success_messages = []
    if 'last_message_time' not in st.session_state:
        st.session_state.last_message_time = None
    if 'all_employees_added_time' not in st.session_state:
        st.session_state.all_employees_added_time = None