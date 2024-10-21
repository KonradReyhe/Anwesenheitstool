# utils.py

import streamlit as st
import zipfile
import os
from datetime import datetime
import pytz
import time
from email_utils import send_documents_to_accounting
from config import VERSION
from text_utils import get_text  


local_tz = pytz.timezone('Europe/Berlin')

def create_zip_file(files, output_path):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))

def end_get_together():
    from attendance import save_attendance  # Import inside the function
    zip_file_name = save_attendance()
    if zip_file_name:
        send_documents_to_accounting(zip_file_name)
        os.remove(zip_file_name)  # Clean up after sending
    st.session_state.get_together_started = False
    st.session_state.page = 'home'
    st.success(get_text("GetTogether wurde beendet.", "GetTogether has been ended."))
    st.experimental_rerun()

def schedule_event_end(end_time):
    st.session_state.end_time = end_time.astimezone(local_tz)

def check_event_end():
    if 'end_time' in st.session_state and st.session_state.end_time and not st.session_state.get('cancel_end', False):
        now = datetime.now(local_tz)
        if now >= st.session_state.end_time:
            end_get_together()
            st.session_state.get_together_started = False
            st.session_state.page = 'home'
            st.experimental_rerun()

def display_countdown_timer():
    if 'scheduled_end_time' in st.session_state and st.session_state.scheduled_end_time:
        now = datetime.now()
        time_left = st.session_state.scheduled_end_time - now
        if time_left.total_seconds() > 0:
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.write(f"Time left: {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            st.write(get_text("Zeit abgelaufen", "Time's up"))

def cancel_scheduled_end():
    st.session_state.scheduled_end_time = None

def trigger_rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

def toggle_language():
    st.session_state.language = 'EN' if st.session_state.language == 'DE' else 'DE'
    st.success(get_text("Sprache wurde geändert.", "Language has been changed."))
    st.rerun()


def update_last_activity():
    st.session_state.last_activity_time = time.time()




