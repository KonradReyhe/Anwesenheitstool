# app_functions.py
import streamlit as st
import time
from utils import get_text
from core_functions import delete_attendance_record, save_current_attendance
from admin import admin_panel as admin_panel_func

def add_success_message(employee):
    new_message = get_text(
        f'Mitarbeiter "{employee}" wurde zur Anwesenheitsliste hinzugefügt.',
        f'Employee "{employee}" has been added to the attendance list.'
    )
    st.session_state.success_messages.append(new_message)
    st.session_state.last_message_time = time.time()

def admin_panel():
    admin_panel_func(delete_attendance_record, save_current_attendance)
