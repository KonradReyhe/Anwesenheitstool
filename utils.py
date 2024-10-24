# utils.py

"""
This module contains utility functions for the GetTogether application,
including file operations, event management, and email sending.
"""

import streamlit as st
import zipfile
import os
from datetime import datetime
import pytz
import time
from email_utils import send_documents_to_accounting
from config import VERSION
from text_utils import get_text  
import asyncio
import pandas as pd

# Set up timezone for Berlin
local_tz = pytz.timezone('Europe/Berlin')

def create_zip_file(files, output_path):
    """
    Create a zip file containing the specified files.

    Args:
        files (list): List of file paths to be included in the zip file.
        output_path (str): Path where the zip file will be saved.
    """
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))

def end_get_together():
    """
    End the current GetTogether event, save attendance data, send email, and clean up.

    This function saves the attendance data, attempts to send an email with the data,
    and resets the application state to prepare for a new event.
    """
    from attendance import save_attendance
    zip_file_name = save_attendance()
    if zip_file_name:
        email_sent = send_documents_to_accounting(zip_file_name)
        if email_sent:
            st.success(get_text("GetTogether wurde beendet und E-Mail wurde gesendet.", "GetTogether has been ended and email was sent."))
        else:
            st.warning(get_text("GetTogether wurde beendet, aber E-Mail wurde nicht gesendet.", "GetTogether has been ended, but email was not sent."))
        if os.path.exists(zip_file_name):
            os.remove(zip_file_name)
    else:
        st.warning(get_text("Keine Anwesenheitsdaten zum Speichern.", "No attendance data to save."))
    
    # Reset session state variables
    st.session_state.get_together_started = False
    st.session_state.page = 'home'
    st.session_state.signature_pdf_path = None
    st.session_state.attendance_data = []
    st.session_state.added_employees = []
    st.rerun()

def schedule_event_end(end_time):
    st.session_state.end_time = end_time.astimezone(local_tz)

async def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.rerun()
    await asyncio.sleep(0)  

@st.cache_data(ttl=60)  
def display_countdown_timer():
    if 'scheduled_end_time' in st.session_state and st.session_state.scheduled_end_time:
        now = datetime.now()
        time_left = st.session_state.scheduled_end_time - now
        if time_left.total_seconds() > 0:
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"Time left: {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return get_text("Zeit abgelaufen", "Time's up")
    return ""

def cancel_scheduled_end():
    st.session_state.scheduled_end_time = None

def trigger_rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

def toggle_language():
    if 'language' not in st.session_state:
        st.session_state.language = 'DE'
    
    st.session_state.language = 'EN' if st.session_state.language == 'DE' else 'DE'
    st.rerun()

def update_last_activity():
    st.session_state.last_activity_time = time.time()

def load_master_data(force_update=False):
    try:
        if force_update or 'master_data' not in st.session_state:
            master_data = pd.read_csv('path_to_master_data.csv')  
            st.session_state.master_data = master_data
        return True
    except Exception as e:
        st.error(f"Error loading master data: {e}")
        return False





