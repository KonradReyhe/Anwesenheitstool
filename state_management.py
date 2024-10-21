# state_management.py
import streamlit as st

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

import streamlit as st
from utils import get_text
from save_operations import save_attendance

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
