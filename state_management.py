# state_management.py

"""
state_management.py

This module handles the management of application state, including
checking for changes in company/team selection, deleting attendance records,
and saving current attendance data.
"""

import streamlit as st
from text_utils import get_text

def check_company_team_change():
    """
    Check if the selected company or team has changed and reset relevant session state variables.

    This function compares the current company and team selection with the previous selection.
    If a change is detected, it resets various session state variables and triggers a rerun.
    """
    # Get the current company and team
    current_company_team = (st.session_state.selected_company, st.session_state.selected_team)
    # Check if the company or team has changed
    if st.session_state.current_company_team != current_company_team:
        # Reset relevant session state variables
        st.session_state.added_employees = []
        st.session_state.current_company_team = current_company_team
        st.session_state.timer_active = False
        st.session_state.countdown_start_time = None
        st.session_state.success_messages = []
        st.session_state.last_message_time = None
        st.session_state.all_employees_added_time = None
        st.rerun()  
    # Display a success message indicating that attendance data has been deleted
    st.success(get_text("Anwesenheitsdaten wurden gelöscht.", "Attendance data has been deleted."))
def delete_attendance_record():
    """
    Delete all attendance records and display a success message.

    This function clears the attendance data stored in the session state
    and shows a success message to the user.
    """
    # Clear the attendance data
    st.session_state.attendance_data = []
    st.success(get_text("Anwesenheitsdaten wurden gelöscht.", "Attendance data has been deleted."))
def save_current_attendance():
    """
    Save the current attendance data and display a success or warning message.

    This function attempts to save the current attendance data using the save_attendance
    function from the attendance module. It then displays an appropriate message based
    on whether the save was successful.
    """
    # Import save_attendance function to avoid circular import
    from attendance import save_attendance  
    if save_attendance():
        st.success(get_text("Aktuelle Anwesenheit wurde gespeichert.", "Current attendance has been saved."))
    else:
        st.warning(get_text("Keine Anwesenheitsdaten zum Speichern vorhanden.", "No attendance data available to save."))

def initialize_session_state():
    """
    Initialize the session state with default values for various application variables.
    This function sets up the initial state for the Streamlit application, ensuring
    all necessary variables are present with default values.
    """
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
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'  # Default to German
    if 'datenschutz_pin_active' not in st.session_state:
        st.session_state.datenschutz_pin_active = False

